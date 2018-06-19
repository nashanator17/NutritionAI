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
ap = argparse.ArgumentParser()
ap.add_argument("--gender", required = True, help = "Enter your gender")
ap.add_argument("--age", required = True, help = "Enter your age")
ap.add_argument("--weight", required = True, help = "Enter your weight in pounds")
ap.add_argument("--height", required = True, help = "Enter your height in centimeters")
ap.add_argument("--exercise", required = True, help = "Enter your exercise level (low, light, moderate, heavy)")
args = vars(ap.parse_args())
gender = float(args["gender"])
height = float(args["height"])
weight = float(args["weight"])
age = float(args["age"])
exerciseLevel = args["exercise"]
customerData = customerInfo.calculate(age, weight, height, exerciseLevel)
healthLabels = set()
# Call placeholder methods
# Return json
#with open("ruffles.json") as f:
    #data = json.load(f)
#
# r1context = .content
# text = json.loads(r1content)
# mainstring = data["textAnnotations"][0]["description"]
# mainstring = mainstring.replace("\n","%20")
# mainstring = mainstring.replace("&amp","and")
# mainstring = mainstring.replace(" ","%20")
#print(mainstring)
#ingredient = "ruffles"
mainstring = vision.run()
urlify = mainstring.replace(' ',"%20")
print("mainstring "+ str(urlify))
url = "https://api.edamam.com/api/food-database/parser?ingr="+str(urlify)+"&app_id=b354c614&app_key=f192339adb7c913344e77f7c4f4a65c0&page=1"
# print(url)
#
r = requests.get(url)
print(mainstring)
mainstring_format = mainstring.split()[0]
print(brandName)
#print(r.text)
bestPerc = 0
bestMatch = ""
bestFoodLabel = ""
for food in r.json()["hints"]:
    food_label = food["food"]["label"]
    perc = similar(food_label.split()[0], brandName)
    print(str(perc) + " " + food_label.split()[0])
    if perc > bestPerc:
        bestPerc = perc
        bestMatch = food["food"]["uri"]
        bestFoodLabel = food_label
#measure_uri = r.json()["hints"][0]["measures"][0]["uri"]
print(str(bestFoodLabel))
measure_uri = "http://www.edamam.com/ontologies/edamam.owl#Measure_pound"
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
if "FAT" not in data["totalNutrients"].keys():
    foodFat =  0
else :
    foodFat = data["totalNutrients"]["FAT"]["quantity"]
if "CHOCDF" not in data["totalNutrients"].keys():
    foodCarbs =  0
else :
    foodCarbs = data["totalNutrients"]["CHOCDF"]["quantity"]
#carbs = str(data["totalNutrients"]["CHOCDF"]["quantity"])+" "+str(data["totalNutrients"]["FAT"]["unit"])
for x in data["healthLabels"]:
    healthLabels.add(x)
cal_perc = foodCalories / customerData["calories"] * 100
pro_perc = foodProtein / customerData["protein"] * 100
fat_perc = foodFat / customerData["fat"] * 100
carb_perc = foodCarbs / customerData["carbs"] * 100
print("Calories: " + str(cal_perc) + "%" + "   " + str(foodCalories) + "/" + str(customerData["calories"]))
print("Protein: " + str(pro_perc) + "%" + "   " + str(foodProtein) + "/" + str(customerData["protein"]))
print("Fat: " + str(fat_perc) + "%" + "   " + str(foodFat) + "/" + str(customerData["fat"]))
print("Carbohydrates: " + str(carb_perc) + "%" + "   " + str(foodCarbs) + "/" + str(customerData["carbs"]))
#print(healthLabels)
#print(str(calories)+ " "+str(fats))