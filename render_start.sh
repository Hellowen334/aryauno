#!/bin/bash
# Render için start script

# Dosya yapısını göster (debug için)
echo "Dosya yapısı:"
ls -la

# Ana dizini göster
echo "Çalışma dizini: $(pwd)"

# Python sürümünü göster
echo "Python sürümü: $(python --version)"

# main.py dosyasını bul
MAIN_PY=$(find . -name "main.py" | head -n 1)

if [ -z "$MAIN_PY" ]; then
    echo "HATA: main.py dosyası bulunamadı!"
    exit 1
else
    echo "main.py dosyası bulundu: $MAIN_PY"
    # Botu başlat
    python $MAIN_PY
fi 