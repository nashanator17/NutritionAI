def calculate(infoMap):
    list_of_allergies = set()
    list_of_diets = set()
    #list_of_healthLabels = [VEGETARIAN, DAIRY_FREE, KOSHER]
    # restrictionsMap = {"vegetarian":"VEGETARIAN",
    #                    "vegan":"VEGAN",
    #                    "pescetarian": "PESCETARIAN",
    #                    "gluten-free": "gluten",
    #                    "kosher": "KOSHER"}

    # if infoMap["allergies"] == "yes":

    if infoMap["restrictions"] == "yes":
        allergyConfirm = input("Are you allergic to certain foods?  ")
        if allergyConfirm == "yes":
            userInput = input("list your food allergies separated by commas:  ")
            userInput = userInput.split(",")
            list_of_allergies = set(userInput)
            # for allergy in userInput:
            #     list_of_healthLabels.update(allergy.upper()+"_FREE")



        medicalConfirm = input("Do you currently follow a diet for medical reasons? (ex. diabetes?)  ")
        if medicalConfirm == "yes":
            medicalInput = input("list your current diets separated by commas:  ")
            for medicalCondition in medicalInput:
                list_of_allergies.update(restrictionMap.get(medicalCondition))
            # if map contains anything in the input String
            # append the value of they key in the amp into list of allergies
            # ex. input is diabetes, gluten-free
            # return value of diabetes and gluten free

        dietConfirm = input("Do you currently follow a non-religious diet? (ex. vegetarian)?  ")
        if dietConfirm == "yes":
            dietInput = input("list your current diets separated by commas:  ")
            dietInput = dietInput.split(",")
            list_of_diets.update(dietInput)
            # for diet in dietInput:
            #     list_of_diets.update(diet.upper())

        religionConfirm = input("Do you currently follow a religious diet? (ex. kosher)?  ")
        if dietConfirm == "yes":
            religiousInput = input("list your current diets separated by commas:  ")
            religiousInput = religiousInput.split(",")
            list_of_diets.update(religiousInput)
            # for diet in religiousInput:
            #     list_of_diets.update(diet.upper())


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

    return {"calories":calories, "protein":protein, "fat":fat, "carbs":carbs, "allergies":list_of_allergies, "diets":list_of_diets}
