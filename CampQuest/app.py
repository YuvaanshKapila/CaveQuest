import requests
from ultralytics import YOLO
from flask import Flask, render_template, request, jsonify, session
import json
import os
import secrets
import geocoder
import torch
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Setting up Flask secret key
if not os.environ.get('FLASK_SECRET_KEY'):
    secret_key = secrets.token_hex(32)
    os.environ['FLASK_SECRET_KEY'] = secret_key
    print(f"Generated and set a new FLASK_SECRET_KEY: {secret_key}")

app.secret_key = os.environ.get('FLASK_SECRET_KEY')


# API Keys
GOOGLE_API_KEY = "AIzaSyDr6Q9k0F9n3XDJrhWCo-NFl5f8lFjBg7c"  # Replace with your actual API key
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m"
GOOGLE_PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={radius}&type=campground&key={api_key}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/campingPage', methods=['GET', 'POST'])
def camping_page():
    # User Location
    g = geocoder.ip('me')
    lat = g.latlng[0] if g.latlng else 43.7333
    lng = g.latlng[1] if g.latlng else -79.7667
    user_location = f"Your current location is latitude: {lat:.4f}, longitude: {lng:.4f}."

    # Weather Info
    weather = requests.get(WEATHER_API_URL.format(latitude=lat, longitude=lng)).json()
    temperature = weather.get("hourly", {}).get("temperature_2m", [])[0] if weather.get("hourly", {}).get("temperature_2m") else "N/A"
    weather_info = {"temperature": temperature}

    # Question flow
    questions = [
        "What's your group size?",
        "What's your budget for the trip?",
        "Do you have infants, kids, or elderly members in your group?",
        "Are you bringing pets?",
        "How far are you willing to travel from your current location (in km or miles)?",
        "Do you prefer comfort or adventure (e.g., access to amenities vs. more rustic experience)?"
    ]

    if 'conversation_history' not in session:
        session['conversation_history'] = ["AI: Hi! I'm your camping assistant. Let's figure out the best camping experience for you."]
        session['question_index'] = 0

    if request.method == 'POST':
        user_input = request.form['user_input']
        session['conversation_history'].append(f"User: {user_input}")
        session['question_index'] += 1

    conversation_history = session['conversation_history']
    question_index = session['question_index']
    question = None
    camping_type = None
    ai_reason = ""
    locations_data = []

    if question_index < len(questions):
        prompt = (
            f"You are a helpful camping assistant. Based on this conversation history, ask the next question:\n"
            + "\n".join(conversation_history)
            + "\n\nQuestions:\n" + "\n".join(questions) +
            f"\n\nCurrent Index: {question_index}\nNext Question:"
        )

        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(f"{BASE_URL}?key={GOOGLE_API_KEY}", headers=headers, data=json.dumps(payload))
        data = response.json()
        reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{"text": ""}])[0].get("text", "").strip()
        session['conversation_history'].append(f"AI: {reply}")
        question = questions[question_index]

    elif question_index == len(questions):
        answers = "\n".join([line.split(": ", 1)[1] for line in conversation_history if line.startswith("User:")])
        prompt = f"""
        Based on the following answers, recommend a camping type (Glamping, RV Camping, Traditional Camping).
        Format:
        Type: <Camping Type>
        Reason: <Short explanation>

        Answers:
        {answers}
        """

        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(f"{BASE_URL}?key={GOOGLE_API_KEY}", headers=headers, data=json.dumps(payload))
        data = response.json()
        recommendation = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{"text": ""}])[0].get("text", "").strip()
        session['conversation_history'].append(f"AI Recommendation:\n{recommendation}")

        try:
            for line in recommendation.strip().split("\n"):
                if line.startswith("Type:"):
                    camping_type = line.split(":")[1].strip()
                elif line.startswith("Reason:"):
                    ai_reason = line.split(":")[1].strip()
        except:
            camping_type = "Unknown"
            ai_reason = "Could not parse AI response."

        # Places
        radius = 50000
        url = GOOGLE_PLACES_API_URL.format(latitude=lat, longitude=lng, radius=radius, api_key=GOOGLE_API_KEY)
        try:
            places = requests.get(url).json()
            for place in places.get("results", [])[:5]:
                locations_data.append({
                    "name": place.get("name"),
                    "address": place.get("vicinity"),
                    "lat": place.get("geometry", {}).get("location", {}).get("lat"),
                    "lng": place.get("geometry", {}).get("location", {}).get("lng"),
                    "place_id": place.get("place_id")
                })
        except:
            locations_data.append({"name": "Error fetching nearby campgrounds.", "address": ""})

        question = "Thanks for your answers! Here's what I found."

    return render_template(
        'campingPage.html',
        camping_type=camping_type,
        reason=ai_reason,
        locations=locations_data,
        conversation_history=conversation_history,
        question=question,
        weather_info=weather_info,
        user_location=user_location,
        GOOGLE_API_KEY=GOOGLE_API_KEY
    )
    


if __name__ == '__main__':
    app.run(debug=True)
