from flask import Flask, render_template, request, jsonify
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

EXCEL_URL = "https://cdn.sschauhan.co.in/credentials.xlsx"

def load_credentials():
    df = pd.read_excel(EXCEL_URL)
    return df.to_dict(orient="records")  # List of dicts: [{Party Name, ID, Password}, ...]

@app.route('/')
def index():
    credentials = load_credentials()
    party_names = [entry["Party Name"] for entry in credentials]
    return render_template("index.html", parties=party_names)

@app.route('/login', methods=['POST'])
def login():
    selected_party = request.json.get("party")
    credentials = load_credentials()
    match = next((item for item in credentials if item["Party Name"] == selected_party), None)

    if not match:
        return jsonify({"status": "error", "message": "Party not found."}), 404

    try:
        login_id = match["ID"]
        password = match["Password"]

        driver = webdriver.Chrome()  # You can set headless if preferred
        driver.get("https://services.gst.gov.in/services/login")
        time.sleep(4)

        driver.find_element(By.ID, "username").send_keys(login_id)
        driver.find_element(By.ID, "user_pass").send_keys(password)

        return jsonify({"status": "success", "message": "Fill the CAPTCHA manually and click login."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
