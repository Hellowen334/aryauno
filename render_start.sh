#!/bin/bash
# Render için start script

# Dosya yapısını göster (debug için)
echo "Dosya yapısı:"
ls -la
ls -la unu/

# Ana dizini göster
echo "Çalışma dizini: $(pwd)"

# Python sürümünü göster
echo "Python sürümü: $(python --version)"

# unu klasöründeki main.py dosyasını çalıştır
if [ -f "unu/main.py" ]; then
    echo "main.py dosyası bulundu: unu/main.py"
    # Botu başlat
    python unu/main.py
else
    echo "HATA: unu/main.py dosyası bulunamadı!"
    
    # Ana dizindeki main.py dosyasını kontrol et
    if [ -f "main.py" ]; then
        echo "Ana dizinde main.py bulundu, kopyalanıyor..."
        cp main.py unu/main.py
        python unu/main.py
    else
        echo "Hiçbir main.py dosyası bulunamadı!"
        exit 1
    fi
fi 