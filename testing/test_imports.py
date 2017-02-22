#!/usr/bin/env python
import unittest


class TestImports(unittest.TestCase):

    def test_import_boto3(self):
        import boto3
        print boto3

    def test_import_numpy(self):
        import numpy
        print numpy

    def test_import_osmium(self):
        import osmium
        print osmium

    def test_import_requests(self):
        import requests
        print requests

    def test_import_shapely(self):
        import shapely
        print shapely

    def test_import_tensorflow(self):
        import tensorflow
        print tensorflow

    def test_import_tflearn(self):
        import tflearn
        print tflearn


if __name__ == "__main__":
    unittest.main()
