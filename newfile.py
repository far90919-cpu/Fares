from flask import Flask, request
import requests

app = Flask(__name__)

# ضع هنا رمز التحقق الخاص بك (يمكنك تغيير هذه الكلمة)
VERIFY_TOKEN = "MY_SECRET_BOT_TOKEN_2026"
# رمز الوصول للصفحة (سنحصل عليه من فيسبوك لاحقاً)
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"

@app.route('/', methods=['GET'])
def verify():
    # خطوة التحقق التي يطلبها فيسبوك للتأكد من سيرفرك
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "خطأ في رمز التحقق!"

@app.route('/', methods=['POST'])
def webhook():
    # استقبال الرسائل القادمة من فيسبوك
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    
                    # قراءة نص الرسالة التي أرسلها المستخدم
                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"]["text"]
                        
                        # المنطق البسيط للرد
                        if "مرحبا" in message_text.lower() or "السلام" in message_text:
                            reply = "أهلاً بك! أنا بوت الرد الآلي، كيف يمكنني مساعدتك اليوم؟"
                        else:
                            reply = f"وصلتني رسالتك: '{message_text}'"
                            
                        send_message(sender_id, reply)
    return "ok", 200

def send_message(recipient_id, message_text):
    # إرسال الرد إلى ماسنجر
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v18.0/me/messages", params=params, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(port=5000)                