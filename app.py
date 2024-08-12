from flask import Flask, render_template, request
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = """
You are a fitness specialist doctor. You are asked from a patient who is seeking advice on their health and fitness goals. Analyze the following information and suggest exercises with exercise routine and meal plan including food items.:
Age: {age}
Gender: {gender}
Weight in kg: {weight}
Height in cm: {height}
Daily Calorie Requirement: {daily_calories}
Activity Level: {activity_level}
"""
llm_chain = LLMChain(prompt=PromptTemplate(template=template), llm=gemini)

@app.route('/', methods=['GET', 'POST'])
def bmi_bmr_calculator():
    bmi = ''
    calories = ''
    feedback = ''
    advice = ''

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
        elif 18.5 <= bmi < 24.9:
            goal = "maintenance"
            feedback = "You have a normal weight. Maintain your current routine."
        else:
            goal = "weight_loss"
            feedback = "You are overweight. Focus on weight loss."

        advice = llm_chain.run({
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "daily_calories": calories,
            "activity_level": daily_calories
        })

    return render_template('index.html', bmi=bmi, calories=calories, feedback=feedback, advice=advice)

if __name__ == '__main__':
    app.run(debug=True)
