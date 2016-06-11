#!/usr/bin/env python

"""Post test results to S3."""

import argparse


def main():
    """Post test results to an S3 bucket."""
    with open(CACHE_PATH + 'raster_data_paths.pickle', 'r') as infile:
        raster_data_paths = pickle.load(infile)

    with open(CACHE_PATH + METADATA_PATH, 'r') as infile:
        training_info = pickle.load(infile)

    with open(CACHE_PATH + 'model.pickle', 'r') as outfile:
        model = pickle.load(outfile)

    if post_findings_to_s3:
        post_findings_to_s3(raster_data_paths, model, training_info, args.render_results,
                            training_info['naip_state'])


if __name__ == "__main__":
    main()
