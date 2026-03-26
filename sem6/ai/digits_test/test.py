import os

# находим пути к nvidia библиотекам через find
import subprocess
def find_lib_path(lib_name):
    try:
        result = subprocess.run(
            ['find', '/home', '-name', lib_name, '-type', 'f'],
            capture_output=True, text=True
        )
        paths = result.stdout.strip().split('\n')
        paths = [p for p in paths if p]
        if paths:
            return os.path.dirname(paths[0])
    except:
        pass
    return None

# ищем libcudnn и libcublas
cudnn_path  = find_lib_path('libcudnn*.so*')
cublas_path = find_lib_path('libcublas*.so*')

ld_paths = ['/usr/local/cuda-12.4/lib64', '/usr/lib/wsl/lib']
if cudnn_path:
    ld_paths.append(cudnn_path)
if cublas_path:
    ld_paths.append(cublas_path)

os.environ['LD_LIBRARY_PATH'] = ':'.join(ld_paths)

import random
import shutil
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')  # без дисплея — сохраняем графики в файлы
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import layers, models
from pathlib import Path
from collections import Counter

# проверяем GPU
gpus = tf.config.list_physical_devices('GPU')
print(f"GPU: {gpus}")
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)
    print("GPU найден и настроен")
else:
    print("GPU не найден, работаем на CPU")

# ===================================================
# ШАГ 1: РАЗБИВКА ДАТАСЕТА
# ===================================================
DATASET_DIR = "/mnt/c/projects/year3/sem6/ai/digits_test/dataset"
TEST_DIR    = "/mnt/c/projects/year3/sem6/ai/digits_test/dataset_test"

# запускаем только если test ещё не создан
if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR, exist_ok=True)
    for digit in range(10):
        src_dir  = os.path.join(DATASET_DIR, str(digit))
        test_dir = os.path.join(TEST_DIR, str(digit))
        os.makedirs(test_dir, exist_ok=True)

        all_imgs = [f for f in os.listdir(src_dir)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.seed(42)
        random.shuffle(all_imgs)
        test_imgs = all_imgs[:500]

        for f in test_imgs:
            shutil.copy(
                os.path.join(src_dir, f),
                os.path.join(test_dir, f)
            )
        print(f"Цифра {digit}: {len(test_imgs)} картинок в test")
    print("Test создан")
else:
    print("Test папка уже существует — пропускаем")

# ===================================================
# ШАГ 2: ЗАГРУЗКА ДАННЫХ
# ===================================================
IMG_SIZE   = 224
BATCH_SIZE = 32
AUTOTUNE   = tf.data.AUTOTUNE

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.1,
    subset="training",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=0.1,
    subset="validation",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Классы: {class_names}")
print(f"Число классов: {num_classes}")
print(f"Train батчей: {len(train_ds)}")
print(f"Val батчей:   {len(val_ds)}")
print(f"Test батчей:  {len(test_ds)}")

# нормализация
norm = tf.keras.layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (norm(x), y)).prefetch(AUTOTUNE)
val_ds   = val_ds.map(lambda x, y: (norm(x), y)).prefetch(AUTOTUNE)
test_ds  = test_ds.map(lambda x, y: (norm(x), y)).prefetch(AUTOTUNE)

# augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.05),
    layers.RandomZoom(0.05),
])
train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y)
).prefetch(AUTOTUNE)

