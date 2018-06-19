import io
import os
import google
import cv2

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

#call process_image to get a returned string containing what you want

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

def format_text(text):
    print("format input" + text)
    stripNewLine = text.replace('\n', " ")
    finalString = stripNewLine.replace('"',"")
    # print (finalString)
    # print ('\n')

    words = finalString.split()
    final = " ".join(sorted(set(words), key=words.index))
    # print (final)

    #print (result)

    return final
    # file = open('result.txt','w')
    # file.write(result)
    # file.close()

def run():
    img_name = process_image()
    parsed = detect_text(img_name)
    result = format_text(parsed)
    return result
