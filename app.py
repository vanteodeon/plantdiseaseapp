import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import os

# ──────────────────────────────────────────────
MODEL_PATH = "model/plant_model.h5"
IMG_SIZE   = (64, 64)
CLASSES    = ["blight", "healthy", "rust"]  # train_data.class_indices sırasıyla
# ──────────────────────────────────────────────

# Model yükle
if not os.path.exists(MODEL_PATH):
    import tkinter.messagebox as mb
    root_check = tk.Tk()
    root_check.withdraw()
    mb.showerror("Model Bulunamadı", f"{MODEL_PATH} dosyası yok.\nÖnce train.py çalıştır!")
    exit()

model = tf.keras.models.load_model(MODEL_PATH)

CLASS_LABELS = {
    "blight":  "🍂 Yanıklık Hastalığı",
    "healthy": "🌿 Sağlıklı Bitki",
    "rust":    "🟤 Pas Hastalığı"
}

TURKCE = {
    "blight":  "Yanıklık",
    "healthy": "Sağlıklı",
    "rust":    "Pas"
}

COLOR_MAP = {
    "blight":  "#e74c3c",
    "healthy": "#27ae60",
    "rust":    "#e67e22"
}

def predict_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)

    preds = model.predict(arr, verbose=0)[0]
    idx   = int(np.argmax(preds))
    conf  = float(preds[idx]) * 100

    return CLASSES[idx], conf, preds

def load_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Görüntü dosyaları", "*.jpg *.jpeg *.png *.bmp")]
    )
    if not file_path:
        return

    cls, conf, preds = predict_image(file_path)

    label_text = CLASS_LABELS.get(cls, cls)
    color      = COLOR_MAP.get(cls, "#333")

    label_result.config(
        text=f"Sonuç: {label_text}\nGüven: %{conf:.1f}",
        fg=color
    )

    # Confidence bar'larını güncelle
    for i, c in enumerate(CLASSES):
        bars[i]["value"] = preds[i] * 100
        bar_labels[i].config(text=f"{TURKCE[c]}: %{preds[i]*100:.1f}")

    # Resmi göster
    img = Image.open(file_path)
    img.thumbnail((280, 280))
    img_tk = ImageTk.PhotoImage(img)
    panel.config(image=img_tk)
    panel.image = img_tk

# ──────────── GUI ────────────
root = tk.Tk()
root.title("🌿 Bitki Hastalık Tespiti")
root.geometry("380x580")
root.resizable(False, False)
root.configure(bg="#f0f4f0")

tk.Label(root, text="Bitki Hastalık Tespiti",
         font=("Helvetica", 16, "bold"),
         bg="#f0f4f0", fg="#2c3e50").pack(pady=(16, 4))

btn = tk.Button(root, text="📂 Görüntü Seç", command=load_image,
                font=("Helvetica", 11),
                bg="#2ecc71", fg="white",
                activebackground="#27ae60",
                relief="flat", padx=12, pady=6)
btn.pack(pady=8)

panel = tk.Label(root, bg="#dce8dc", relief="sunken",
                 width=280, height=280)
panel.pack(pady=6)

label_result = tk.Label(root, text="Sonuç: —",
                        font=("Helvetica", 13, "bold"),
                        bg="#f0f4f0", fg="#2c3e50",
                        justify="center")
label_result.pack(pady=8)

# Confidence bars
bar_frame = tk.Frame(root, bg="#f0f4f0")
bar_frame.pack(fill="x", padx=30)

bars       = []
bar_labels = []

for cls in CLASSES:
    row = tk.Frame(bar_frame, bg="#f0f4f0")
    row.pack(fill="x", pady=2)

    lbl = tk.Label(row, text=f"{TURKCE[cls]}: —", width=20, anchor="w",
                   bg="#f0f4f0", font=("Helvetica", 9))
    lbl.pack(side="left")

    bar = ttk.Progressbar(row, length=120, maximum=100)
    bar.pack(side="left", padx=4)

    bars.append(bar)
    bar_labels.append(lbl)

root.mainloop()