from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bmi_bmr_calculator():
    bmi = ''
    feedback = ''
    calories = ''
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        meter_height = height / 100  # Convert height to meters
        age = int(request.form['age'])
        gender = request.form['gender']
        daily_calories = request.form['daily_calories']
        bmi = weight / (meter_height ** 2)
        bmi = round(bmi, 2)
        
        if bmi < 18.5:
            feedback = 'Underweight'
        elif 18.5 <= bmi < 24.9:
            feedback = 'Normal weight'
        elif 25 <= bmi < 29.9:
            feedback = 'Overweight'
        else:
            feedback = 'Obesity'
        
        if gender == 'male':
            bmr = 66.5 + (13.75 * weight) + (5.003 * height * 100) - (6.75 * age)
        elif gender == 'female':
            bmr = 655.1 + (9.563 * weight) + (1.850 * height * 100) - (4.676 * age)
        if daily_calories == 'sedentary':
            calories = bmr * 1.2
        elif daily_calories == 'lightly_active':
            calories = bmr * 1.375
        elif daily_calories == 'moderately_active':
            calories = bmr * 1.55
        elif daily_calories == 'very_active':
            calories = bmr * 1.725
        elif daily_calories == 'super_active':
            calories = bmr * 1.9

    return render_template('index.html', bmi=bmi, feedback=feedback, calories=calories)

if __name__ == '__main__':
    app.run(debug=True)