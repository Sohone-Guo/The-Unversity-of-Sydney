'''
----This code made for University of Syndey SIT Machine Learning assignment 2 by Xuhong GUO, Huixin,CHEN

----This code learn from:
    1: Tensorflow TURORIALS: https://www.tensorflow.org/tutorials/deep_cnn
    2: Tensorflow tutorial on Youtube: Kevin Xu
    3: Tensorflow tutorial on Youtube: Hvass Laboratories
    4: Deep Learning tutorial on Youtube: sentdex

---- Envoirnment:
    1: Ubuntu 16
    2: Anaconda 3.6
    3: Tensorflow 1.0
    4: I5, 8G memory
    
----- Datasets:
http://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz
'''


import tensorflow as tf # Start the Tensorflow Lib
import numpy as np 
import os
import math
from sklearn.metrics import classification_report # For evaluation

''' Data prepocessing '''
if os.path.exists('input/') is True and os.path.exists('output/') is False:
    print('Begin data preporcessing, transfer data_batch_1/5 --> data_batch_1/10 ')
    os.system('mkdir output')
    os.system('split -n 2 -d --additional-suffix=.bin input/data_batch_1.bin output/data_batch_1-')
    os.system('split -n 2 -d --additional-suffix=.bin input/data_batch_2.bin output/data_batch_2-')
    os.system('split -n 2 -d --additional-suffix=.bin input/data_batch_3.bin output/data_batch_3-')
    os.system('split -n 2 -d --additional-suffix=.bin input/data_batch_4.bin output/data_batch_4-')
    os.system('split -n 2 -d --additional-suffix=.bin input/data_batch_5.bin output/data_batch_5-')

    os.system('mv output/data_batch_1-00.bin output/data_batch_1.bin')
    os.system('mv output/data_batch_1-01.bin output/data_batch_2.bin')
    os.system('mv output/data_batch_2-00.bin output/data_batch_3.bin')
    os.system('mv output/data_batch_2-01.bin output/data_batch_4.bin')
    os.system('mv output/data_batch_3-00.bin output/data_batch_5.bin')
    os.system('mv output/data_batch_3-01.bin output/data_batch_6.bin')
    os.system('mv output/data_batch_4-00.bin output/data_batch_7.bin')
    os.system('mv output/data_batch_4-01.bin output/data_batch_8.bin')
    os.system('mv output/data_batch_5-00.bin output/data_batch_9.bin')
    os.system('mv output/data_batch_5-01.bin output/data_batch_10.bin')
else:
    print('No input file, or have already finished data prepocessing. Begin to Training...')


training_files_index = 1 # File 4 
if os.path.exists('Model/') is False:
    os.system('mkdir Model/')
os.system('mkdir Model/log_%d/'%training_files_index)

BATCH_SIZE = 128
learning_rate = 0.05
MAX_STEP = 1000
n_test = 5000


img_width = 32
img_height = 32
img_depth = 3
img_pixel = img_width*img_height*img_depth
label_bytes = 1
image_bytes = img_width*img_height*img_depth

data_url='../Dataset/cifa_split/cifar-10-batches-bin/result/'
log_url = 'Model/log_%d/'%training_files_index
test_url = data_url


print(
    'The setting is in this training model: \n'
    'Read file from: %s \n'%data_url,
    'Model file save at: %s \n'%log_url,
    'Testing file is: output/data_batch_%d.bin \n'%training_files_index,
    'Batch size:%d \n'%BATCH_SIZE,
    'Learning rate:%d \n'%learning_rate,
    'Max of step: %d \n'%MAX_STEP,
    'Number of test: %d \n'%n_test,
    'Image width:%d, Image height:%d, Image depth: %d, Image pixel: %d, Label bytes: %d, image_bytes: %d \n'%(img_width,img_height,img_depth,img_pixel,label_bytes,image_bytes)
    )

