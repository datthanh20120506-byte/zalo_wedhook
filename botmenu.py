# botmenu.py
# Zalo OA Bot - Python/Flask
# Dùng Zalo Official Account API chính thức.
# Không dùng cookie/IMEI/QR đăng nhập tài khoản cá nhân.

import os
from datetime import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("ZALO_ACCESS_TOKEN", "")
SECRET_KEY = os.getenv("ZALO_SECRET_KEY", "")
SEND_API = "https://openapi.zalo.me/v3.0/oa/message/cs"
PORT = int(os.getenv("PORT", "5000"))


def send_message(user_id, text):
    if not ACCESS_TOKEN:
        print("CHƯA CÓ ZALO_ACCESS_TOKEN")
        return False

    headers = {
        "access_token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    data = {
        "recipient": {"user_id": user_id},
        "message": {"text": text}
    }

    try:
        response = requests.post(
            SEND_API,
            headers=headers,
            json=data,
            timeout=15
        )
        print("SEND:", response.status_code, response.text)
        return response.ok
    except Exception as e:
        print("LỖI GỬI TIN:", e)
        return False


def menu():
    return (
        "🤖 BOT MENU\n"
        "━━━━━━━━━━━━━━\n"
        "/menu   - Hiện menu\n"
        "/help   - Trợ giúp\n"
        "/ping   - Kiểm tra bot\n"
        "/time   - Xem thời gian\n"
        "/info   - Thông tin bot\n"
        "/id     - Xem User ID\n"
        "/echo   - Lặp lại nội dung\n"
        "/about  - Thông tin bot\n"
        "━━━━━━━━━━━━━━"
    )


def handle_command(user_id, text):
    text = text.strip()
    lower = text.lower()

    if lower == "/menu":
        return menu()

    if lower == "/help":
        return "📖 TRỢ GIÚP\n\nGõ /menu để xem toàn bộ lệnh."

    if lower == "/ping":
        return "🏓 Pong!\nBot đang hoạt động bình thường."

    if lower == "/time":
        now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        return f"🕐 Thời gian hiện tại:\n{now}"

    if lower == "/info":
        return (
            "🤖 BOT ZALO\n\n"
            "Nền tảng: Zalo Official Account\n"
            "Ngôn ngữ: Python\n"
            "Server: Flask\n"
            "Trạng thái: Online"
        )

    if lower == "/id":
        return f"🆔 User ID của bạn:\n{user_id}"

    if lower == "/about":
        return (
            "ℹ️ ABOUT\n\n"
            "Bot được xây dựng bằng Python + Flask "
            "và kết nối Zalo Official Account."
        )

    if lower.startswith("/echo "):
        content = text[6:].strip()
        if not content:
            return "❌ Cách dùng:\n/echo nội dung"
        return f"🔁 {content}"

    if not lower.startswith("/"):
        return "👋 Xin chào!\n\nGõ /menu để xem danh sách lệnh."

    return "❌ Không tìm thấy lệnh.\n\nGõ /menu để xem danh sách lệnh."


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "bot": "Zalo Menu Bot",
        "message": "Bot đang chạy."
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return jsonify({
            "status": "ok",
            "message": "Webhook is running"
        })

    try:
        data = request.get_json(silent=True) or {}

        print("\n========== WEBHOOK ==========")
        print(data)
        print("=============================\n")

        user_id = None
        sender = data.get("sender")

        if isinstance(sender, dict):
            user_id = sender.get("id")

        if not user_id:
            user_id = data.get("user_id")

        message = data.get("message")
        text = ""

        if isinstance(message, dict):
            text = message.get("text", "")

        if not text:
            text = data.get("text", "")

        if not user_id or not text:
            return jsonify({"status": "ok"})

        reply = handle_command(str(user_id), str(text))

        print("USER:", user_id)
        print("TEXT:", text)
        print("REPLY:", reply)

        send_message(str(user_id), reply)

        return jsonify({"status": "ok"})

    except Exception as e:
        print("WEBHOOK ERROR:", repr(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 200


if __name__ == "__main__":
    print("================================")
    print("       ZALO MENU BOT")
    print("================================")
    print("Status :", "ONLINE")
    print("Port   :", PORT)
    print("Webhook: /webhook")
    print("Menu   : /menu")
    print("================================")

    if not ACCESS_TOKEN:
        print("⚠️ Chưa có ZALO_ACCESS_TOKEN")

    if not SECRET_KEY:
        print("⚠️ Chưa có ZALO_SECRET_KEY")

    app.run(host="0.0.0.0", port=PORT, debug=False)
