import unittest
from . import image_phash
from dtypes.image import make_from_url, make_from_file


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        image_phash.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_image_from_disk(self):
        image = make_from_file("sample_data/image-with-text.jpg")
        image_hash = image_phash.run(image)
        self.assertEqual(image_hash, "ffff000001a1ffff")

    def test_sample_image_from_url(self):
        image = make_from_url(
            "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        )
        image_hash = image_phash.run(image)
        self.assertEqual(image_hash, "3c3c7e00183c0010")