def read_data(data_url,is_train,batch_size,shuffle): # Read the binary data
    with tf.name_scope('input'):
        if is_train: # If it is trainning
            filenames = [os.path.join(data_url,'data_batch_%d.bin'%ii) for ii in [i for i in range(1,11) if i!=training_files_index]]
        else: # If it is testing
            filenames = [os.path.join(data_url,'data_batch_%d.bin'%training_files_index)]

        _,value = tf.FixedLengthRecordReader(label_bytes+image_bytes).read(tf.train.string_input_producer(filenames)) # Read data
        record_bytes = tf.decode_raw(value,tf.uint8) # Decode the data
        label = tf.cast(tf.slice(record_bytes,[0],[label_bytes]),tf.int32) # Transfer the int8 to int32
        image_raw = tf.reshape(tf.slice(record_bytes,[label_bytes],[image_bytes]),[img_depth,img_height,img_width]) # Slice the data as depth, height,width
        image = tf.cast(tf.transpose(image_raw,(1,2,0)),tf.float32) # Transfor the order of depth, height,width to height width depth
        image = tf.image.per_image_standardization(image) # Standard the image values
        if shuffle: # If shuffle
            images, label_batch = tf.train.shuffle_batch(
                [image,label],
                batch_size = batch_size,
                num_threads = 2,
                capacity = 2000,
                min_after_dequeue = 1500
            ) 

        else:
            images, label_batch = tf.train.batch(
                [image,label],
                batch_size = batch_size,
                num_threads = 2,
                capacity = 2000
            )

        return images,tf.reshape(label_batch,[batch_size])

def inference(images): # Model 
    with tf.variable_scope('conv1') as scope: # First layer
        weights = tf.get_variable(
            'weights',
            shape = [3,3,3,96],
            dtype = tf.float32,
            initializer = tf.truncated_normal_initializer(stddev=0.05,dtype=tf.float32)
            ) # W values in first layer
        biases = tf.get_variable(
            'biases',
            shape=[96],
            dtype = tf.float32,
            initializer = tf.constant_initializer(0.0)
            ) # b value in first layer
        conv = tf.nn.conv2d(images,weights,strides=[1,1,1,1],padding='SAME') # Image to 2d
        pre_activation = tf.nn.bias_add(conv,biases) 
        conv1 = tf.nn.relu(pre_activation,name=scope.name)

    with tf.variable_scope('pooling1_lrn') as scope:
        pool1 = tf.nn.max_pool(conv1,ksize=[1,3,3,1],strides=[1,2,2,1],padding='SAME',name='pooling1')
        norm1 = tf.nn.lrn(pool1,depth_radius =4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='norm1')

    with tf.variable_scope('conv2') as scope: # Second layer
        weights = tf.get_variable(
            'weights',
            shape = [3,3,96,64],
            dtype = tf.float32,
            initializer = tf.truncated_normal_initializer(stddev=0.05,dtype=tf.float32)
            ) # W value for second layer
        biases = tf.get_variable(
            'biases',
            shape=[64],
            dtype = tf.float32,
            initializer = tf.constant_initializer(0.1)
            )
        conv = tf.nn.conv2d(norm1,weights,strides=[1,1,1,1],padding='SAME')
        pre_activation = tf.nn.bias_add(conv,biases)
        conv2 = tf.nn.relu(pre_activation,name='conv2')

    with tf.variable_scope('pooling2_lrn') as scope:
        norm2 = tf.nn.lrn(conv2,depth_radius =4,bias=1.0,alpha=0.001/9.0,beta=0.75,name='norm2')
        pool2 = tf.nn.max_pool(norm2,ksize=[1,3,3,1],strides=[1,1,1,1],padding='SAME',name='pooling2')

    with tf.variable_scope('local3') as scope:
        reshape = tf.reshape(pool2,shape=[BATCH_SIZE,-1])
        dim =reshape.get_shape()[1].value
        weights = tf.get_variable(
            'weights',
            shape = [dim,384],
            dtype = tf.float32,
            initializer = tf.truncated_normal_initializer(stddev=0.004,dtype=tf.float32)
        )

        biases = tf.get_variable(
            'biases',
            shape=[384],
            dtype = tf.float32,
            initializer  =tf.constant_initializer(0.1)
        )

        local3 = tf.nn.relu(tf.matmul(reshape,weights)+biases,name=scope.name)

    with tf.variable_scope('local4') as scope:
        weights = tf.get_variable(
            'weights',
            shape = [384,192],
            dtype = tf.float32,
            initializer = tf.truncated_normal_initializer(stddev=0.004,dtype=tf.float32)
        )

        biases = tf.get_variable(
            'biases',
            shape=[192],
            dtype = tf.float32,
            initializer  =tf.constant_initializer(0.1)
        )

        local4 = tf.nn.relu(tf.matmul(local3,weights)+biases,name='local4')

    with tf.variable_scope('softmax_linear') as scope:
        weights = tf.get_variable(
            'softmax_linear',
            shape = [192,10],
            dtype = tf.float32,
            initializer = tf.truncated_normal_initializer(stddev=0.004,dtype=tf.float32)
        )

        biases = tf.get_variable(
            'biases',
            shape=[10],
            dtype = tf.float32,
            initializer  =tf.constant_initializer(0.1)
        )

        softmax_linear = tf.add(tf.matmul(local4,weights),biases,name='softmax_linear')
    return softmax_linear

