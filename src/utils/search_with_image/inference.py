import torch
from PIL import Image
from .init import init_supres
from .preprocessing import grayscaling, preprocessing_std
device = torch.device('cpu')

def upnoscale(img_path, image_path):
       
    if img_path.any() != None:
        if(len(img_path)>=256):
            img = Image.fromarray(img_path)
            image_tensor = preprocessing_std(img)

        elif len(img_path)<224:
            # model = RealESRGAN(device, scale=4)
            # model.load_weights('weight/RealESRGAN_x4plus.pth')
            img = Image.open(image_path).convert('RGB')
            sr_mod = init_supres.predict(img_path)
            image_tensor = preprocessing_std(img_path=sr_mod)

    else:
        print("cannot find image")

    return image_tensor

def get_result(image, model_inf):
    output_tensor = model_inf(image)
    output_numpy = output_tensor.detach().numpy()

    return output_numpy