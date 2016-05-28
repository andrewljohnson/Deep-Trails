#!/usr/bin/env python

"""Train a neural network using OpenStreetMap labels and NAIP images."""

import argparse
import pickle

# src.training_visualization must be included before src.single_layer_network,
# in order to import PIL before TFLearn - or PIL errors tryig to save a JPEG
from src.training_visualization import render_results_for_analysis
from src.single_layer_network import train_on_cached_data, predictions_for_tiles, list_findings
from src.training_data import CACHE_PATH, tag_with_locations, load_training_tiles


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
    parser.add_argument("--list-findings",
                        action='store_true',
                        help="list the most likely false negatives/positives in the OSM data")
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
    test_images, model = train_on_cached_data(raster_data_paths, args.neural_net, args.bands,
                                              args.tile_size, args.number_of_epochs)
    if args.list_findings:
        for path in raster_data_paths:
            labels, images = load_training_tiles(path)
            if len(labels) == 0 or len(images) == 0:
                print("WARNING, there is a borked naip image file")
                continue
            false_positives, false_negatives, fp_images, fn_images = list_findings(labels, images, model)
            path_parts = path.split('/')
            filename = path_parts[len(path_parts) - 1]
            print("FINDINGS: {} false pos and {} false neg, of {} tiles, from {}".format(
                len(false_positives), len(false_negatives), len(images), filename))
            tag_with_locations([], [], args.tile_size)
            # tag_with_locations(test_images, predictions, tile_size):
            # [false_positives.append(x) for x in false_negatives]
            render_results_for_analysis(raster_data_paths, false_positives, fp_images, args.bands,
                                        args.tile_size)
            #render_results_for_analysis(raster_data_paths, false_negatives, fn_images, args.bands,
            #                            args.tile_size)

    if args.render_results:
        predictions = predictions_for_tiles(test_images, model)
        render_results_for_analysis(raster_data_paths, predictions, test_images, args.bands,
                                    args.tile_size)


if __name__ == "__main__":
    main()
