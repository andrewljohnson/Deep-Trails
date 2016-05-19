#!/usr/bin/env python

"""Train a neural network using OpenStreetMap labels and NAIP images."""

import argparse
import pickle

from src.single_layer_network import train_with_data, predictions_for_tiles
from src.training_data import CACHE_PATH, load_training_tiles, equalize_data, split_train_test, \
    format_as_onehot_arrays, shuffle_in_unison
from src.training_visualization import render_results_for_analysis


def create_parser():
    """Create the argparse parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--tile-size",
                        default=64,
                        type=int,
                        help="tile the NAIP and training data into NxN tiles with this dimension")
    parser.add_argument("--bands",
                        default=[0, 0, 0, 1],
                        nargs=4,
                        type=int,
                        help="specify which bands to activate (R  G  B  IR). default is "
                        "--bands 0 0 0 1 (which activates only the IR band)")
    parser.add_argument("--render-results",
                        action='store_true',
                        help="output data/predictions to JPEG")
    parser.add_argument("--number-of-epochs",
                        default=100,
                        type=int,
                        help="the number of epochs to batch the training data into")
    parser.add_argument("--neural-net",
                        default='one_layer_relu',
                        choices=['one_layer_relu', 'one_layer_relu_conv'],
                        help="the neural network architecture to use")
    return parser


def main():
    """Use local data to train the neural net, probably made by bin/create_training_data.py."""
    parser = create_parser()
    args = parser.parse_args()

    with open(CACHE_PATH + 'raster_data_paths.pickle', 'r') as infile:
        raster_data_paths = pickle.load(infile)

    training_images = []
    onehot_training_labels = []

    test_images = []
    onehot_test_labels = []
    model = None

    epoch = 0

    for path in raster_data_paths:
        # keep test list to 1000 images
        if len(test_images) > 1000:
            test_images = test_images[:900]
            onehot_test_labels = onehot_test_labels[:900]

        # keep train list to 10000 images
        if len(training_images) > 10000:
            training_images = training_images[:9000]
            onehot_training_labels = onehot_training_labels[:9000]

        # read in another NAIP worth of data
        labels, images = load_training_tiles(path)
        equal_count_way_list, equal_count_tile_list = equalize_data(labels, images, False)
        new_test_labels, training_labels, new_test_images, new_training_images = \
            split_train_test(equal_count_tile_list, equal_count_way_list, .9)
        if len(training_labels) == 0:
            print("WARNING: a naip image didn't have any road labels?")
            continue

        # add it to the training and test lists
        [training_images.append(i) for i in new_training_images]
        [test_images.append(i) for i in new_test_images]
        [onehot_training_labels.append(l) for l in format_as_onehot_arrays(training_labels)]
        [onehot_test_labels.append(l) for l in format_as_onehot_arrays(new_test_labels)]

        # shuffle it so when we chop off data it's from many NAIPs, not just the last one
        shuffle_in_unison(training_images, onehot_training_labels)
        shuffle_in_unison(test_images, onehot_test_labels)

        # continue training the model with the new data set
        model = train_with_data(onehot_training_labels, onehot_test_labels, test_images,
                                training_images, args.neural_net, args.bands, args.tile_size,
                                epoch, model)
        epoch += 1

    predictions = predictions_for_tiles(test_images, model)
    if args.render_results:
        render_results_for_analysis(raster_data_paths, predictions, test_images, args.band_list,
                                    args.tile_size)


if __name__ == "__main__":
    main()
