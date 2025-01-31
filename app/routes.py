import os
from flask import Blueprint, redirect, request, jsonify, session
import requests

api = Blueprint('api', __name__)
api.secret_key = os.urandom(24)  # Necessary for session storage

CLIENT_ID = "1ff9ff298eca330521db8ed3dd41b68b"
CLIENT_SECRET = "a3d3deef4e7f25a8"
REDIRECT_URI = "https://maliksabatali.pythonanywhere.com/callback"


# Step 1: Authorization URL
@api.route("/auth")
def auth():
    auth_url = (
        f"https://www.upwork.com/ab/account-security/oauth2/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)


@api.route("/callback")
def callback():
    code = request.args.get("code")

    try:
        response = requests.post(
            "https://www.upwork.com/api/v3/oauth2/token",
            data={
                "grant_type": "refresh_token",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": "oauth2v2_91c55d4ac5ff4689f9f23f1071832a3f",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        response.raise_for_status()
        tokens = response.json()

        access_token = tokens.get("access_token")


        # Return tokens in the HTTP response
        return jsonify({
            "status": "success",
            "message": "Authorization successful!",
            "access_token": access_token,
        }), 200

    except requests.exceptions.RequestException as e:
        print("Error exchanging token:", e.response.json() if e.response else str(e))
        return jsonify({
            "status": "error",
            "message": "Authentication failed",
            "details": e.response.json() if e.response else str(e)
        }), 500




@api.route("/profile")
def profile():
    access_token = "oauth2v2_984b48ab37dd182cfbc77d173380823e"  

    if not access_token:
        return "Access token is missing. Please authenticate first.", 400

    try:
        response = requests.get(
            "https://www.upwork.com/api/team/v3/workdiaries/contracts/37174334/2025-01-30.json",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        print("🚀 ~ response:", response)

        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        print("Error fetching profile:", e.response.json() if e.response else str(e))
        return "Failed to fetch profile", 500


ACCESS_TOKEN = 'oauth2v2_984b48ab37dd182cfbc77d173380823e'
# Endpoint variables
BASE_URL = 'https://www.upwork.com/api'
CONTRACT_ID = '38693670'         # Replace with the actual contract ID
DATE = '20250101'           # Use the desired date in YYYY-MM-DD format
FORMAT = 'json'

           # Specify the desired format (e.g., json or xml)

@api.route("/get_workdiary")
def get_workdiary():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    url = f'{BASE_URL}/team/v3/workdiaries/contracts/{CONTRACT_ID}.{FORMAT}'
    response = requests.get(url, headers=headers)

    response.raise_for_status()
    return jsonify(response.json())
