import numpy as np
import json

list_labels_names = json.load(open('src/utils/search_with_image/classification.json'))


def get_postprocessing_name(output_model):
    max_index = np.argmax(output_model)
    max_name = list_labels_names[max_index]
    return max_name

# def result_info_fashion(result_model):
#     dict_result = {
#         "T-shirt/top": result_model[0],
#         "Trouser": result_model[1],
#         "Pullover": result_model[2],
#         "Dress": result_model[3],
#         "Coat": result_model[4],
#         "Sandal": result_model[5],
#         "Shirt": result_model[6],
#         "Sneaker": result_model[7],
#         "Bag": result_model[8],
#         "Ankle boot": result_model[9],
#         "Hat": result_model[10]
#     }
#     return dict_result

# def result_info_fashion_highest(result_model):
#     index = np.argmax(result_model)
#     class_name = list_labels_names[index]
#     class_score = result_model[index]
#     return class_name, class_score

