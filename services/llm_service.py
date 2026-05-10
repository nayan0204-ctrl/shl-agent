import google.generativeai as genai

genai.configure(api_key="AIzaSyAofbeI49ww0Rty3JSe_d493Kb1O3zQ45Q")

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_reply(prompt):

    response = model.generate_content(prompt)

    return response.text