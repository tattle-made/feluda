import unittest
from core.feluda import Feluda
from core.models.media_factory import ImageFactory


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Intializing Feluda
        cls.feluda = Feluda('image_vec_rep_resnet-config.yaml')
        cls.feluda.setup()

    @classmethod
    def tearDownClass(cls):
        # Clean up resources if needed
        pass

    @skip
    def test_sample_image_from_disk(self):
        image_path = r"core/operators/sample_data/text.png"
        image_obj = ImageFactory.make_from_file_on_disk(image_path)
        operator = self.feluda.operators.get()["image_vec_rep_resnet"]
        image_vec = operator.run(image_obj)
        print(len(image_vec))
        self.assertEqual(len(image_vec), 512)

    def test_sample_image_from_url(self):
        image_obj = ImageFactory.make_from_url(
            "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png"
        )
        operator = self.feluda.operators.get()["image_vec_rep_resnet"]
        image_vec = operator.run(image_obj)
        print(len(image_vec))
        self.assertEqual(len(image_vec), 512)

