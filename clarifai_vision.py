import io
import json

#python3 -m pip install clarifai
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as CImage

def post(img_path):
    f = open("key_clarifai.txt","r")
    key = f.readline()

    # - `CLARIFAI_API_KEY`
    app = ClarifaiApp(api_key=key)


    model = app.models.get('food-items-v1.0')
    image = CImage(url=img_path)

    #output this to JSON
    with open ('./output_data/results.json', 'w') as f:
        json.dump(model.predict([image]),f)