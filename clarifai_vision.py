import io
import json

#python3 -m pip install clarifai
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as CImage

def post(imagePath):

    f = open("./Keys/key_clarifai.txt","r")
    key = f.readline()
    f.close()

    # - `CLARIFAI_API_KEY`
    app = ClarifaiApp(api_key=key)


    model = app.models.get('food-items-v1.0')
    image = CImage(file_obj=open(imagePath, 'rb'))

    #output this to JSON
    with open ('./output_data/results.json', 'w') as f:
        json.dump(model.predict([image]),f)


def process():

    #Get and append JSON data
    with open('./output_data/results.json') as results:
        data = json.load(results)

    mealArr = []
    mealDict = {}
    
    #Get top 10 ingredients, return those with threshold > 82.5%
    for i in range(10):
        
        if data["outputs"][0]["data"]["concepts"][i]["value"]>0.825:
            mealArr.append(data["outputs"][0]["data"]["concepts"][i]["name"])
            mealDict.update({data["outputs"][0]["data"]["concepts"][i]["name"]:i})

    #Need to remove general words.
    words = ""
    f = open("./data/foodWords.txt","r")
    for line in f:
        words = words + line
    f.close()

    wordsArr = words.split("\n")
    
    A = set(mealDict)
    B = set(wordsArr)

    relevantFood = list(A.difference(B))

    #temporary O(n^2) algorithm

    foodList = [0,0,0,0,0,0,0,0,0,0]

    for i in range(len(relevantFood)):
        for food, index in mealDict.items():
            if relevantFood[i] == food:
                foodList[index] = food
    

    foodList = [value for value in foodList if value != 0]
    foodOutput = ' '.join(foodList)
    return foodOutput