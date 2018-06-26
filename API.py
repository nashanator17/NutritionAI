# import requests
# import json
# #
# url = "https://api.edamam.com/api/food-database/parser?ingr=ruffles%20all%20dressed&app_id=b354c614&app_key=f192339adb7c913344e77f7c4f4a65c0&page=1"
#
# result = requests.get(url)
# content = result.content
# data = json.loads(content)
# name = data["hints"]
# Example Call:
#python3 API.py --gender male --age 20 --weight 165 --height 170 --exercise light --restrictions no --weight_goal lose
import requests
import json
from pprint import pprint
import argparse
import customerInfo
import vision
from difflib import SequenceMatcher
import clarifai_vision

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def nutritionix(mainstring):
    urlify = mainstring.replace(' ',"%20")
    nutritionixURL1 = "https://trackapi.nutritionix.com/v2/search/instant?query=" + str(urlify)
    payload = {"timezone": "US/Eastern"}
    headers = {'content-type': 'application/json', 'x-app-id': '44a081cf', 'x-app-key': '412b1c16a680363f6c16c4eee2cfa2fa'}
    r1 = requests.get(nutritionixURL1, json=payload, headers=headers)
    nutDataGeneral = json.loads(r1.content)
    itemID = nutDataGeneral['branded'][0]['nix_item_id']
    nutritionixURL2 = "https://trackapi.nutritionix.com/v2/search/item?nix_item_id=" + str(itemID)
    r2 = requests.get(nutritionixURL2, json=payload, headers=headers)
    nutDataSpecific = json.loads(r2.content)
    servingWeightGrams = nutDataSpecific['foods'][0]["serving_weight_grams"]
    return servingWeightGrams

def argparser():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gender", required = True, help = "Enter your gender")
    ap.add_argument("--age", required = True, help = "Enter your age")
    ap.add_argument("--weight", required = True, help = "Enter your weight in pounds")
    ap.add_argument("--height", required = True, help = "Enter your height in centimeters")
    ap.add_argument("--exercise", required = True, help = "Enter your exercise level (low, light, moderate, heavy)")
    ap.add_argument("--restrictions", required = True, help = "Do you have any food restrictions? (yes or no)")
    ap.add_argument("--weight_goal", required = True, help = "Enter your weight goal?? (lose, maintain, gain)")
    args = vars(ap.parse_args())
    gender = args["gender"]
    height = float(args["height"])
    weight = float(args["weight"])
    age = float(args["age"])
    exerciseLevel = args["exercise"]
    restrictions = args["restrictions"]
    goal = args["weight_goal"]
    infoMap = {"gender": gender, "height": height, "weight": weight, "age": age, "exerciseLevel": exerciseLevel, "restrictions": restrictions, "goal": goal}
    return infoMap

def edamamGet(mainstring):
    urlify = mainstring.replace(' ',"%20")
    print("mainstring "+ str(urlify))
    url = "https://api.edamam.com/api/food-database/parser?ingr="+str(urlify)+"&app_id=b354c614&app_key=f192339adb7c913344e77f7c4f4a65c0&page=1"
    # print(url)
    #
    r = requests.get(url)
    print(mainstring)
    mainstring_set = mainstring.lower().split(" ")
    mainstring_set.sort()
    mainstring_format = ' '.join(mainstring_set)
    print(mainstring_format)
    return (mainstring_format, r)

def bestString(mainstring_format, r):
    bestPerc = 0
    bestMatch = ""
    bestFoodLabel = ""
    for food in r.json()["hints"]:
        food_label = food["food"]["label"]
        foodlabel_set = food_label.lower().split(" ")
        foodlabel_set.sort()
        foodlabel_format = ' '.join(foodlabel_set)
        perc = similar(foodlabel_format, mainstring_format)
        print(str(perc) + " " + foodlabel_format)
        if perc > bestPerc:
            bestPerc = perc
            bestMatch = food["food"]["uri"]
            bestFoodLabel = food_label
    #measure_uri = r.json()["hints"][0]["measures"][0]["uri"]
    print(str(bestFoodLabel))
    return bestMatch

def edamamPost(bestMatch):
    measure_uri = "http://www.edamam.com/ontologies/edamam.owl#Measure_kilogram"
    #print(str(food_uri))
    payload = {"yield": 1,"ingredients": [{"quantity": 1,"measureURI": measure_uri,"foodURI": bestMatch}]}
    url2 = "https://api.edamam.com/api/food-database/nutrients?app_id=b354c614&app_key=f192339adb7c913344e77f7c4f4a65c0"
    r2 = requests.post(url2, json=payload)
    content = r2.content
    data = json.loads(content)
    return data