def losses(logits,labels): # Loss Fucntion
    with tf.variable_scope('loss') as scope:
        labels = tf.cast(labels,tf.int64)

        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,labels=labels,name='xentropy_per_example')
        loss = tf.reduce_mean(cross_entropy,name='loss')
        tf.summary.scalar(scope.name + '/loss',loss)
    return loss

def train(): # Training part
    Glob_Step = tf.Variable(0,name='glob_step',trainable = False)

    images,labels = read_data(data_url=data_url,is_train=True,batch_size=BATCH_SIZE,shuffle=True)

    logits = inference(images) # Fit the model 
    loss = losses(logits,labels) # Get the loss 

    optimizer = tf.train.GradientDescentOptimizer(learning_rate) # Learning method
    train_op = optimizer.minimize(loss, global_step = Glob_Step)

    saver = tf.train.Saver(tf.global_variables()) # Generate a save for model
    summary_op = tf.summary.merge_all()

    init = tf.global_variables_initializer()
    sess = tf.Session() # Set 
    sess.run(init) # Run the model

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess,coord=coord)

    summary_writer = tf.summary.FileWriter(log_url,sess.graph)

    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                break
            _,loss_value = sess.run([train_op,loss])

            if step%50==0:
                print('Step:%d, loss:%.4f'%(step,loss_value))

            if step%100 == 0:
                summary_str = sess.run(summary_op)
                summary_writer.add_summary(summary_str,step)
            if step%2000 == 0 or (step+1)==MAX_STEP: # Save the model
                checkpoint_path = os.path.join(log_url,'model.ckpt')
                saver.save(sess,checkpoint_path,global_step=step)
    except tf.errors.OutOfRangeError:
        print('Done training ----epoch liit reached')
    finally:
        coord.request_stop()
    coord.join(threads)
    sess.close()

def evaluate(): #  Evluate
    with tf.Graph().as_default():
        images,labels = read_data(
            data_url=test_url,
            is_train=False,
            batch_size=BATCH_SIZE,
            shuffle=False
        ) # Read the testing data

        logits = inference(images)
        arg_max_predict_y = tf.argmax(logits,1)
        saver = tf.train.Saver(tf.global_variables())

        with tf.Session() as sess: # Read the models
            print('Reading checkpoints...')
            ckpt = tf.train.get_checkpoint_state(log_url)
            if ckpt and ckpt.model_checkpoint_path:
                global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]

                saver.restore(sess,ckpt.model_checkpoint_path)
                print('Loading success, global_step is %s'%global_step)
            else:
                print('No checkpoint file found')
                return

            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess,coord=coord)

            try:
                num_iter = int(math.ceil(n_test/BATCH_SIZE))
                step = 0
                predicted_list = []
                true_y_list = []
                while step < num_iter and not coord.should_stop():
                    predicted_y,true_y = sess.run([arg_max_predict_y,tf.cast(labels,tf.int64)])
                    predicted_list.extend(predicted_y)
                    true_y_list.extend(true_y)
                    step+=1
                print("Classification Report:\n%s" % classification_report(true_y_list, predicted_list)) # Genertate the report of evluation

            except Exception as e:
                coord.request_stop(e)

            finally:
                coord.request_stop()
                coord.join(threads)
                
train()
# evaluate()