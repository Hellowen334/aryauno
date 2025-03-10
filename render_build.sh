#!/bin/bash
# Render için build script

# Gerekli paketleri yükle
pip install -r requirements.txt

# Dosya yapısını göster (debug için)
echo "Dosya yapısı:"
ls -la

# Eğer main.py farklı bir dizindeyse, sembolik link oluştur
# Örnek: ln -s gerçek_konum/main.py ./main.py

# Build tamamlandı
echo "Build tamamlandı!" 