import io
import os
import google
import cv2
import barcode
from PIL import Image
import time

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

#call process_image to get a returned string containing what you want
#export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations #Print this to view returned data

    parsed = {}
    resultString = ""

    for text in texts:
        #parsed += ('\n"{}"'.format(text.description))
        area = ((text.bounding_poly.vertices[2].x - text.bounding_poly.vertices[0].x) * (text.bounding_poly.vertices[2].y - text.bounding_poly.vertices[0].y))
        temp = {area:text.description}
        parsed.update(temp)
        # print(text.bounding_poly.vertices[0].x)

    # print (format_text(parsed))
    keylist = sorted(parsed)
    keylist = list(reversed(keylist))
    limit = 1
    for key in keylist:
        if limit != 1:
            resultString += str(parsed[key]) + " "
        limit+=1
        if (limit > 6):
            break

    print("vision " + resultString)
    return resultString

def process_image():

    img_counter = 0
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    while(True):
        ret, frame = cam.read()
        cv2.imshow("test",frame)

        k = cv2.waitKey(1)

        if k%256 == 27:
            print("Escape hit, closing...")
            break

        elif k%256 == 32:

            img_name = "opencv_frame_{}.jpg".format(img_counter)
            img_counter = img_counter + 1
            cv2.imwrite(img_name,frame)
            print("image taken, processing results...")
            # Instantiates a client
            client = vision.ImageAnnotatorClient()
            return img_name


    cam.release()
    cv2.destroyAllWindows()

def process_image_barcode():

    img_counter = 0
    cam = cv2.VideoCapture(0)
    cam.set(6,24)
    cv2.namedWindow("test")

    while(True):
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        cv2.rectangle(frame,(500,250),(900,500),(255,0,0),3)
        cv2.imshow("test",frame)
        img_name = "latest.jpg"
        roi = frame[250:500, 500:900]
        roi = cv2.flip(roi, 1)
        lab= cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        roi = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        cv2_im = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        cv2.waitKey(1)
        product_barcode = barcode.get_barcode(pil_im)
        if product_barcode is not None:
            #cv2.imshow("contrast",cv2_im)
            #cv2.waitKey(0)
            print("found")
            cv2.rectangle(frame,(500,250),(900,500),(0,255,0),3)
            cv2.imshow("test",frame)
            cv2.waitKey(10)
            time.sleep(1)
            cam.release()
            cv2.destroyAllWindows()
            client = vision.ImageAnnotatorClient()
            return product_barcode


def format_text(text):
    print("format input" + text)
    stripNewLine = text.replace('\n', " ")
    finalString = stripNewLine.replace('"',"")

    words = finalString.split()
    final = " ".join(sorted(set(words), key=words.index))

    return final


def run(vision_option):
    if(vision_option == 'b'):
        product_barcode = process_image_barcode()
        product_name = barcode.product_from_barcode(product_barcode)
    else:
        img_name = process_image()
        product_name = detect_text(img_name)
    result = format_text(product_name)
    return result
