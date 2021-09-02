import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras.applications.efficientnet import EfficientNetB4


def get_model():
    modelPre = EfficientNetB4(
        weights='imagenet',
        include_top=False,
        input_shape=(224, 224, 3),
        classes=40
    )
    model = tf.keras.Sequential()
    model.add(modelPre)
    model.add(tf.keras.layers.GlobalAveragePooling2D())
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(40, name='fully_connected', activation='softmax', use_bias=False))

    return model


def load_image(image_path):
    image = cv2.imread(image_path).astype(np.float32)

    image = random_size(image, target_size=224)
    image = normalize(image)

    return image


def random_size(image, target_size=None):
    height, width, _ = np.shape(image)
    size_ratio_height = target_size / height
    size_ratio_width = target_size / width
    resize_shape = (int(width * size_ratio_width), int(height * size_ratio_height))
    return cv2.resize(image, resize_shape)


def normalize(image):
    mean = [103.939, 116.779, 123.68]
    std = [58.393, 57.12, 57.375]
    for i in range(3):
        image[..., i] = (image[..., i] - mean[i]) / std[i]
    return image