# ===================================================
# ШАГ 3: АРХИТЕКТУРЫ
# ===================================================
def build_alexnet(num_classes, input_shape=(224, 224, 3)):
    return models.Sequential([
        layers.Conv2D(96, (11,11), strides=4, activation='relu',
                      input_shape=input_shape),
        layers.MaxPooling2D((3,3), strides=2),
        layers.Conv2D(256, (5,5), padding='same', activation='relu'),
        layers.MaxPooling2D((3,3), strides=2),
        layers.Conv2D(384, (3,3), padding='same', activation='relu'),
        layers.Conv2D(384, (3,3), padding='same', activation='relu'),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D((3,3), strides=2),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

def build_vgg16(num_classes, input_shape=(224, 224, 3)):
    return models.Sequential([
        layers.Conv2D(64, (3,3), padding='same', activation='relu',
                      input_shape=input_shape),
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

def build_vgg19(num_classes, input_shape=(224, 224, 3)):
    return models.Sequential([
        layers.Conv2D(64, (3,3), padding='same', activation='relu',
                      input_shape=input_shape),
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.Conv2D(256, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.Conv2D(512, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])

def build_custom_v1(num_classes, input_shape=(224, 224, 3)):
    return models.Sequential([
        layers.Conv2D(32, (3,3), padding='same', activation='relu',
                      input_shape=input_shape),
        layers.Conv2D(32, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.Conv2D(64, (3,3), padding='same', activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(128, (3,3), padding='same', activation='relu'),
        layers.Conv2D(128, (1,1), padding='same', activation='relu'),
        layers.AveragePooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(num_classes, activation='softmax')
    ])

# ===================================================
# ШАГ 4: ОБУЧЕНИЕ
# ===================================================
def train_model(model, name, epochs=20):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            f'{name}_best.keras',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]

    print(f"\n{'='*50}")
    print(f"Обучаем: {name}")
    print(f"{'='*50}")

    history = model.fit(
        train_ds,
        epochs=epochs,
        validation_data=val_ds,
        callbacks=callbacks
    )
    return history

models_dict = {
    'AlexNet':   build_alexnet(num_classes),
    # 'VGG16':     build_vgg16(num_classes),
    # 'VGG19':     build_vgg19(num_classes),
    # 'Custom_v1': build_custom_v1(num_classes),
}

histories = {}
for name, model in models_dict.items():
    histories[name] = train_model(model, name, epochs=20)

# ===================================================
# ШАГ 5: ГРАФИКИ — сохраняем в файлы
# ===================================================
fig, axes = plt.subplots(len(models_dict), 2,
                          figsize=(14, len(models_dict) * 4))

for row, (name, history) in enumerate(histories.items()):
    axes[row, 0].plot(history.history['accuracy'], label='train')
    axes[row, 0].plot(history.history['val_accuracy'], label='val')
    axes[row, 0].set_title(f'{name} — Accuracy')
    axes[row, 0].set_xlabel('Эпоха')
    axes[row, 0].set_ylabel('Accuracy')
    axes[row, 0].legend()

    axes[row, 1].plot(history.history['loss'], label='train')
    axes[row, 1].plot(history.history['val_loss'], label='val')
    axes[row, 1].set_title(f'{name} — Loss')
    axes[row, 1].set_xlabel('Эпоха')
    axes[row, 1].set_ylabel('Loss')
    axes[row, 1].legend()

plt.tight_layout()
plt.savefig('results_training.png', dpi=150, bbox_inches='tight')
print("График сохранён: results_training.png")

# ===================================================
# ШАГ 6: ИТОГОВАЯ ТАБЛИЦА
# ===================================================
print("\n" + "="*55)
print(f"{'Модель':15} | {'Val accuracy':12} | {'Train accuracy':14}")
print("="*55)
for name, history in histories.items():
    val_acc   = max(history.history['val_accuracy'])
    train_acc = history.history['accuracy'][-1]
    print(f"{name:15} | {val_acc:.3f}        | {train_acc:.3f}")

# ===================================================
# ШАГ 7: ТЕСТ
# ===================================================
print("\n" + "="*55)
print("Результаты на test датасете:")
print("="*55)
for name, model in models_dict.items():
    test_loss, test_acc = model.evaluate(test_ds, verbose=0)
    print(f"{name:15} | test accuracy: {test_acc:.3f}")

# ===================================================
# ШАГ 8: ВИЗУАЛИЗАЦИЯ ПРЕДСКАЗАНИЙ
# ===================================================
def show_predictions(model, name, n=50):
    all_images, all_true, all_pred, all_conf = [], [], [], []

    for imgs, labels in test_ds:
        probs = model.predict(imgs, verbose=0)
        all_images.extend(imgs.numpy())
        all_true.extend(labels.numpy())
        all_pred.extend(probs.argmax(axis=1))
        all_conf.extend(probs.max(axis=1))

    indices = random.sample(range(len(all_images)), min(n, len(all_images)))
    cols = 5
    rows = (len(indices) + cols - 1) // cols

    plt.figure(figsize=(cols * 3, rows * 3))
    for plot_i, idx in enumerate(indices):
        plt.subplot(rows, cols, plot_i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(all_images[idx])
        true_label = class_names[all_true[idx]]
        pred_label = class_names[all_pred[idx]]
        color = 'green' if true_label == pred_label else 'red'
        plt.xlabel(
            f"pred: {pred_label} {all_conf[idx]*100:.0f}%\ntrue: {true_label}",
            fontsize=7, color=color
        )

    plt.suptitle(f"{name} — предсказания на test", fontsize=14, y=1.01)
    plt.tight_layout()
    plt.savefig(f'predictions_{name}.png', dpi=150, bbox_inches='tight')
    print(f"График сохранён: predictions_{name}.png")

for name, model in models_dict.items():
    show_predictions(model, name, n=50)

print("\nВсё готово!")