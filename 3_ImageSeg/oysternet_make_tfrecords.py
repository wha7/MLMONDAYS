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

from imports import *

###############################################################
## VARIABLES
###############################################################

imdir = os.getcwd()+os.sep+'data/oysternet/train_images/data'

# # Convert folder of pngs into jpegs
# for file in *.png
# do
# convert $file $"${file%.png}.jpg"
# done

lab_path = os.getcwd()+os.sep+'data/oysternet/train_labels/data'

tfrecord_dir = os.getcwd()+os.sep+'/data/oysternet/'+str(TARGET_SIZE)

images = tf.io.gfile.glob(imdir+os.sep+'*.jpg') #1054

nb_images=len(tf.io.gfile.glob(imdir+os.sep+'*.jpg'))

SHARDS = int(nb_images / ims_per_shard) + (1 if nb_images % ims_per_shard != 0 else 0)

shared_size = int(np.ceil(1.0 * nb_images / SHARDS))

dataset = get_seg_dataset_for_tfrecords_oysternet(imdir, lab_path, shared_size)

# # view a batch
# for imgs,lbls in dataset.take(1):
#   imgs = imgs[:BATCH_SIZE]
#   lbls = lbls[:BATCH_SIZE]
#   for count,(im,lab) in enumerate(zip(imgs,lbls)):
#      plt.subplot(int(BATCH_SIZE/2),int(BATCH_SIZE/2),count+1)
#      plt.imshow(tf.image.decode_jpeg(im, channels=3))
#      plt.imshow(tf.image.decode_jpeg(lab, channels=1), alpha=0.5, cmap='gray')
#      plt.axis('off')
# plt.show()

filestr = "oysternet-train"
write_seg_records_oysternet(dataset, tfrecord_dir, filestr)

#





imdir = os.getcwd()+os.sep+'data/oysternet/test_images/data'

# # Convert folder of pngs into jpegs
# for file in *.png
# do
# convert $file $"${file%.png}.jpg"
# done

lab_path = os.getcwd()+os.sep+'data/oysternet/test_labels/data'

tfrecord_dir = os.getcwd()+os.sep+'/data/oysternet/'+str(TARGET_SIZE)

images = tf.io.gfile.glob(imdir+os.sep+'*.jpg') #1054

nb_images=len(tf.io.gfile.glob(imdir+os.sep+'*.jpg'))

SHARDS = int(nb_images / ims_per_shard) + (1 if nb_images % ims_per_shard != 0 else 0)

shared_size = int(np.ceil(1.0 * nb_images / SHARDS))

dataset = get_seg_dataset_for_tfrecords_oysternet(imdir, lab_path, shared_size)

# view a batch
for imgs,lbls in dataset.take(1):
  imgs = imgs[:BATCH_SIZE]
  lbls = lbls[:BATCH_SIZE]
  for count,(im,lab) in enumerate(zip(imgs,lbls)):
     plt.subplot(int(BATCH_SIZE/2),int(BATCH_SIZE/2),count+1)
     plt.imshow(tf.image.decode_jpeg(im, channels=3))
     plt.imshow(tf.image.decode_jpeg(lab, channels=1), alpha=0.5, cmap='gray')
     plt.axis('off')
plt.show()

filestr = "oysternet-test"
write_seg_records_oysternet(dataset, tfrecord_dir, filestr)

#





imdir = os.getcwd()+os.sep+'data/oysternet/val_images/data'

# # Convert folder of pngs into jpegs
# for file in *.png
# do
# convert $file $"${file%.png}.jpg"
# done

lab_path = os.getcwd()+os.sep+'data/oysternet/val_labels/data'

tfrecord_dir = os.getcwd()+os.sep+'/data/oysternet/'+str(TARGET_SIZE)

images = tf.io.gfile.glob(imdir+os.sep+'*.jpg') #1054

nb_images=len(tf.io.gfile.glob(imdir+os.sep+'*.jpg'))

SHARDS = int(nb_images / ims_per_shard) + (1 if nb_images % ims_per_shard != 0 else 0)

shared_size = int(np.ceil(1.0 * nb_images / SHARDS))

dataset = get_seg_dataset_for_tfrecords_oysternet(imdir, lab_path, shared_size)

# view a batch
for imgs,lbls in dataset.take(1):
  imgs = imgs[:BATCH_SIZE]
  lbls = lbls[:BATCH_SIZE]
  for count,(im,lab) in enumerate(zip(imgs,lbls)):
     plt.subplot(int(BATCH_SIZE/2),int(BATCH_SIZE/2),count+1)
     plt.imshow(tf.image.decode_jpeg(im, channels=3))
     plt.imshow(tf.image.decode_jpeg(lab, channels=1), alpha=0.5, cmap='gray')
     plt.axis('off')
plt.show()

filestr = "oysternet-val"
write_seg_records_oysternet(dataset, tfrecord_dir, filestr)

#
