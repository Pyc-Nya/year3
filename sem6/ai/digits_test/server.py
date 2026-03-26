import socket
import os

# ============ НАСТРОЙКИ — МЕНЯЙ ТУТ ============
FILE_PATH = r"C:\projects\year3\sem6\ai\digits_test\digits_test.rar"   # ← полный путь к файлу
HOST = "0.0.0.0"                              # не трогай
PORT = 9999                                   # порт (можно любой 1024–65535)
# ===============================================

def send_file():
    file_size = os.path.getsize(FILE_PATH)
    file_name = os.path.basename(FILE_PATH)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Жду подключения на порту {PORT}...")
        conn, addr = s.accept()
        print(f"Подключился: {addr}")

        with conn:
            # Отправляем имя и размер файла
            header = f"{file_name}|||{file_size}".encode()
            conn.sendall(len(header).to_bytes(4, "big"))
            conn.sendall(header)

            # Отправляем файл
            sent = 0
            with open(FILE_PATH, "rb") as f:
                while chunk := f.read(1024 * 1024):  # 1 МБ кусками
                    conn.sendall(chunk)
                    sent += len(chunk)
                    pct = sent / file_size * 100
                    print(f"\rОтправлено: {sent / 1e9:.2f} ГБ / {file_size / 1e9:.2f} ГБ ({pct:.1f}%)", end="")

        print("\nГотово!")

send_file()