def getNutrition(data, servingSize):
    foodCalories = data["calories"]
    foodCalories = foodCalories*servingSize
    foodCalories = foodCalories/1000
    #print(data["totalNutrients"]["PROCNT"])
    if "PROCNT" not in data["totalNutrients"].keys():
        foodProtein =  0
    else :
        foodProtein = data["totalNutrients"]["PROCNT"]["quantity"]
        foodProtein = foodProtein*servingSize
        foodProtein = foodProtein/1000

    if "FAT" not in data["totalNutrients"].keys():
        foodFat =  0
    else :
        foodFat = data["totalNutrients"]["FAT"]["quantity"]
        foodFat = foodFat*servingSize
        foodFat = foodFat/1000
    if "CHOCDF" not in data["totalNutrients"].keys():
        foodCarbs =  0
    else :
        foodCarbs = data["totalNutrients"]["CHOCDF"]["quantity"]
        foodCarbs = foodCarbs*servingSize
        foodCarbs = foodCarbs/1000
    nutritionMap = {"foodCalories":foodCalories, "foodProtein":foodProtein, "foodFat":foodFat, "foodCarbs":foodCarbs}
    return nutritionMap

def analyze(nutritionMap, customerData):
    cal_perc = nutritionMap["foodCalories"] / customerData["calories"] * 100
    pro_perc = nutritionMap["foodProtein"] / customerData["protein"] * 100
    fat_perc = nutritionMap["foodFat"] / customerData["fat"] * 100
    carb_perc = nutritionMap["foodCarbs"] / customerData["carbs"] * 100
    percMap = {"cal_perc":cal_perc, "pro_perc":pro_perc, "fat_perc":fat_perc, "carb_perc":carb_perc}
    return percMap

def display(percMap, customerData, servingSize, nutritionMap, warnings):
    print("Serving Size: " + str(servingSize) + "g")
    print("Calories: " + str(percMap["cal_perc"]) + "%" + "   " + str(nutritionMap["foodCalories"]) + "/" + str(customerData["calories"]))
    print("Protein: " + str(percMap["pro_perc"]) + "%" + "   " + str(nutritionMap["foodProtein"]) + "/" + str(customerData["protein"]))
    print("Fat: " + str(percMap["fat_perc"]) + "%" + "   " + str(nutritionMap["foodFat"]) + "/" + str(customerData["fat"]))
    print("Carbohydrates: " + str(percMap["carb_perc"]) + "%" + "   " + str(nutritionMap["foodCarbs"]) + "/" + str(customerData["carbs"]))
    print("WARNING! CONTAINS: " + warnings)

def clarifai(imagePath):
    clarifai_vision.post(imagePath)
    resultSet = clarifai_vision.process().split(" ")
    #LOOP THROUGH AND GET NUTRITION FOR EACH AND SUM UP

def getRestrictions(data, customerData):
    warnings = ""
    healthLabels = ""
    cautions = ""
    for x in data["healthLabels"]:
        healthLabels += str(x) + " "
    print("healthLabels" + healthLabels)
    for x in data["cautions"]:
        cautions += str(x) + " "
    print("cautions" + cautions)
    for restriction in customerData["restrictions"]:
        # restriction = restriction.upper()
        print(restriction)
        if restriction.upper() in cautions or (restriction.upper()+"_FREE") in healthLabels:
            warnings += str(restriction) + " "
    return warnings



def main():
    customerData = customerInfo.calculate(argparser())

    # get user input to scan barcode or label
    while(True):
        vision_option = input("type 'b' to scan barcode or 'l' to read item label: ")
        if(vision_option != 'b' and vision_option != 'l'):
            print("Must type 'b' or 'l")
            continue
        else:
            break
    mainstring = vision.run(vision_option)
    getResult = edamamGet(mainstring)
    mainstring_format = getResult[0]
    r = getResult[1]
    servingSize = nutritionix(mainstring_format)
    # bestMatch = bestString(mainstring_format, r)
    data = edamamPost(mainstring_format)
    nutritionMap = getNutrition(data, servingSize)
    warnings = getRestrictions(data, customerData)
    percMap = analyze(nutritionMap, customerData)
    display(percMap, customerData, servingSize, nutritionMap, warnings)
<<<<<<< HEAD

=======
>>>>>>> 4fe12015fb167d78ceaf3df2e5b9eddba822b74f


<<<<<<< HEAD

#
=======
main()
>>>>>>> 4fe12015fb167d78ceaf3df2e5b9eddba822b74f
