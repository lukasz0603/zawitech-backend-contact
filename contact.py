@app.route("/", methods=["GET"])
def home():
    return "✅ Zawitech backend działa!", 200

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os


from dotenv import load_dotenv

load_dotenv()  # wczytuje plik .env

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")

app = Flask(__name__)
CORS(app)  # Umożliwia komunikację z frontem


 ## @app.route("/")
 ## def home():
 ##   return "✅ Zawitech API działa poprawnie!"

@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"error": "Brak danych"}), 400

        msg = EmailMessage()
        msg["Subject"] = "Nowa wiadomość kontaktowa"
        msg["From"] = SMTP_USER
        msg["To"] = CONTACT_EMAIL
        msg.set_content(f"Od: {name} <{email}>\n\nWiadomość:\n{message}")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
         
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ Wystąpił błąd:", e)  # <-- pokaże błąd w terminalu
        return jsonify({"error": "Internal server error"}), 500

##if __name__ == "__main__":
##    app.run(debug=True)



    
