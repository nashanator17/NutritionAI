#
# Pip install the client:
# pip install clarifai
#

# The package will be accessible by importing clarifai:

import io
import json

from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as CImage

# The client takes the `API_KEY` you created in your Clarifai
# account. You can set these variables in your environment as:

f = open("key_clarifai.txt","r")
key = f.readline()

# - `CLARIFAI_API_KEY`
app = ClarifaiApp(api_key=key)


model = app.models.get('food-items-v1.0')
image = CImage(url='https://samples.clarifai.com/food.jpg')

#output this to JSON
print(model.predict([image]))