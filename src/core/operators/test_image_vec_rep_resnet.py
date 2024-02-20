import unittest
from unittest.case import skip
import image_vec_rep_resnet
# from dtypes.image import make_from_url, make_from_file
from PIL import Image


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        image_vec_rep_resnet.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    def test_sample_image_from_disk(self):
        image = Image.open(r'sample_data/text.png')
        image_obj = {"image": image}
        image_vec = image_vec_rep_resnet.run(image_obj)
        self.assertEqual(len(image_vec), 512)

    @skip
    def test_sample_image_from_url(self):
        image = make_from_url(
            "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        )
        image_vec = image_vec_rep_resnet.run(image)
        self.assertEqual(len(image_vec), 512)
