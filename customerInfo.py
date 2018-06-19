def calculate(gender, age, weight, height, exerciseLevel):
    goal = 'lose'
    BMR = 0

    exerciseMap = {"low":1.2,"light":1.375,"moderate":1.55,"heavy":1.725}
    goalMap = {"lose":-0.2,"maintain":1,"gain":0.2}

    #BMR Calculation
    if gender == "male":
        BMR = 66.47 + (13.75 * weight) + (5.0 * height) - (6.75 * age)
    else:
        BMR = 665.09 + (9.56 * weight) + (1.84 * height) - (4.67 * age)

    BMR *= exerciseMap[exerciseLevel]
    BMR = BMR + (BMR * goalMap[goal])

    calories = BMR
    protein = weight * 0.825
    fat = BMR * 0.25 / 9.0
    carbs = (BMR - protein - fat) / 4.0

    return {"calories":calories, "protein":protein, "fat":fat, "carbs":carbs}
