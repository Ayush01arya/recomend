from flask import Flask, request, jsonify
import random
import time
import logging
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the frontend

# Define career options based on score ranges
def calculate_recommendation(data):
    # Initialize scores for different career paths
    scores = {
        "Data Scientist": 0,
        "Software Engineer": 0,
        "Marketing Specialist": 0,
        "Graphic Designer": 0
    }

    # Define scoring based on answers
    scoring = {
        "q1": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q2": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q3": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q4": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q5": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q6": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q7": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q8": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q9": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        },
        "q10": {
            "a": "Data Scientist",
            "b": "Software Engineer",
            "c": "Marketing Specialist",
            "d": "Graphic Designer"
        }
    }

    # Calculate scores based on user answers
    for question, answer in data.items():
        if question in scoring:
            career = scoring[question].get(answer)
            if career:
                scores[career] += 1

    # Determine the highest scoring career
    recommendation = max(scores, key=scores.get)

    return recommendation


@app.route('/submit', methods=['POST'])
def submit_quiz():
    data = request.json
    # Process the data to determine recommendation
    recommendation = calculate_recommendation(data)
    return jsonify({'recommendation': recommendation})
otp_storage = {}

# OTP expiration time (in seconds)
OTP_EXPIRATION_TIME = 300  # 5 minutes

# Setup logging to capture server-side errors
logging.basicConfig(level=logging.DEBUG)


def send_otp(mobile_number, otp):
    # Fast2SMS API URL
    url = f"https://www.fast2sms.com/dev/bulkV2"

    # Payload for the Fast2SMS API request
    payload = {
        'authorization': '791aHfEgF6fXxj46ZNNposGDV24WWZN3NRIq9tZdvXytz8z79KuUUpKb2Epw',
        'route': 'otp',
        'variables_values': otp,
        'flash': '1',
        'numbers': mobile_number
    }

    headers = {
        'cache-control': "no-cache"
    }

    try:
        # Send the request to Fast2SMS
        response = requests.get(url, headers=headers, params=payload)

        # Check the response status and log it
        if response.status_code == 200:
            result = response.json()  # Parse the JSON response
            logging.debug(f"Fast2SMS Response: {result}")
            # Check if the API indicated success
            if result.get("return"):
                return True
            else:
                logging.error(f"Fast2SMS error: {result.get('message')}")
                return False
        else:
            logging.error(f"Failed to send OTP, HTTP Status: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"Error sending OTP: {e}")
        return False


@app.route('/send_otp', methods=['POST'])
def send_otp_api():
    try:
        data = request.json
        mobile_number = data.get('mobile_number')

        # Validate mobile number (basic validation)
        if not mobile_number or len(mobile_number) != 10 or not mobile_number.isdigit():
            return jsonify({"message": "Invalid mobile number"}), 400

        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)

        # Send the OTP using Fast2SMS API
        success = send_otp(mobile_number, otp)

        if success:
            # Store the OTP with a timestamp for expiration
            otp_storage[mobile_number] = {"otp": otp, "timestamp": time.time()}
            return jsonify({"message": "OTP sent successfully"}), 200
        else:
            return jsonify({"message": "Failed to send OTP"}), 500

    except Exception as e:
        logging.error(f"Error in /send_otp: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500


@app.route('/verify_otp', methods=['POST'])
def verify_otp_api():
    try:
        data = request.json
        mobile_number = data.get('mobile_number')
        otp = data.get('otp')

        # Check if the OTP is valid and not expired
        if mobile_number in otp_storage:
            stored_data = otp_storage[mobile_number]
            stored_otp = stored_data['otp']
            otp_timestamp = stored_data['timestamp']

            # Check if the OTP has expired
            if time.time() - otp_timestamp > OTP_EXPIRATION_TIME:
                del otp_storage[mobile_number]  # Delete expired OTP
                return jsonify({"success": False, "message": "OTP expired"}), 400

            # Convert the received OTP to an integer for comparison
            if stored_otp == int(otp):
                del otp_storage[mobile_number]  # Delete OTP after successful verification
                return jsonify({"success": True, "message": "OTP verified successfully"}), 200
            else:
                return jsonify({"success": False, "message": "Invalid OTP"}), 400
        else:
            return jsonify({"success": False, "message": "OTP not found"}), 400
    except Exception as e:
        logging.error(f"Error in /verify_otp: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500



if __name__ == '__main__':
    app.run(debug=True)
