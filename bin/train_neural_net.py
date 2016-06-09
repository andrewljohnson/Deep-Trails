#!/usr/bin/env python

"""Train a neural network using OpenStreetMap labels and NAIP images."""

import argparse
import boto3
import pickle

# src.training_visualization must be included before src.single_layer_network,
# in order to import PIL before TFLearn - or PIL errors tryig to save a JPEG
from src.training_visualization import render_results_for_analysis
from src.single_layer_network import train_on_cached_data, predictions_for_tiles, list_findings
from src.training_data import CACHE_PATH, METADATA_PATH, load_training_tiles, tag_with_locations


def create_parser():
    """Create the argparse parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--render-results",
                        action='store_true',
                        help="output data/predictions to JPEG, in addition to normal JSON")
    parser.add_argument("--number-of-epochs",
                        default=5,
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

    with open(CACHE_PATH + METADATA_PATH, 'r') as infile:
        training_info = pickle.load(infile)

    test_images, model = train_on_cached_data(raster_data_paths, args.neural_net, 
                                              training_info['bands'], training_info['tile_size'], 
                                              args.number_of_epochs)
    findings = []
    for path in raster_data_paths:
        labels, images = load_training_tiles(path)
        if len(labels) == 0 or len(images) == 0:
            print("WARNING, there is a borked naip image file")
            continue
        false_positives, false_negatives, fp_images, fn_images = list_findings(labels, images,
                                                                               model)
        path_parts = path.split('/')
        filename = path_parts[len(path_parts) - 1]
        print("FINDINGS: {} false pos and {} false neg, of {} tiles, from {}".format(
            len(false_positives), len(false_negatives), len(images), filename))
        if args.render_results:
            # render JPEGs showing findings
            render_results_for_analysis([path], false_positives, fp_images, training_info['bands'],
                                    training_info['tile_size'])

        # combine findings for all NAIP images analyzedfor the region
        [findings.append(f) for f in tag_with_locations(fp_images, false_positives,
                                                        training_info['tile_size'])]

    # dump combined findings to disk as a pickle
    naip_path_in_cache_dir = training_info['naip_state'] + '/' + 'findings.pickle'
    local_path = CACHE_PATH + naip_path_in_cache_dir
    with open(local_path, 'w') as outfile:
        pickle.dump(findings, outfile)

    # push pickle to S3
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_path, 'deeposm', naip_path_in_cache_dir)


if __name__ == "__main__":
    main()
