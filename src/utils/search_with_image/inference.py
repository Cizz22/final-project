import torch
from PIL import Image
from .init import init_supres
from .preprocessing import grayscaling, preprocessing_std
device = torch.device('cpu')

def upnoscale(img_path, image_path):
       
    if img_path.any() != None:
        if(len(img_path)>=224):
            print('This image is big downscaling')
            img = Image.fromarray(img_path)
            image_tensor = preprocessing_std(img)

        elif len(img_path)>28 & len(img_path) < 150 :
            print('I think this image not big enough, upscaling')
            img = Image.open(image_path).convert('RGB')
            sr_mod = init_supres().predict(img)
            image_tensor = preprocessing_std(sr_mod)

        elif len(img_path)<=50:
            print('Image is small, let upscale 2 times')
            img = Image.open(image_path).convert('RGB')
            sr_mod = init_supres().predict(img)
            sr_mod2 = init_supres().predict(sr_mod)
            image_tensor = preprocessing_std(sr_mod2)

    else:
        print("cannot find image")

    return image_tensor

def get_result(image, model_inf):
    output_tensor = model_inf(image)
    output_numpy = output_tensor.detach().numpy()

    return output_numpy