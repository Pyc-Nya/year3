import socket
import os

# ============ НАСТРОЙКИ — МЕНЯЙ ТУТ ============
SERVER_IP = "192.168.1.103"    # ← IP-адрес сервера (узнай через ipconfig)
PORT = 9999                     # должен совпадать с server.py
SAVE_DIR = r"C:\Users\pyc_nya\Downloads"   # ← куда сохранить файл
# ===============================================

def receive_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Подключаюсь к {SERVER_IP}:{PORT}...")
        s.connect((SERVER_IP, PORT))
        print("Подключился!")

        # Читаем заголовок
        header_len = int.from_bytes(s.recv(4), "big")
        header = s.recv(header_len).decode()
        file_name, file_size = header.split("|||")
        file_size = int(file_size)

        save_path = os.path.join(SAVE_DIR, file_name)
        print(f"Получаю: {file_name} ({file_size / 1e9:.2f} ГБ)")
        print(f"Сохраняю в: {save_path}")

        # Принимаем файл
        received = 0
        with open(save_path, "wb") as f:
            while received < file_size:
                chunk = s.recv(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                pct = received / file_size * 100
                print(f"\rПолучено: {received / 1e9:.2f} ГБ / {file_size / 1e9:.2f} ГБ ({pct:.1f}%)", end="")

        print("\nГотово!")

receive_file()