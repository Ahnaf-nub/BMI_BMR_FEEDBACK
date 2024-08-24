from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
GOOGLE_API_KEY = os.getenv('API_KEY')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_API_KEY)

prompt_template = """
You are a fitness specialist doctor. You are asked by a patient who is seeking advice on their health and fitness goals. Analyze the following information and suggest exercises with an exercise routine and meal plan, including food items.

Age: {age}
Gender: {gender}
Weight in kg: {weight}
Height in cm: {height}
Activity Level: {activity_level}
Daily Calorie Requirement: {daily_calories}

Provide your suggestions in a clear and structured format.

Format the response like this:

Health and Fitness Plan

Goals:
- Goal 1: Description
- Goal 2: Description

Exercise Routine:
- Frequency: (Number of days per week)
- Duration: (Minutes per session)
- Intensity: (Description)

Sample Workout Plan:
- Day 1: Cardio and Strength
  - Warm-up: Description
  - Cardio: Description
  - Strength Training:
    - Exercise 1: Details
    - Exercise 2: Details

- Day 2: Rest or Active Recovery
  - Active Recovery: Description

Meal Plan:
- Breakfast: (Suggestions)
- Lunch: (Suggestions)
- Dinner: (Suggestions)
- Snacks: (Suggestions)

Important Considerations:
- Consideration 1: Description
- Consideration 2: Description

Make sure the response is easy to read and well-organized.
"""

llm_chain = LLMChain(
    prompt=PromptTemplate(template=prompt_template),
    llm=gemini
)

@app.get("/", response_class=HTMLResponse)
async def bmi_bmr_calculator_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "bmi": "", "calories": "", "feedback": "", "advice": ""})

@app.post("/", response_class=HTMLResponse)
async def bmi_bmr_calculator(
    request: Request,
    weight: float = Form(...),
    height: float = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    daily_calories: str = Form(...)
):
    try:
        meter_height = height / 100

        # Calculate BMI
        bmi = weight / (meter_height * meter_height)

        # Calculate BMR based on gender
        if gender == 'male': bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else: bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Adjust BMR based on activity level
        activity_multiplier = {
            "Sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        calories = round(bmr * activity_multiplier[daily_calories])

        if bmi < 18.5: feedback = "You are underweight. Focus on muscle gain."
        elif 18.5 <= bmi < 24.9: feedback = "You have a normal weight. Maintain your current routine."
        else: feedback = "You are overweight. Focus on weight loss."

        advice = llm_chain.run({
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "daily_calories": calories,
            "activity_level": daily_calories
        })
        advice = advice.replace("**", "").replace("##", "")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "bmi": round(bmi, 2),
            "calories": calories,
            "feedback": feedback,
            "advice": advice
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
