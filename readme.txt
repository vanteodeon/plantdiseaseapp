📁 1. DOSYA KONTROLÜ
Uygulamayı çalıştırmadan önce klasör yapısının şu şekilde olduğundan emin ol:

app.py: Uygulama arayüzü.

train.py: Modeli eğiten kod.

organize_dataset.py: Verileri düzenleyen kod.

requirements.txt: Gerekli kütüphanelerin listesi.

model/ klasörü: İçinde plant_model.h5 dosyası olmalı (Uygulamanın beyni budur).

🚀 2. KURULUM ADIMLARI
Python Yükle: Bilgisayarında Python 3.9(mümkünse 3.10 ben o sürüm kullandım) veya üstü bir sürüm yüklü olmalıdır. (Yüklü değilse python.org adresinden indirebilirsin).

Klasöre Git: Terminali (veya CMD) aç ve cd komutuyla sana gönderdiğim proje klasörünün içine gir.

Sanal Ortam Oluştur: Bilgisayarındaki diğer kütüphanelerle çakışmaması için şu komutu yaz:
python -m venv venv

Sanal Ortamı Aktif Et:

venv\Scripts\activate (Windows)

Kütüphaneleri Yükle: Gerekli tüm paketleri tek seferde kurmak için:
pip install -r requirements.txt

Uygulamayı Başlat: Her şey hazır! Şu komutla arayüzü aç:
python app.py

⚠️ 3. KRİTİK DOSYA YOLU UYARISI
Kodlar şu an benim bilgisayarımdaki dosya yollarına (C:\Users\earda\...) göre ayarlanmış olabilir. Eğer uygulama "Dosya bulunamadı" hatası verirse şu düzenlemeyi yapman gerekir:

organize_dataset.py, train.py veya app.py dosyalarını bir not defteri/VS Code ile aç.

En üst kısımlardaki SOURCE_DIR, TARGET_DIR veya MODEL_PATH değişkenlerinde yazan yolları, projenin senin bilgisayarındaki tam adresiyle değiştir.

💡 4. KULLANIM İPUÇLARI
Yeniden Eğitme: Eğer kendi veri setinle modeli baştan eğitmek istersen, dataset klasörüne resimlerini ekleyip önce organize_dataset.py sonra train.py dosyalarını çalıştırabilirsin.