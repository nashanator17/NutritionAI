# import requests
# import json
# #
# url = "https://api.edamam.com/api/food-database/parser?ingr=ruffles%20all%20dressed&app_id=b354c614&app_key=f192339adb7c913344e77f7c4f4a65c0&page=1"
#
# result = requests.get(url)
# content = result.content
# data = json.loads(content)
# name = data["hints"]
#
import requests
import json
from pprint import pprint
import argparse
import customerInfo
import vision
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def nutritionix(query):
    nutritionixURL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    payload = {"query":str(query), "timezone": "US/Eastern"}
    headers = {'content-type': 'application/json', 'x-app-id': '44a081cf', 'x-app-key': '412b1c16a680363f6c16c4eee2cfa2fa'}
    r2 = requests.post(nutritionixURL, json=payload, headers=headers)
    content = r2.content
    nutData = json.loads(content)
    print(nutData)
    servingWeightGrams = nutData['foods'][0]["serving_weight_grams"]
    return servingWeightGrams

ap = argparse.ArgumentParser()
ap.add_argument("--gender", required = True, help = "Enter your gender")
ap.add_argument("--age", required = True, help = "Enter your age")
ap.add_argument("--weight", required = True, help = "Enter your weight in pounds")
ap.add_argument("--height", required = True, help = "Enter your height in centimeters")
ap.add_argument("--exercise", required = True, help = "Enter your exercise level (low, light, moderate, heavy)")
args = vars(ap.parse_args())
gender = args["gender"]
height = float(args["height"])
weight = float(args["weight"])
age = float(args["age"])
exerciseLevel = args["exercise"]
customerData = customerInfo.calculate(gender, age, weight, height, exerciseLevel)
healthLabels = set()

mainstring = vision.run()
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
#print(r.text)
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
nutritionixAPI = nutritionix(mainstring_format)
measure_uri = "http://www.edamam.com/ontologies/edamam.owl#Measure_kilogram"
#print(str(food_uri))
payload = {"yield": 1,"ingredients": [{"quantity": 1,"measureURI": measure_uri,"foodURI": bestMatch}]}
url2 = "https://api.edamam.com/api/food-database/nutrients?app_id=b354c614&app_key=f192339adb7c913344e77f7c4f4a65c0"
r2 = requests.post(url2, json=payload)
content = r2.content
data = json.loads(content)
foodCalories = data["calories"]
#print(data["totalNutrients"]["PROCNT"])
if "PROCNT" not in data["totalNutrients"].keys():
    foodProtein =  0
else :
    foodProtein = data["totalNutrients"]["PROCNT"]["quantity"]
    foodProtein = foodProtein*nutritionixAPI
    foodProtein = foodProtein/1000

if "FAT" not in data["totalNutrients"].keys():
    foodFat =  0
else :
    foodFat = data["totalNutrients"]["FAT"]["quantity"]
    foodFat = foodFat*nutritionixAPI
    foodFat = foodFat/1000
if "CHOCDF" not in data["totalNutrients"].keys():
    foodCarbs =  0
else :
    foodCarbs = data["totalNutrients"]["CHOCDF"]["quantity"]
    foodCarbs = foodCarbs*nutritionixAPI
    foodCarbs = foodCarbs/1000
#carbs = str(data["totalNutrients"]["CHOCDF"]["quantity"])+" "+str(data["totalNutrients"]["FAT"]["unit"])
for x in data["healthLabels"]:
    healthLabels.add(x)
cal_perc = foodCalories / customerData["calories"] * 100
pro_perc = foodProtein / customerData["protein"] * 100
fat_perc = foodFat / customerData["fat"] * 100
carb_perc = foodCarbs / customerData["carbs"] * 100
print("Serving Size: " + str(nutritionixAPI) + "g")
print("Calories: " + str(cal_perc) + "%" + "   " + str(foodCalories) + "/" + str(customerData["calories"]))
print("Protein: " + str(pro_perc) + "%" + "   " + str(foodProtein) + "/" + str(customerData["protein"]))
print("Fat: " + str(fat_perc) + "%" + "   " + str(foodFat) + "/" + str(customerData["fat"]))
print("Carbohydrates: " + str(carb_perc) + "%" + "   " + str(foodCarbs) + "/" + str(customerData["carbs"]))
#print(healthLabels)
#print(str(calories)+ " "+str(fats))
#
#
