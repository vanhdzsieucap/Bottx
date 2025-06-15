bot_tai_xiu_ai.py

import telebot import pytesseract from PIL import Image import cv2 import random import os

Cấu hình token Telegram Bot (bạn thay bằng token của bạn)

TOKEN = "YOUR_BOT_TOKEN_HERE" bot = telebot.TeleBot(TOKEN)

======== HÀM PHÂN TÍCH ========

def pattern_vote(data): if len(data) < 3: return None if data[-1] == data[-2] == data[-3]: return data[-1] return None

def prob_vote(data): if len(data) < 6: return None return max(set(data), key=data.count)

def random_vote(): return random.choice(['tài', 'xỉu'])

def du_doan(data): if len(data) < 4: return "❗ Chưa đủ dữ liệu để dự đoán." votes = [pattern_vote(data), prob_vote(data), random_vote()] votes = [v for v in votes if v is not None] if not votes: return "Không đủ tín hiệu để đưa ra dự đoán." prediction = max(set(votes), key=votes.count) phan_tram = round(votes.count(prediction) / len(votes) * 100)

chuoi = 1
for i in range(len(data) - 2, -1, -1):
    if data[i] == data[-1]:
        chuoi += 1
    else:
        break

canh_bao = "🚫 Cẩn thận!" if chuoi >= 3 else "✅ Ổn định"

return (
    f"🔮 Dự đoán: **{prediction.upper()}**\n"
    f"🗳️ Đồng thuận: {phan_tram}%\n"
    f"📊 Chuỗi hiện tại: {chuoi} {data[-1].upper()} liên tiếp.\n"
    f"⚠️ {canh_bao}"
)

===== OCR ẢNH =====

def xu_ly_anh_ocr(path): image = cv2.imread(path) gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) text = pytesseract.image_to_string(gray) return text

def tach_ket_qua(text): dong = text.lower().replace(" ", "").splitlines() ket_qua = [] for d in dong: if d.isdigit(): so = int(d) if so <= 10: ket_qua.append("xỉu") elif so >= 11: ket_qua.append("tài") return ket_qua

===== LỊCH SỬ DỮ LIỆU =====

du_lieu = []

===== TELEGRAM COMMANDS =====

@bot.message_handler(commands=['start']) def send_welcome(message): bot.reply_to(message, "👋 Chào bạn! Gửi ảnh kết quả hoặc nhập chuỗi TÀI/XỈU để dự đoán nhé!")

@bot.message_handler(content_types=['photo']) def handle_photo(message): file_info = bot.get_file(message.photo[-1].file_id) downloaded_file = bot.download_file(file_info.file_path) file_path = f"temp_{message.chat.id}.jpg" with open(file_path, 'wb') as f: f.write(downloaded_file)

text = xu_ly_anh_ocr(file_path)
ket_qua = tach_ket_qua(text)
os.remove(file_path)

global du_lieu
du_lieu += ket_qua
if not ket_qua:
    bot.reply_to(message, "❌ Không đọc được kết quả từ ảnh.")
else:
    kq = ", ".join(ket_qua)
    bot.reply_to(message, f"✅ Đã nhận kết quả: {kq}\n\n{du_doan(du_lieu)}")

@bot.message_handler(func=lambda m: True) def handle_text(message): global du_lieu text = message.text.lower().strip() if text in ["tài", "xỉu"]: du_lieu.append(text) bot.reply_to(message, du_doan(du_lieu)) elif text == "reset": du_lieu = [] bot.reply_to(message, "♻️ Đã reset dữ liệu!") else: bot.reply_to(message, "❓ Vui lòng nhập 'tài' hoặc 'xỉu', hoặc gửi ảnh bảng kết quả!")

===== CHẠY BOT =====

if name == "main": bot.infinity_polling()

