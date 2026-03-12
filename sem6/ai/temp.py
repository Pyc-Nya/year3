import os
import shutil

src = "PokemonData"
dst = "dataset"

for folder in os.listdir(src):
    folder_path = os.path.join(src, folder)
    if not os.path.isdir(folder_path):
        continue
    for file in os.listdir(folder_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            src_file = os.path.join(folder_path, file)
            # Добавляем имя подпапки к файлу, чтобы не было конфликтов имён
            dst_file = os.path.join(dst, f"{folder}_{file}")
            shutil.copy2(src_file, dst_file)

print(f"Готово! Скопировано файлов: {len(os.listdir(dst))}")