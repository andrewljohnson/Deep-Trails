'''
    simple 1 layer network
'''
from __future__ import division, print_function, absolute_import

import numpy
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d


def analyze(onehot_training_labels, onehot_test_labels, test_labels, training_labels, test_images,
            training_images, neural_net_type, band_list, tile_size, number_of_epochs, model):
    '''
      package data for tensorflow and analyze
    '''
    npy_training_images = numpy.array([img_loc_tuple[0] for img_loc_tuple in training_images])

    npy_test_images = numpy.array([img_loc_tuple[0] for img_loc_tuple in test_images])
    npy_training_labels = numpy.asarray(onehot_training_labels)
    npy_test_labels = numpy.asarray(onehot_test_labels)

    # normalize 0-255 values to 0-1
    train_images = npy_training_images.astype(numpy.float32)
    train_images = numpy.multiply(train_images, 1.0 / 255.0)
    test_images = npy_test_images.astype(numpy.float32)
    test_images = numpy.multiply(test_images, 1.0 / 255.0)

    if not model:
      on_band_count = 0
      for b in band_list:
          if b == 1:
              on_band_count += 1

      network = tflearn.input_data(shape=[None, tile_size, tile_size, on_band_count])
      if neural_net_type == 'one_layer_relu':
          network = tflearn.fully_connected(network, 2048, activation='relu')
      elif neural_net_type == 'one_layer_relu_conv':
          network = conv_2d(network, 256, 16, activation='relu')
          network = max_pool_2d(network, 3)
      else:
          print("ERROR: exiting, unknown layer type for neural net")

      # classify as road or not road
      softmax = tflearn.fully_connected(network, 2, activation='softmax')

      # based on parameters from www.cs.toronto.edu/~vmnih/docs/Mnih_Volodymyr_PhD_Thesis.pdf
      momentum = tflearn.optimizers.Momentum(
          learning_rate=.005, momentum=0.9,
          lr_decay=0.0002, name='Momentum')

      net = tflearn.regression(softmax, optimizer=momentum, loss='categorical_crossentropy')

      model = tflearn.DNN(net, tensorboard_verbose=0)
    else:
      model.fit(train_images,
                npy_training_labels,
                n_epoch=number_of_epochs,
                shuffle=False,
                validation_set=(npy_test_images, npy_test_labels),
                show_metric=True,
                run_id='mlp')

    return model

    # batch predictions on the test image set, to avoid a memory spike
    '''
    all_predictions = []
    for x in range(0, len(test_images) - 100, 100):
        for p in model.predict(test_images[x:x + 100]):
            all_predictions.append(p)

    for p in model.predict(test_images[len(all_predictions):]):
        all_predictions.append(p)
    assert len(all_predictions) == len(test_images)

    return all_predictions
    '''
