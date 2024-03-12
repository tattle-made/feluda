import unittest

# from unittest.case import skip
from core.operators import image_vec_rep_resnet
from core.models.media_factory import ImageFactory


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

    # @skip
    def test_sample_image_from_disk(self):
        image_path = r"core/operators/sample_data/text.png"
        image_obj = ImageFactory.make_from_file_on_disk(image_path)
        image_vec = image_vec_rep_resnet.run(image_obj)
        print(len(image_vec))
        self.assertEqual(len(image_vec), 512)

    # @skip
    def test_sample_image_from_url(self):
        image_obj = ImageFactory.make_from_url(
            "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        )
        image_vec = image_vec_rep_resnet.run(image_obj)
        print(len(image_vec))
        self.assertEqual(len(image_vec), 512)
