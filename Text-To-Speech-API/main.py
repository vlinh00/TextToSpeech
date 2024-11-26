import json
import threading
from flask import Flask, request, jsonify
from text_to_speech_lib import text_to_speech
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
import os
from flask_cors import CORS
import sys
import atexit


lock_file_path = "server.lock"

def create_lock_file():
    """Tạo file khóa để đánh dấu server đang chạy"""
    if os.path.exists(lock_file_path):
        print("Server is already running.")
        sys.exit(0)
    else:
        with open(lock_file_path, 'w') as lock_file:
            lock_file.write(str(os.getpid()))  # Ghi PID vào file khóa

def remove_lock_file():
    """Xóa file khóa khi server dừng"""
    if os.path.exists(lock_file_path):
        os.remove(lock_file_path)


def on_clicked(icon, item):
    if item.text == 'Exit':
        icon.stop()  # Dừng icon system tray
        stop_flask()  # Dừng Flask server và thoát chương trình
    
def stop_flask():
    """Dừng Flask server và kết thúc toàn bộ tiến trình"""
    remove_lock_file()
    os._exit(0)
    

def create_image():
    # Tạo hình ảnh cho icon
    width, height = 64, 64
    image = Image.new('RGB', (width, height), color=(0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 4, height // 4, 3 * width // 4, 3 * height // 4),
        fill=(255, 255, 255))
    return image


def setup_tray_icon():
    icon = pystray.Icon('name', create_image(), 'Text-to-Speech Service')
    icon.menu = pystray.Menu(pystray.MenuItem('Exit', on_clicked))
    icon.run()


def flask_thread():
    # Đường dẫn tới chứng chỉ và khóa riêng
    ssl_cert = config['ssl_cert']
    ssl_key = config['ssl_key']
    ssl_context = (ssl_cert, ssl_key)
    
    app.run(host=config['host'], port=config['port'], ssl_context=ssl_context)
    # app.run(host=config['host'], port=config['port'])

# đọc từ file config
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
CORS(app)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data['text']
    lang = data.get('lang', config['default_lang'])

    result = text_to_speech(text, lang)
    return jsonify({"base64_audio": result})

if __name__ == '__main__':
    app_window_visible = False

    # Tạo file khóa
    create_lock_file()

    # Đảm bảo file khóa được xóa khi server dừng
    atexit.register(remove_lock_file)

     # Tạo cửa sổ GUI ẩn
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ khi khởi động
    # Chạy Flask server và icon system tray đồng thời
    threading.Thread(target=setup_tray_icon).start()
    threading.Thread(target=flask_thread).start()

