def calculate(infoMap):
    list_of_restrictions = set()
    if infoMap["restrictions"] == "yes":
        userInput = input("list your food restrictions separated by commas:  ")
        list_of_restrictions = set(userInput.split(","))
    BMR = 0

    exerciseMap = {"low":1.2,"light":1.375,"moderate":1.55,"heavy":1.725}
    goalMap = {"lose":-0.2,"maintain":1,"gain":0.2}

    #BMR Calculation
    if infoMap["gender"] == "male":
        BMR = 66.47 + (13.75 * infoMap["weight"]) + (5.0 * infoMap["height"]) - (6.75 * infoMap["age"])
    else:
        BMR = 665.09 + (9.56 * infoMap["weight"]) + (1.84 * infoMap["height"]) - (4.67 * infoMap["age"])

    BMR *= exerciseMap[infoMap["exerciseLevel"]]
    BMR = BMR + (BMR * goalMap[infoMap["goal"]])

    calories = BMR
    protein = infoMap["weight"] * 0.825
    fat = BMR * 0.25 / 9.0
    carbs = (BMR - protein - fat) / 4.0

<<<<<<< HEAD
    return {"calories":calories, "protein":protein, "fat":fat, "carbs":carbs, "restrictions":list_of_restrictions}
=======
    return {"calories":calories, "protein":protein, "fat":fat, "carbs":carbs, "restrictions":list_of_restrictions}
>>>>>>> 4fe12015fb167d78ceaf3df2e5b9eddba822b74f
