import torch
# import numpy as np
# import torchvision.transforms as T
from PIL import Image
import cv2 as cv
# import json
# import requests
# import io
import base64

#file from other module
from .init import init_model
from .preprocessing import grayscaling
from .inference import get_result, upnoscale
from .postprocessing import get_postprocessing_name

#############################################################################################

def ai_pipeline(model_inf, img_path, image_path):
    img = grayscaling(img_path)

    image_tensor  = upnoscale(img_path = img, image_path=image_path)

    image_tensor.resize_(1, 3, 224, 224)

    output_numpy = get_result(image= image_tensor, model_inf=model_inf)

    highest = get_postprocessing_name(output_model=output_numpy)

    return highest

def search_img(img_str):
    
    img_data = bytes(img_str, 'utf-8')
    with open("static/image/imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(img_data))

    #model initialization

    # image_base64 = requests.data["image64"]

    # converting from base64 to image cv
    # base64 processing to cv image
    # reconstruct image as an numpy array
    # image64_decode = cv.imread(io.BytesIO(base64.b64decode(image_base64)))

    # # finally convert RGB image to BGR for opencv
    # # and save result
    # image_cv = cv.cvtColor(image64_decode, cv.COLOR_RGB2BGR) 

    device = torch.device('cpu')
    #initial model
    path_model = "src/utils/search_with_image/weight/resnet18_custom_11_class_fix1.pth" #changed everytime maybe
    inf_model = init_model(model_path = path_model , device = device)

    #preprocessing 
    image_path = "static/image/imageToSave.png"
    img_cv = cv.imread(image_path)

    #requests from API
    highest = ai_pipeline(model_inf = inf_model, img_path = img_cv, 
                        image_path = image_path)

    return highest

    # # for API
    # response = {
    #     "classification_name": result_name,
    #     "classification_score": result_score
    # }
