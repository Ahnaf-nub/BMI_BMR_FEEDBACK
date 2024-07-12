from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def bmi_bmr_calculator():
    bmi = ''
    calories = ''
    feedback = ''
    exercises = []
    meals = []

    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        meter_height = height / 100  # Convert height to meters
        age = int(request.form['age'])
        gender = request.form['gender']
        daily_calories = request.form['daily_calories']

        # Calculate BMI
        bmi = round(weight / (meter_height * meter_height), 2)

        # Calculate BMR based on gender
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Adjust BMR based on activity level
        activity_multiplier = {
            "Sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        calories = round(bmr * activity_multiplier[daily_calories])

        # Determine user goal based on BMI
        if bmi < 18.5:
            goal = "muscle_gain"
            feedback = "You are underweight. Focus on muscle gain."
            exercises = [
                {"day": "Monday", "routine": "🏋️ Weight Lifting - Upper Body"},
                {"day": "Tuesday", "routine": "🏋️‍♂️ Resistance Training - Lower Body"},
                {"day": "Wednesday", "routine": "🏋️‍♀️ Squats and Lunges"},
                {"day": "Thursday", "routine": "🤸 Push-ups and Pull-ups"},
                {"day": "Friday", "routine": "💪 Core Strength Training"},
                {"day": "Saturday", "routine": "🧘‍♂️ Yoga and Stretching"},
                {"day": "Sunday", "routine": "🛌 Rest Day"}
            ]
            meals = [
                {"meal": "Egg curry with rice", "icon": "🥚"},
                {"meal": "Chicken breast with vegetables", "icon": "🍗"},
                {"meal": "Fish curry with lentils", "icon": "🐟"}
            ]
        elif 18.5 <= bmi < 24.9:
            goal = "maintenance"
            feedback = "You have a normal weight. Maintain your current routine."
            exercises = [
                {"day": "Monday", "routine": "🧘 Yoga"},
                {"day": "Tuesday", "routine": "🧘‍♀️ Pilates"},
                {"day": "Wednesday", "routine": "🥾 Hiking or Brisk Walking"},
                {"day": "Thursday", "routine": "💃 Dancing or Zumba"},
                {"day": "Friday", "routine": "🏃 Light Jogging"},
                {"day": "Saturday", "routine": "🏊 Swimming"},
                {"day": "Sunday", "routine": "🛌 Rest Day"}
            ]
            meals = [
                {"meal": "Vegetable curry with rice", "icon": "🥗"},
                {"meal": "Grilled fish with salad", "icon": "🐠🥗"},
                {"meal": "Daal (lentils) with roti", "icon": "🥙"}
            ]
        else:
            goal = "weight_loss"
            feedback = "You are overweight. Focus on weight loss."
            exercises = [
                {"day": "Monday", "routine": "🚶 Walking or Light Jogging"},
                {"day": "Tuesday", "routine": "🚴 Cycling"},
                {"day": "Wednesday", "routine": "🏊 Swimming"},
                {"day": "Thursday", "routine": "🤸 Aerobics"},
                {"day": "Friday", "routine": "🔥 High-Intensity Interval Training (HIIT)"},
                {"day": "Saturday", "routine": "💃 Dancing or Zumba"},
                {"day": "Sunday", "routine": "🛌 Rest Day"}
            ]
            meals = [
                {"meal": "Fruit salad", "icon": "🍉"},
                {"meal": "Grilled chicken salad", "icon": "🥗"},
                {"meal": "Boiled vegetables with fish", "icon": "🥦🐠"}
            ]

    return render_template('index.html', bmi=bmi, calories=calories, feedback=feedback, exercises=exercises, meals=meals)

if __name__ == '__main__':
    app.run(debug=True)
