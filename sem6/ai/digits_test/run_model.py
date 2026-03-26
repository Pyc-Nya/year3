import os
import random
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ===================================================
# НАСТРОЙКИ — поменяй пути если надо
# ===================================================
MODEL_PATH = "/home/pyc_nya/tf-gpu/AlexNet_best.keras"
TEST_DIR   = "/mnt/c/projects/year3/sem6/ai/digits_test/dataset_test"
IMG_SIZE   = 224
BATCH_SIZE = 32
N_SHOW     = 100  # сколько картинок показать

# ===================================================
# ЗАГРУЗКА МОДЕЛИ И ДАННЫХ
# ===================================================
model = tf.keras.models.load_model(MODEL_PATH)
print("Модель загружена")

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = test_ds.class_names
print(f"Классы: {class_names}")

norm = tf.keras.layers.Rescaling(1./255)
test_ds = test_ds.map(lambda x, y: (norm(x), y)).prefetch(tf.data.AUTOTUNE)

# ===================================================
# СОБИРАЕМ ВСЕ ПРЕДСКАЗАНИЯ
# ===================================================
all_images, all_true, all_pred, all_conf = [], [], [], []

for imgs, labels in test_ds:
    probs = model.predict(imgs, verbose=0)
    all_images.extend(imgs.numpy())
    all_true.extend(labels.numpy())
    all_pred.extend(probs.argmax(axis=1))
    all_conf.extend(probs.max(axis=1))

total = len(all_true)
correct = sum(p == t for p, t in zip(all_pred, all_true))
print(f"\nТочность на тесте: {correct}/{total} = {correct/total:.3f}")

# ===================================================
# РИСУЕМ N_SHOW СЛУЧАЙНЫХ КАРТИНОК
# ===================================================
indices = random.sample(range(total), N_SHOW)
cols = 10
rows = N_SHOW // cols

fig, axes = plt.subplots(rows, cols, figsize=(cols * 2, rows * 2.5))

for plot_i, idx in enumerate(indices):
    ax = axes[plot_i // cols][plot_i % cols]
    ax.imshow(all_images[idx])
    ax.axis('off')
    true_label = class_names[all_true[idx]]
    pred_label = class_names[all_pred[idx]]
    color = 'green' if true_label == pred_label else 'red'
    ax.set_title(f"pred:{pred_label}\ntrue:{true_label}", fontsize=7, color=color)

plt.suptitle(f"AlexNet — тест (accuracy={correct/total:.3f})", fontsize=14)
plt.tight_layout()
plt.savefig('test_predictions.png', dpi=150, bbox_inches='tight')
print("Сохранено: test_predictions.png")