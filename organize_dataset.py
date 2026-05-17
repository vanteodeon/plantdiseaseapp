"""
PlantVillage → blight/healthy/rust Dönüştürücü
================================================
Kullanım:
  1. SOURCE_DIR = senin büyük dataset'in (train klasörü)
  2. TARGET_DIR = projenin dataset/train klasörü
  3. python organize_dataset.py

Script ne yapar:
  - "blight" geçen tüm klasörleri  → blight/
  - "healthy" geçen tüm klasörleri → healthy/
  - "rust" geçen tüm klasörleri    → rust/
  - Geri kalanları ignore eder
  - Görüntüleri kopyalar (silmez, güvenli)
  - Sonunda kaç görüntü kopyalandığını gösterir
"""

import os
import shutil
import random
from pathlib import Path

# ──────────────────────────────────────────────
# AYARLAR — sadece bu iki satırı değiştir
# ──────────────────────────────────────────────
SOURCE_DIR = r"C:\Users\damla\Desktop\plant_disease_app\dataset\PlantVillage"
TARGET_DIR = r"C:\Users\damla\Desktop\plant_disease_app\dataset\train"

VALIDATION_SPLIT = 0.2   # %20 validation, %80 train
MAX_PER_CLASS    = 500    # Her sınıftan max kaç resim (None = hepsini al)
RANDOM_SEED      = 42
# ──────────────────────────────────────────────

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

# Hangi klasör adı hangi sınıfa gidiyor
def get_class(folder_name: str):
    name = folder_name.lower()
    if "blight" in name or "spot" in name or "mold" in name or "scorch" in name or "mildew" in name or "measles" in name or "rot" in name:
        return "blight"
    elif "healthy" in name:
        return "healthy"
    elif "rust" in name:
        return "rust"
    return None  # ignore

def copy_images(src_folder, dst_folder, images):
    os.makedirs(dst_folder, exist_ok=True)
    for img_name in images:
        src = os.path.join(src_folder, img_name)
        dst = os.path.join(dst_folder, img_name)
        # İsim çakışmasını önle
        if os.path.exists(dst):
            stem, ext = os.path.splitext(img_name)
            dst = os.path.join(dst_folder, f"{stem}_{random.randint(1000,9999)}{ext}")
        shutil.copy2(src, dst)

def main():
    random.seed(RANDOM_SEED)

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ SOURCE_DIR bulunamadı: {SOURCE_DIR}")
        return

    # Tüm klasörleri tara ve sınıflara grupla
    class_buckets = {"blight": [], "healthy": [], "rust": []}

    all_folders = [f for f in os.listdir(SOURCE_DIR)
                   if os.path.isdir(os.path.join(SOURCE_DIR, f))]

    print(f"📂 {len(all_folders)} klasör tarandı...\n")

    for folder in sorted(all_folders):
        cls = get_class(folder)
        folder_path = os.path.join(SOURCE_DIR, folder)

        images = [f for f in os.listdir(folder_path)
                  if Path(f).suffix.lower() in VALID_EXTENSIONS]

        if cls is None:
            print(f"   ⏭  SKIP  : {folder} ({len(images)} resim)")
            continue

        class_buckets[cls].append((folder_path, images))
        print(f"   ✅ {cls:8s}: {folder} ({len(images)} resim)")

    print()

    # Her sınıf için kopyala
    total_train = 0
    total_val   = 0

    for cls, entries in class_buckets.items():
        # Tüm resimleri tek listeye topla
        all_images = []
        for folder_path, images in entries:
            for img in images:
                all_images.append((folder_path, img))

        random.shuffle(all_images)

        # MAX_PER_CLASS uygula
        if MAX_PER_CLASS:
            all_images = all_images[:MAX_PER_CLASS]

        split_idx = int(len(all_images) * (1 - VALIDATION_SPLIT))
        train_imgs = all_images[:split_idx]
        val_imgs   = all_images[split_idx:]

        train_dst = os.path.join(TARGET_DIR, cls)
        val_dst   = os.path.join(
            TARGET_DIR.replace("\\train", "\\validation").replace("/train", "/validation"),
            cls
        )

        # Kopyala
        for folder_path, img_name in train_imgs:
            copy_images(folder_path, train_dst, [img_name])
        for folder_path, img_name in val_imgs:
            copy_images(folder_path, val_dst, [img_name])

        print(f"   {cls:8s} → train: {len(train_imgs)}, validation: {len(val_imgs)}")
        total_train += len(train_imgs)
        total_val   += len(val_imgs)

    print(f"\n✅ Tamamlandı!")
    print(f"   Toplam train      : {total_train} resim")
    print(f"   Toplam validation : {total_val} resim")
    print(f"\n📁 Hedef klasör: {TARGET_DIR}")
    print("\nArtık python train.py çalıştırabilirsin! 🚀")

if __name__ == "__main__":
    main()
