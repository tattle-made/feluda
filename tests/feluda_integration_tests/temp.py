from feluda import Feluda
from feluda.models.media_factory import ImageFactory
from operators.image_vec_rep_resnet import image_vec_rep_resnet

feluda = Feluda(r"tests/feluda_integration_tests/01_config.yml")
feluda.setup()

image_obj = ImageFactory.make_from_url("https://tattle-media.s3.amazonaws.com/test-data/tattle-search/text-in-image-test-hindi.png")
image_vec = image_vec_rep_resnet.run(image_obj)
print(len(image_vec))
