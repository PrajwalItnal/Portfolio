from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='template')
CORS(app)  # allow your frontend to call this backend

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    # Email setup (replace with your details)
    sender_email = os.getenv('SENDER_EMAIL')  # your email
    sender_password = os.getenv('SENDER_PASSWORD')  # use Gmail App Password
    receiver_email = sender_email  # send to yourself

    # Prepare the email
    subject = f"New message from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    subject_user = "Thank you for contacting me!"
    body_user = f"Hi {name},\n\nThanks for reaching out! I’ve received your message and will get back to you soon.\n\n- Prajwal"
    msg_user = MIMEText(body_user)
    msg_user["Subject"] = subject_user
    msg_user["From"] = sender_email
    msg_user["To"] = email



    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.send_message(msg_user)
        return jsonify({"status": "success", "message": "Email sent successfully"})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Failed to send email"})

if __name__ == "__main__":
    app.run(debug=True)
