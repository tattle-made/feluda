from feluda.feluda import Feluda
from feluda.models.media_factory import ImageFactory

fel = Feluda(r"test-config.yaml")
fel.setup()

image_loc = r'/home/aatman/Downloads/text-in-image-test-hindi.png'
image_obj = ImageFactory.make_from_file_on_disk(image_loc)
operator = fel.operators.get()["image_vec_rep_resnet"]
image_vec = operator.run(image_obj)
print(len(image_vec))