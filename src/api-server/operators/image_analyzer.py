from io import BytesIO
import torchvision.models as models
import torch
import torchvision.transforms as transforms
from torch.autograd import Variable
import numpy as np
import requests
import PIL
from monitor import timeit


# imagenet normalize
normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
scaler = transforms.Resize((224, 224))
to_tensor = transforms.ToTensor()


@timeit
def image_from_url(image_url):
    resp = requests.get(image_url)
    image_bytes = resp.content
    image = PIL.Image.open(BytesIO(image_bytes))
    image_array = np.array(image)
    return {"image": image, "image_array": image_array, "image_bytes": image_bytes}


class ResNet18:
    def __init__(self):
        print("Initializing ResNet")
        self.model = models.resnet18(pretrained=True)
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
