import os
import requests
from flask import Blueprint, redirect, request, jsonify, session

api = Blueprint("api", __name__)
api.secret_key = os.urandom(24)  # Necessary for session storage

# Upwork OAuth credentials
CLIENT_ID = "1ff9ff298eca330521db8ed3dd41b68b"
CLIENT_SECRET = "a3d3deef4e7f25a8"
REDIRECT_URI = "https://maliksabatali.pythonanywhere.com/callback"
UPWORK_TOKEN_URL = "https://www.upwork.com/api/v3/oauth2/token"

# Step 1: Redirect user to Upwork Authorization URL
@api.route("/auth")
def auth():
    auth_url = (
        f"https://www.upwork.com/ab/account-security/oauth2/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

# Step 2: Handle OAuth Callback & Exchange Code for Tokens
@api.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"status": "error", "message": "Authorization code missing"}), 400

    try:
        response = requests.post(
            "https://www.upwork.com/api/v3/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        tokens = response.json()

        # Store tokens in session (Replace with DB for production)
        session["access_token"] = tokens.get("access_token")
        session["refresh_token"] = tokens.get("refresh_token")

        return jsonify({
            "status": "success",
            "message": "Authorization successful!",
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Failed to get tokens",
            "details": e.response.json() if e.response else str(e),
        }), 500

# Step 3: Refresh Access Token using Refresh Token
@api.route("/refresh")
def refresh():
    refresh_token = session.get("refresh_token")  # Retrieve refresh token from session
    if not refresh_token:
        return jsonify({"status": "error", "message": "No refresh token available"}), 400

    try:
        response = requests.post(
            UPWORK_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": refresh_token,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        tokens = response.json()

        # Update session with new tokens
        session["access_token"] = tokens.get("access_token")
        session["refresh_token"] = tokens.get("refresh_token")

        return jsonify({
            "status": "success",
            "message": "Token refreshed successfully!",
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Failed to refresh token",
            "details": e.response.json() if e.response else str(e),
        }), 500
