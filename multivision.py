import io
import os
import google
import cv2

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

def detect_labels_uri(path):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

detect_labels_uri('./Images/chicken.jpg')