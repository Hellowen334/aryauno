#!/bin/bash
# Render için build script

# Dosya izinlerini göster
echo "Dosya izinleri:"
ls -la

# Gerekli paketleri yükle
pip install -r requirements.txt

# Dosya yapısını göster (debug için)
echo "Dosya yapısı:"
ls -la
ls -la unu/

# Build tamamlandı
echo "Build tamamlandı!"