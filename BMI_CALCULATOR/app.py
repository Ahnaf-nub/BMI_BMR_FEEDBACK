from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Define exercise and meal plans
exercise_plans = {
    "weight_loss": ["Walking", "Jogging", "Cycling", "Swimming"],
    "muscle_gain": ["Weight Lifting", "Resistance Training", "Squats", "Push-ups"],
    "maintenance": ["Yoga", "Pilates", "Hiking", "Dancing"]
}

meal_plans = {
    "weight_loss": [
        {"meal": "Oatmeal with fruits", "icon": "🥣"},
        {"meal": "Grilled chicken salad", "icon": "🥗"},
        {"meal": "Quinoa and vegetables", "icon": "🥙"}
    ],
    "muscle_gain": [
        {"meal": "Scrambled eggs with avocado", "icon": "🥑"},
        {"meal": "Chicken breast with brown rice", "icon": "🍗"},
        {"meal": "Salmon with sweet potatoes", "icon": "🍣"}
    ],
    "maintenance": [
        {"meal": "Greek yogurt with honey", "icon": "🍯"},
        {"meal": "Sandwich with whole grain bread", "icon": "🥪"},
        {"meal": "Stir-fried tofu and vegetables", "icon": "🥡"}
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height']) / 100
        age = int(request.form['age'])
        gender = request.form['gender']
        activity_level = request.form['daily_calories']

        # Calculate BMI
        bmi = round(weight / (height * height), 2)

        # Calculate BMR based on gender
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)

        # Adjust BMR based on activity level
        activity_multiplier = {
            "Sedentary": 1.2,
            "lightly_active": 1.375,
            "modarately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        daily_calories = round(bmr * activity_multiplier[activity_level])

        # Determine user goal based on BMI
        if bmi < 18.5:
            goal = "muscle_gain"
            feedback = "You are underweight. Focus on muscle gain."
        elif 18.5 <= bmi < 24.9:
            goal = "maintenance"
            feedback = "You have a normal weight. Maintain your current routine."
        else:
            goal = "weight_loss"
            feedback = "You are overweight. Focus on weight loss."

        # Get exercise and meal plan
        exercises = exercise_plans[goal]
        meals = meal_plans[goal]

        return render_template('index.html', bmi=bmi, calories=daily_calories, feedback=feedback, exercises=exercises, meals=meals)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
