import os
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ===================================================
# НАСТРОЙКИ
# ===================================================
MODEL_PATH = "/home/pyc_nya/tf-gpu/AlexNet_mnist.keras"
INPUT_DIR     = "/mnt/c/projects/year3/sem6/ai/digits_test/hand_input"
IMG_SIZE      = 224

# ===================================================
# ЗАГРУЗКА МОДЕЛИ
# ===================================================
model = tf.keras.models.load_model(MODEL_PATH)
print("Модель загружена")

class_names = [str(i) for i in range(10)]

# ===================================================
# ПРОГОНЯЕМ ВСЕ ФОТКИ
# ===================================================
extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
image_paths = [
    p for p in Path(INPUT_DIR).iterdir()
    if p.suffix.lower() in extensions
]

if not image_paths:
    print("Фотки не найдены!")
    exit()

print(f"Найдено фоток: {len(image_paths)}")

results = []
for path in image_paths:
    img = tf.keras.utils.load_img(path, target_size=(IMG_SIZE, IMG_SIZE))
    arr = tf.keras.utils.img_to_array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)  # добавляем batch dimension

    probs = model.predict(arr, verbose=0)[0]
    pred  = probs.argmax()
    conf  = probs.max()

    results.append({
        'path': path,
        'image': arr[0],
        'pred': class_names[pred],
        'conf': conf,
        'probs': probs
    })
    print(f"{path.name}: предсказание={class_names[pred]}, уверенность={conf*100:.1f}%")

# ===================================================
# ГРАФИК
# ===================================================
n = len(results)
fig, axes = plt.subplots(n, 2, figsize=(10, n * 4))

if n == 1:
    axes = np.array([axes])

for i, r in enumerate(results):
    # картинка
    axes[i, 0].imshow(r['image'])
    axes[i, 0].axis('off')
    axes[i, 0].set_title(
        f"{r['path'].name}\nПредсказание: {r['pred']}  ({r['conf']*100:.1f}%)",
        fontsize=12
    )

    # вероятности по всем классам
    axes[i, 1].bar(class_names, r['probs'], color='steelblue')
    axes[i, 1].set_xlabel('Цифра')
    axes[i, 1].set_ylabel('Вероятность')
    axes[i, 1].set_title('Распределение вероятностей')
    axes[i, 1].set_ylim(0, 1)

plt.tight_layout()
plt.savefig('hand_predictions.png', dpi=150, bbox_inches='tight')
print("\nСохранено: hand_predictions.png")