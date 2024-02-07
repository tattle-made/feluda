from PIL import Image
from core.operators import image_vec_rep_resnet


def profile_code():
    image_vec_rep_resnet.initialize(param=None)
    image_path = r"core/operators/sample_data/text.png"
    image = Image.open(image_path)
    example_image_obj = {"image": image}
    image_vec_rep_resnet.run(example_image_obj)
    print("Image vec profiler complete!")


if __name__ == "__main__":
    profile_code()
