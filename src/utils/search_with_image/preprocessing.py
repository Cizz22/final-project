import torchvision.transforms as T
import torch
import cv2 as cv
from .RealESRGAN import RealESRGAN
from PIL import Image
from .init import init_supres

device = torch.device('cpu')

def preprocessing_std(img_path):
    preprocess=T.Compose([
            T.Resize(224),
            T.CenterCrop(size=224),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406],
                                [0.229, 0.224, 0.225])
        ])
    return preprocess(img_path)

def grayscaling(img_path):
    img = cv.bitwise_not(img_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(gray, cv.COLOR_GRAY2RGB)

    return img
