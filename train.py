import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ──────────────────────────────────────────────
# AYARLAR
# ──────────────────────────────────────────────
TRAIN_DIR = "dataset/train"
VAL_DIR   = "dataset/validation"
IMG_SIZE  = (64, 64)
BATCH     = 16
EPOCHS    = 10
MODEL_OUT = "model/plant_model.h5"
# ──────────────────────────────────────────────

# Dataset kontrolü
for d in [TRAIN_DIR, VAL_DIR]:
    if not os.path.exists(d):
        print(f"❌ Klasör bulunamadı: {d}")
        print("   Önce organize_dataset.py çalıştır!")
        exit()

train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)

val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical",
    shuffle=True
)

val_data = val_gen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical",
    shuffle=False
)

print("\n📊 Sınıf mapping:")
print(train_data.class_indices)
print(f"   Train  : {train_data.samples} resim")
print(f"   Val    : {val_data.samples} resim\n")

# Model
model = Sequential([
    tf.keras.Input(shape=(64, 64, 3)),

    Conv2D(32, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu', padding='same'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Eğitim
model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# Kaydet
os.makedirs("model", exist_ok=True)
model.save(MODEL_OUT)
print(f"\n✅ Model kaydedildi → {MODEL_OUT}")