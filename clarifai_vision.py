import io
import json

#python3 -m pip install clarifai
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as CImage

def post():

    f = open("./Keys/key_clarifai.txt","r")
    key = f.readline()
    f.close()

    # - `CLARIFAI_API_KEY`
    app = ClarifaiApp(api_key=key)


    model = app.models.get('food-items-v1.0')
    image = CImage(file_obj=open('./Images/waffles.jpg', 'rb'))

    #output this to JSON
    with open ('./output_data/results.json', 'w') as f:
        json.dump(model.predict([image]),f)


def process():

    #Get and append JSON data
    with open('./output_data/results.json') as results:
        data = json.load(results)

    mealArr = []
    #Get top 10 ingredients, return those with threshold > 85%
    for i in range(10):
        
        if data["outputs"][0]["data"]["concepts"][i]["value"]>0.825:
            mealArr.append(data["outputs"][0]["data"]["concepts"][i]["name"])

        # print (data["outputs"][0]["data"]["concepts"][i]["name"])
        # print (data["outputs"][0]["data"]["concepts"][i]["value"])

    print (mealArr)

    #Need to remove general words.
    words = ""
    f = open("foodWords.txt","r")
    for line in f:
        words = words + line
    f.close()

    wordsArr = words.split("\n")
    
    A = set(mealArr)
    B = set(wordsArr)

    print(list(A.difference(B)))




post()
process()