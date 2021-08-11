import json

import utils
import numpy as np

def classify_image(image, model):
    prediction = model(np.array([image]), training=False)
    label = np.argmax(prediction)
    return prediction, label

def get_model_label():
    model = utils.get_model()
    model.build(input_shape=(None, 224, 224, 3))
    model.load_weights("static/EfficientNetB4_Pretrain_Tricks.h5")

    with open('static/label_to_content.json', 'r') as f:
        label_to_content = f.readline()
        label_to_content = json.loads(label_to_content)

    return model, label_to_content