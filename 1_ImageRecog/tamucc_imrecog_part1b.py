# Written by Dr Daniel Buscombe, Marda Science LLC
# for "ML Mondays", a course supported by the USGS Community for Data Integration
# and the USGS Coastal Change Hazards Program
#
# MIT License
#
# Copyright (c) 2020, Marda Science LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

###############################################################
## IMPORTS
###############################################################
from imports import *

###############################################################
## FUNCTIONS
###############################################################

#-----------------------------------
def get_training_dataset():
    """
    This function will return a batched dataset for model training
    INPUTS: None
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: training_filenames
    OUTPUTS: batched data set object
    """
    return get_batched_dataset(training_filenames)

def get_validation_dataset():
    """
    This function will return a batched dataset for model training
    INPUTS: None
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: validation_filenames
    OUTPUTS: batched data set object
    """
    return get_batched_dataset(validation_filenames)

def get_validation_eval_dataset():
    """
    This function will return a batched dataset for model training
    INPUTS: None
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: validation_filenames
    OUTPUTS: batched data set object
    """
    return get_eval_dataset(validation_filenames)

#-----------------------------------
def get_aug_datasets():
    """
    This function will create train and validation sets based on a specific
    data augmentation pipeline consisting of random flipping, small rotations,
    translations and contrast adjustments
    INPUTS: None
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: validation_filenames, training_filenames
    OUTPUTS: two batched data set objects, one for training and one for validation
    """
    data_augmentation = tf.keras.Sequential([
      tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
      tf.keras.layers.experimental.preprocessing.RandomRotation(0.01),
      tf.keras.layers.experimental.preprocessing.RandomTranslation(0.1,0.1),
      tf.keras.layers.experimental.preprocessing.RandomContrast(0.1)
    ])

    augmented_train_ds = get_training_dataset().map(
      lambda x, y: (data_augmentation(x, training=True), y))

    augmented_val_ds = get_validation_dataset().map(
      lambda x, y: (data_augmentation(x, training=True), y))
    return augmented_train_ds, augmented_val_ds

def get_all_labels(nb_images, VALIDATION_SPLIT, BATCH_SIZE):
    """
    "get_all_labels"
    This function will obtain the classes of all samples in both train and
    validation sets. For computing class imbalance on the whole dataset
    INPUTS:
        * nb_images [int]: number of total images
    OPTIONAL INPUTS: None
    GLOBAL INPUTS: VALIDATION_SPLIT, BATCH_SIZE
    OUTPUTS:
        * l [list]: list of integers representing labels of each image
    """
    l = []
    num_batches = int(((1-VALIDATION_SPLIT) * nb_images) / BATCH_SIZE)
    train_ds = get_training_dataset()
    for _,lbls in train_ds.take(num_batches):
        l.append(lbls.numpy())

    val_ds = get_validation_dataset()
    num_batches = int(((VALIDATION_SPLIT) * nb_images) / BATCH_SIZE)
    for _,lbls in val_ds.take(num_batches):
        l.append(lbls.numpy())

    l = np.asarray(l).flatten()
    return l

###############################################################
## VARIABLES
###############################################################

## model inputs
data_path= os.getcwd()+os.sep+"data/tamucc/subset_2class/400"

test_samples_fig = os.getcwd()+os.sep+'results/tamucc_sample_2class_mv2_model2_est24samples.png'

cm_filename = os.getcwd()+os.sep+'results/tamucc_sample_2class_mv2_model2_cm_val.png'

sample_data_path= os.getcwd()+os.sep+"data/tamucc/subset_2class/sample"

hist_fig = os.getcwd()+os.sep+'results/tamucc_sample_2class_custom_model2.png'

filepath = os.getcwd()+os.sep+'results/tamucc_subset_2class_custom_best_weights_model2.h5'

CLASSES = [b'dev', b'undev']
patience = 10

###############################################################
## EXECUTION
###############################################################

filenames = sorted(tf.io.gfile.glob(data_path+os.sep+'*.tfrec'))

nb_images = ims_per_shard * len(filenames)
print(nb_images)

split = int(len(filenames) * VALIDATION_SPLIT)

training_filenames = filenames[split:]
validation_filenames = filenames[:split]

validation_steps = int(nb_images // len(filenames) * len(validation_filenames)) // BATCH_SIZE
steps_per_epoch = int(nb_images // len(filenames) * len(training_filenames)) // BATCH_SIZE

## data augmentation is typically used
augmented_train_ds, augmented_val_ds = get_aug_datasets()


lr_callback = tf.keras.callbacks.LearningRateScheduler(lambda epoch: lrfn(epoch), verbose=True)

#####################################################################
## class weights

l = get_all_labels(nb_images, VALIDATION_SPLIT, BATCH_SIZE)

# class weights will be given by n_samples / (n_classes * np.bincount(y))

class_weights = class_weight.compute_class_weight('balanced',
                                                 np.unique(l),
                                                 l)

class_weights = dict(enumerate(class_weights))
print(class_weights)

##==============================
numclass = len(CLASSES)

custom_model2 = make_cat_model(numclass, denseunits=256, base_filters = 30, dropout=0.5)


custom_model2.compile(optimizer=tf.keras.optimizers.Adam(),
          loss='sparse_categorical_crossentropy',
          metrics=['accuracy'])

earlystop = EarlyStopping(monitor="val_loss",
                              mode="min", patience=patience)

# set checkpoint file
model_checkpoint = ModelCheckpoint(filepath, monitor='val_loss',
                                verbose=0, save_best_only=True, mode='min',
                                save_weights_only = True)

callbacks = [model_checkpoint, earlystop, lr_callback]

do_train = False #True

if do_train:
    K.clear_session()

    history = custom_model2.fit(augmented_train_ds, steps_per_epoch=steps_per_epoch, epochs=MAX_EPOCHS,
                          validation_data=augmented_val_ds, validation_steps=validation_steps,
                          callbacks=callbacks, class_weight = class_weights)

    # Plot training history
    plot_history(history, hist_fig)
    # plt.show()
    # plt.savefig(hist_fig, dpi=200, bbox_inches='tight')

    plt.close('all')
    K.clear_session()

else:
    custom_model2.load_weights(filepath)


##########################################################
### evaluate
loss, accuracy = custom_model2.evaluate(get_validation_eval_dataset(), batch_size=BATCH_SIZE)
print('Test Mean Accuracy: ', round((accuracy)*100, 2),' %')

##85%

##########################################################
### predict

sample_filenames = sorted(tf.io.gfile.glob(sample_data_path+os.sep+'*.jpg'))

make_sample_plot(custom_model2, sample_filenames, test_samples_fig, CLASSES)

##################################################

## confusion matrix
val_ds = get_validation_eval_dataset()

labs, preds = get_label_pairs(val_ds, custom_model2)

p_confmat(labs, preds, cm_filename, CLASSES)

#80%
