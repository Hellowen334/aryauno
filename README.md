# UNO Telegram Bot

Telegram üzerinde UNO oyunu oynamanızı sağlayan bir bot.

## Özellikler

- Türkçe dil desteği
- Çoklu oyuncu desteği
- Güvenli yapılandırma
- Rate limiting
- Hata yönetimi
- Otomatik kaydetme

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env` dosyasını oluşturun:
- `.env.example` dosyasını `.env` olarak kopyalayın
- Telegram API bilgilerinizi ekleyin
- Yönetici ID'lerinizi ekleyin

3. Botu çalıştırın:
```bash
python -m unu
```

## Güvenlik Önlemleri

- API anahtarları environment variables üzerinden yönetilir
- Rate limiting ile DDoS koruması
- Maksimum oyun ve oyuncu sınırlamaları
- Hata yönetimi ve loglama
- Sadece grup sohbetlerinde çalışır
- Kullanıcı başına oyun sınırlaması

## Komutlar

- `/new` - Yeni oyun başlat
- `/join` - Oyuna katıl
- `/start` - Oyunu başlat
- `/leave` - Oyundan ayrıl
- `/help` - Yardım menüsü

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: X'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın. 