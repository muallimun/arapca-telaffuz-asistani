# 🛡️ Güvenlik ve Veri Gizliliği Politikası (Security Policy)

**Muallimun.Net — Arapça Telaffuz ve Konuşma Asistanı** projesinin güvenliğine ve öğrenci/öğretmen verilerinin gizliliğine büyük önem veriyoruz.

## 📌 Desteklenen Sürümler

Aşağıdaki sürümler aktif olarak güvenlik ve kararlılık güncellemeleri almaktadır:

| Sürüm | Destek Durumu |
| :--- | :--- |
| **v40.x (Gold Master)** | ✅ Aktif Destekleniyor |
| **< v40.0** | ❌ Desteklenmiyor (Lütfen uygulama içi `🔄 Güncelle` aracını kullanın) |

## 🔒 Öğrenci Ses ve Veri Gizliliği İlkeleri

1. **Yerel Ses İşleme (Offline STT):** Öğrencilerin mikrofona okudukları ses kayıtları (`recordings/*.wav`), bilgisayar üzerinde yerel olarak çalışan **Faster-Whisper** modeli tarafından analiz edilir; hiçbir harici sunucuya gönderilmez.
2. **Yerel Veritabanı:** Öğrenci ismi, başarı puanları, rozetler ve SM-2 tekrar takvimi tamamen kullanıcının kendi bilgisayarındaki yerel SQLite veritabanlarında (`data/*.db`) saklanır.
3. **Güvenli Güncelleme:** Otomatik güncelleme motoru (`core/updater.py`) yalnızca resmi `https://github.com/muallimun/arapca-telaffuz-asistani` deposu üzerinden HTTPS protokolü ile sürüm kontrolü yapar.

## 🚨 Güvenlik Açığı Bildirimi (Reporting a Vulnerability)

Uygulamada bir güvenlik açığı veya kritik bir hata tespit ederseniz:
1. Lütfen [GitHub Issues](https://github.com/muallimun/arapca-telaffuz-asistani/issues) üzerinden veya [www.muallimun.com](https://www.muallimun.com) iletişim kanalları aracılığıyla bize bildirin.
2. Bildiriminize işletim sistemi sürümünüzü, Python sürümünüzü ve varsa `uygulama.log` dosyasındaki ilgili hata satırını ekleyin.
3. Bildirimler en geç **48 saat** içinde incelenerek gerekli yama yeni sürümle yayınlanır.