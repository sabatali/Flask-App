import os
import requests
import logging
from flask import Blueprint, redirect, request, jsonify

# Initialize Blueprint for API
api = Blueprint("api", __name__)

# Upwork OAuth credentials
CLIENT_ID = "d32f8b5da7cf06845c5d2f12f499055d"
CLIENT_SECRET = "7028b54fc4111c07"
REDIRECT_URI = "https://upwork-nhnb.onrender.com/callback"
UPWORK_TOKEN_URL = "https://www.upwork.com/api/v3/oauth2/token"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Step 1: Redirect user to Upwork Authorization URL
@api.route("/auth")
def auth():
    try:
        print("==================Redirect user to Upwork Authorization URL===============")
        auth_url = (
            f"https://www.upwork.com/ab/account-security/oauth2/authorize?"
            f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        )
        logger.debug(f"Redirecting to Upwork Authorization URL: {auth_url}")
        return redirect(auth_url)
    except Exception as e:
        logger.error(f"Error redirecting to Upwork Authorization URL: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to initiate authorization flow"}), 500

# Step 2: Handle OAuth Callback & Exchange Code for Tokens
@api.route("/callback")
def callback():
    try:
        print("==================Handle OAuth Callback & Exchange Code for Tokens===============")
        code = request.args.get("code")
        if not code:
            logger.error("Authorization code missing in callback")
            return jsonify({"status": "error", "message": "Authorization code missing"}), 400

        logger.debug(f"Authorization code received: {code}")

        # Exchange code for tokens
        response = requests.post(
            UPWORK_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()  # Raise an exception for bad responses

        tokens = response.json()
        logger.debug(f"Tokens received: {tokens}")

        print("Access Token: " + tokens.get("access_token"))
        print("Refresh Token: " + tokens.get("refresh_token"))

        return jsonify({
            "status": "success",
            "message": "Authorization successful!",
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
        }), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during token exchange: {str(e)}")
        if e.response:
            logger.error(f"Error response: {e.response.text}")
        return jsonify({
            "status": "error",
            "message": "Failed to get tokens",
            "details": str(e),
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error during callback: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Unexpected error during callback",
            "details": str(e),
        }), 500

# Step 3: Refresh Access Token using Refresh Token
@api.route("/refresh")
def refresh():
    try:
        refresh_token = "oauth2v2_b1cc8b45ab3613ba202e625b06559264"
        if not refresh_token:
            logger.error("No refresh token available")
            return jsonify({"status": "error", "message": "No refresh token available"}), 400

        logger.debug(f"Using refresh token: {refresh_token}")

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
        response.raise_for_status()  # Raise an exception for bad responses

        tokens = response.json()
        logger.debug(f"Tokens refreshed: {tokens}")

        return jsonify({
            "status": "success",
            "message": "Token refreshed successfully!",
            "access_token": tokens.get("access_token"),
            "refresh_token": tokens.get("refresh_token"),
        }), 200

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during token refresh: {str(e)}")
        if e.response:
            logger.error(f"Error response: {e.response.text}")
        return jsonify({
            "status": "error",
            "message": "Failed to refresh token",
            "details": str(e),
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error during token refresh: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Unexpected error during token refresh",
            "details": str(e),
        }), 500
