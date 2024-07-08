from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bmi_calculator():
    bmi = ''
    feedback = ''
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height']) / 100  # Convert height to meters
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
        
        if bmi < 18.5:
            feedback = 'Underweight'
        elif 18.5 <= bmi < 24.9:
            feedback = 'Normal weight'
        elif 25 <= bmi < 29.9:
            feedback = 'Overweight'
        else:
            feedback = 'Obesity'
    
    return render_template('index.html', bmi=bmi, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)