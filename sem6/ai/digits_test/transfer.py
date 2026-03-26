import os
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

cudnn_path  = find_lib_path('libcudnn*.so*')
cublas_path = find_lib_path('libcublas*.so*')
ld_paths = ['/usr/local/cuda-12.4/lib64', '/usr/lib/wsl/lib']
if cudnn_path: ld_paths.append(cudnn_path)
if cublas_path: ld_paths.append(cublas_path)
os.environ['LD_LIBRARY_PATH'] = ':'.join(ld_paths)

import tensorflow as tf
import numpy as np

MODEL_PATH      = "/home/pyc_nya/tf-gpu/AlexNet_best.keras"
FINETUNED_PATH  = "/home/pyc_nya/tf-gpu/AlexNet_mnist.keras"
IMG_SIZE        = 224
BATCH_SIZE      = 64

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)
    print("GPU найден")

# ===================================================
# ЗАГРУЖАЕМ MNIST
# ===================================================
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# оставляем как есть — numpy 28x28, ресайз будет на лету
x_train = x_train.astype(np.float32) / 255.0
x_test  = x_test.astype(np.float32)  / 255.0

# добавляем channel dimension: (60000, 28, 28) -> (60000, 28, 28, 1)
x_train = x_train[..., np.newaxis]
x_test  = x_test[..., np.newaxis]

def prepare(image, label):
    # grayscale -> RGB
    image = tf.repeat(image, 3, axis=-1)
    # ресайз на лету — не грузит память
    image = tf.image.resize(image, [IMG_SIZE, IMG_SIZE])
    return image, label

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)) \
    .shuffle(10000) \
    .map(prepare, num_parallel_calls=tf.data.AUTOTUNE) \
    .batch(BATCH_SIZE) \
    .prefetch(tf.data.AUTOTUNE)

test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)) \
    .map(prepare, num_parallel_calls=tf.data.AUTOTUNE) \
    .batch(BATCH_SIZE) \
    .prefetch(tf.data.AUTOTUNE)

# ===================================================
# ЗАГРУЖАЕМ МОДЕЛЬ И ДООБУЧАЕМ
# ===================================================
model = tf.keras.models.load_model(MODEL_PATH)
print("Модель загружена")

# замораживаем все слои кроме последних 4 (Dense слои)
for layer in model.layers[:-4]:
    layer.trainable = False

trainable_count = sum(1 for l in model.layers if l.trainable)
print(f"Обучаемых слоёв: {trainable_count} из {len(model.layers)}")

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),  # маленький lr
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),
    tf.keras.callbacks.ModelCheckpoint(
        FINETUNED_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

history = model.fit(
    train_ds,
    epochs=10,
    validation_data=test_ds,
    callbacks=callbacks
)

# ===================================================
# РЕЗУЛЬТАТ
# ===================================================
loss, acc = model.evaluate(test_ds, verbose=0)
print(f"\nТочность на MNIST test: {acc:.3f}")
print(f"Модель сохранена: {FINETUNED_PATH}")