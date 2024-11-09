import torchvision.models as models
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
import numpy as np

# imagenet normalize
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
scaler = transforms.Resize((224, 224))
to_tensor = transforms.ToTensor()


class ResNet18:
    def __init__(self):
        print("Initializing ResNet")
        self.model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        self.feature_layer = self.model._modules.get("avgpool")
        self.model.eval()

    def extract_feature(self, img):
        img = Variable(normalize(to_tensor(scaler(img))).unsqueeze(0))
        embedding = torch.zeros(512)

        def hook(m, i, o):
            feature_data = o.data.reshape((512))
            embedding.copy_(feature_data)

        h = self.feature_layer.register_forward_hook(hook)
        self.model(img)
        h.remove()
        embedding_fp16 = np.array(embedding.numpy(), dtype=np.float16)
        return embedding_fp16


def initialize(param):
    global resnet18
    resnet18 = ResNet18()


def run(image_obj):
    image = image_obj["image"]
    image = image.convert("RGB")
    image_vec = resnet18.extract_feature(image)
    return image_vec


# if __name__ == "__main__":
#     initialize(param=None)
#     image_path = r"sample_data/text.png"
#     from PIL import Image
#     image = Image.open(image_path)
#     example_image_obj = {"image": image}
#     result = run(example_image_obj)
#     print(len(result))
