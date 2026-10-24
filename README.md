# 🎙️ Arapça Telaffuz ve Konuşma Asistanı — Muallimun.Net (v40.0)

[![Sürüm](https://img.shields.io/badge/S%C3%BCr%C3%BCm-v40.0%20Gold%20Master-10b981?style=for-the-badge)](https://github.com/muallimun/arapca-telaffuz-asistani/releases)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3b82f6?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-eab308?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011%20%26%20Ak%C4%B1ll%C4%B1%20Tahta-8b5cf6?style=for-the-badge)](https://github.com/muallimun/arapca-telaffuz-asistani)
[![Web](https://img.shields.io/badge/Web-Muallimun.Net-ffd369?style=for-the-badge)](https://www.muallimun.com)

**Arapça Telaffuz ve Konuşma Asistanı**, İmam Hatip Liseleri, İlahiyat Fakülteleri, TÖMER ve bireysel Arapça öğrenenlerin en büyük ihtiyacı olan **doğru telaffuz (النطق الصحيح)**, **sarf / sülâsî kök-türev farkındalığı (الصرف والاشتقاق)**, **cümle akıcılığı** ve **karşılıklı konuşma (المحادثة والتكلم)** becerilerini geliştirmek amacıyla **Muallimun.Net** tarafından geliştirilmiş yapay zekâ destekli interaktif bir dil laboratuvarıdır.

---

## 🌟 Öne Çıkan Özellikler (v40.0)

### 🏛️ 1. Öğrenci Odaklı 2x2 Ana Giriş Ekranı (Dashboard) ve Kişiselleştirme
* **👤 Öğrenci / Kullanıcı Kaydı (`ayarlar.db`):** İlk açılışta öğrencinin adını ve soyadını kaydeder; ana ekranda öğrenciyi ismiyle karşılar, **Öğretmen Raporları**, **Excel (CSV)** çıktıları ve **Ödev `.ZIP`** karnelerine öğrenci adını otomatik işler.
* **📍 Kaldığım Yerden Devam Et & 🎯 Akıllı Öneri:** Öğrencinin son çalıştığı mod ve paketi hatırlar; günlük çalışma verisine göre kişisel telaffuz ve tekrar önerileri sunar.
* **👨‍🏫 Gizlenebilir Öğretmen Barı:** Öğrenci bilgisayarlarında Ayarlar üzerinden *"Ana Ekranda Öğretmen & Ölçme Araçları Barını Göster"* seçeneği kapatılarak arayüz %100 öğrenci odaklı hale getirilebilir.

### 🎯 2. Canlı Mahreç (Fonem), Kök Harf ve Hareke Koçu
* **Harf ve Mahreç Analizi:** Birbirine yakın mahreçli Arapça harfleri (`ص↔س`, `ط↔ت`, `ض↔د`, `ض↔ظ`, `ع↔ء/ا`, `ح↔ه`, `خ↔ح`, `غ↔ق`, `ق↔ك`, `ذ↔ز`, `ث↔س`, `ن↔ر`, `ل↔ر`, `ب↔م` vb.) harf düzeyinde hizalayarak yakalar ve ağız/boğazdaki doğru çıkış noktasını Türkçe tarif eder.
* **Kök Harf ve Vezin Koruma Kalkanı:**
  * Kısa kelimelerde tek bir kök harfin değişmesini (`نَحْلَة` [Arı] ➔ `رحلة` [Yolculuk]) yakalayarak yanlışlıkla doğru sayılmasını engeller ve hatalı kelimeyi **kırmızıyla** vurgular.
  * 4 harfli isimlerin 3 harfli fiil kalıbında okunmasını (`كِتَاب` ➔ `كتب`, `عَامِل` ➔ `عمل`) **Sarf Kalıbı / Vezin Farklılığı** olarak, 3 harfli ecvef fiillerdeki uzatma yutmalarını (`قَالَ` ➔ `قل`) ise **Med (Uzatma) Eksikliği** olarak ayrıştırır.
* **🔤 Pedagojik Hareke Rehberi:** Kelime ve cümlelerdeki *Fetha, Kesra, Damme, Şedde ve Cezim/Sükûn* sayılarını analiz ederek vokal farkındalığı sağlar.
* **🎙️ Canlı Mikrofon Çerçeve Parlaması (Green Glow):** Bip sesinden sonra kayıt başladığı anda kartın dış çerçevesi parlak yeşil renkte parlayarak öğrenciye görsel sinyal verir.

### 📖 3. Sarf Sözlüğü ve Sülâsî Kök Ailesi Keşif Atölyesi (`data/sozluk.db`)
* **Altıgen Sülâsî Kök Rozeti ve Tıklanabilir Türev Ağacı:** Görseli olmayan sözlük kelimelerinde kart üzerinde kelimenin 3 asli kök harfini (`ك ت ب` vb.) altıgen rozet içinde gösterir.
  * **İsimlerde:** *Müfret (Tekil)* ve *Cemî (Çoğul)* formlarını tıklayarak ayrı ayrı dinleme ve telaffuz etme.
  * **Fiillerde:** *Mâzî (Geçmiş)*, *Muzâri (Şimdiki/Geniş)* ve *Masdar* çekimlerini tıklayarak çalışma (üzerine gelindiğinde öğrenci dostu Türkçe terim açıklamaları / Tooltip açılır).
* **Kök Ailesi Keşif Penceresi:** 1.500+ sözlük maddesi arasında kök, kelime veya anlam araması yapma, **sütun başlıklarına tıklayarak A➔Z / Z➔A sıralama** ve aynı kökten türeyen tüm akraba kelimeleri tek ekranda inceleme.

### 🏠 4. Görselli Kelime Modu, Gölgeleme (Shadowing) ve SM-2 Akıllı Tekrar
* **📅 Günün 15 Tekrarı (SM-2 Spaced Repetition):** Unutulmaya yüz tutmuş veya zorlanılan kelimeleri bilimsel SM-2 aralıklı tekrar algoritmasıyla her gün otomatik seçer.
* **🗣️ Gölgeleme (Shadowing) Akıcılık Antrenmanı:** Referans sesin dalga boyunu (mavi) ve öğrencinin ses dalga boyunu (yeşil) alt alta çizerek hem **Telaffuz Doğruluğunu** hem de **Ritim / Süre Uyumunu (%)** ölçer.
* **Kadın / Erkek Referans Seslendirme ve Yavaş Okuma:** Tüm kelimeleri kadın (`ZariyahNeural`) veya erkek (`HamedNeural`) sesiyle normal ya da **🐢 %25 Yavaş** hızda dinleme.

### 💬 5. Günlük Diyaloglar (Muhâdesât) ve Rol Yapma (`data/diyaloglar.db`)
* **📖 Öğrenme Modu:** A1–C1 seviyelerindeki 60+ günlük hayat diyaloğunu satır satır vurgulamalı ve otomatik kaydırmalı olarak dinleme.
* **🎭 Ölçme / Canlandırma (Roleplay) Modu:** Diyalogdaki bir karakterin rolünü seçerek uygulamayla karşılıklı konuşma. Öğrencinin sırası geldiğinde Türkçe çeviri otomatik gizlenir (**`💡 Türkçe İpucu Göster`** butonuyla istenirse açılabilir), doğru okunan kelimeler anında **Yeşil** renkte açılır ve diyalog sonunda detaylı **📊 Konuşma Karnesi** verilir.

### 📜 6. Anahtar Cümleler (`data/cumleler.db`) ve 🎧 Dinle & Bul Sınav Merkezi
* **Kelime Kelime Renkli Cümle Analizi:** 7.950+ anahtar cümlede her kelimenin telaffuzunu ayrı ayrı değerlendirir; doğru kelimeleri yeşil, hatalı kelimeleri kırmızı renkle gösterir.
* **🎧 Dinle & Bul (İstimâ) Sınav Merkezi:** *Görselli Kelimeler, Sarf Sözlüğü, Anahtar Cümleler* veya *Diyaloglar* havuzundan **10, 20, 50 Soru** veya **♾️ Sınırsız** modda 4 şıklı sesli anlama sınavı yapar. Hazırlık ekranında **`▶️ SINAVI BAŞLAT`** butonuna basılmadan ses çalmaz; verilen cevaplar otomatik olarak SM-2 takvimine ve karneye işlenir.

### 🖨️ 7. Öğretmenler İçin A4 Yazılı Sınav, Karma Quiz ve "Ders Notu / Okuma Metni" PDF Üretici
* **Ayrık Havuzlu Yazılı Sınav Üretici:**
  * *Arapça ➔ Türkçe Yazma (0-50)*, *Türkçe ➔ Arapça Yazma (0-50)*, *Boşluk Doldurma (0-50)*, *2x2 Hizalı Çoktan Seçmeli Test (0-50)*, *Eşleştirme (0-30)* ve *Sarf Kök/Türev Tablosu (0-30)* soru sayılarını bağımsız `Spinbox` kontrolleriyle belirleme.
  * **`ar_to_tr_pool` ve `tr_to_ar_pool` Ayrık Havuz Algoritması:** 1. bölümde Arapçası sorulan bir kelimenin 2. bölümde Türkçesinin sorulmasını engelleyerek kopya ihtimalini ortadan kaldırır.
  * **🌟 Karma Sınav Modu:** Tek bir sınav kağıdında hem Kelime, hem Diyalog, hem de Cümle veritabanlarından aynı anda soru çekebilme.
  * **Kurumsal A4 Antet ve Ayrı Sayfada Cevap Anahtarı:** Okul/kurum logosu, *Adı Soyadı / Sınıfı / Tarih / Puan* anteti ve `page-break-before: always` CSS kuralıyla her zaman ayrı bir A4 sayfasına basılan **Öğretmen Cevap Anahtarı**.
* **📖 Ders Notu / Okuma Metni (Handout) PDF Üretici:**
  * Diyalog ve Cümle paketlerini sınav soruları olmadan temiz A4 okuma yaprağı olarak üretir.
  * **Harekeli / Harekesiz Gösterim** ve **3 Farklı Tercüme Yerleşimi** (*Yan Yana İki Sütun %50-%50*, *Alt Alta*, *Sonda Toplu Çeviri* veya *Sadece Arapça Okuma Metni*).

### 🛠️ 8. Yönetim & Paket Paneli (Admin) ve GitHub Otomatik Güncelleme
* **📋 Excel / Panodan Doğrudan Yapıştır (Clipboard Import):** Excel'den kopyalanan kelime, cümle veya diyalog satırlarını doğrudan yapıştırarak saniyeler içinde veritabanına ekleme ve **Detaylı Yükleme / Atlanan Satır Raporu**.
* **🖼️ Toplu Medya Klasörü Eşleştirici:** Bilgisayardaki bir klasör içinde bulunan görsel (`.jpg`, `.png`, `.webp`) ve ses (`.mp3`, `.wav`) dosyalarını kelime ID'sine veya Türkçe anlamına (`Arı` ➔ `ari.jpg`) göre otomatik eşleştirme.
* **🔤 Tüm Sütunlarda A➔Z / Z➔A Sıralama ve Çoklu Seçim (`Shift/Ctrl`):** Sütun başlıklarına tıklayarak sıralama ve çoklu seçimle yüzlerce kayda tek tıkla toplu CEFR seviyesi (`A1–C1`) atama.
* **🎧 Öğrenci Ses Kaydını Dinleme & 📦 Ödev `.ZIP` Paketleyici:** Raporlar ekranında öğrencinin zorlandığı kelimelerdeki gerçek ses kaydını (`.wav`) dinleme ve son 20 ses kaydıyla başarı karnesini tek bir `.ZIP` ödev paketinde toplama.
* **🔄 GitHub Otomatik Güncelleme Merkezi:** Uygulama açılışında arka planda GitHub deposunu kontrol eder; yeni sürüm çıktığında sürüm notlarını (changelog) gösterir ve tek tıkla indirip günceller.

---

## 🚀 Kurulum ve Çalıştırma

### 1. Gereksinimler
* **İşletim Sistemi:** Windows 10 veya Windows 11 (64-bit)
* **Python:** Python 3.10, 3.11 veya 3.12
* **Donanım:** Sesli telaffuz değerlendirmesi için mikrofon ve hoparlör/kulaklık

### 2. Kaynak Koddan Kurulum (PowerShell)

~~~powershell
# 1. Depoyu bilgisayarınıza klonlayın
git clone https://github.com/muallimun/arapca-telaffuz-asistani.git
cd arapca-telaffuz-asistani

# 2. Sanal ortam (.venv) oluşturun ve etkinleştirin
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# 4. Uygulamayı başlatın
py app.py
~~~

### 3. Otomatik Birim Testlerini Çalıştırma (`15/15`)
Arapça NLP, kök harf koruma kalkanı (`نَحْلَة` vs `رحلة`), vezin ayrımı (`كِتَاب` vs `كتب`), ardışık tekrar tekilleştirme (`نحلة نحلة` ➔ `نحلة`), mahreç koçu ve SM-2 algoritmasını doğrulamak için:

~~~powershell
py tests/test_arabic_nlp.py
~~~

---

## 📂 Proje Klasör Yapısı

~~~text
arapca-telaffuz-asistani/
├── app.py                      # Ana uygulama, 2x2 Dashboard ve pencere yöneticisi
├── version.json                # GitHub otomatik güncelleme sürüm ve changelog dosyası
├── requirements.txt            # Python bağımlılık listesi
├── LICENSE                     # MIT Açık Kaynak Lisansı
├── SECURITY.md                 # Güvenlik politikası ve bildirim rehberi
├── CONTRIBUTING.md             # Katkıda bulunma ve içerik geliştirme rehberi
├── core/
│   ├── config.py               # Sabitler, tema paletleri ve GitHub depo yapılandırması
│   ├── arabic_nlp.py           # RTL şekillendirici, kök harf/vezin koruyucu ve mahreç koçu
│   ├── database.py             # SQLite oturum yöneticisi, SM-2, Excel pano ve medya eşleştirici
│   ├── dictionary.py           # Sarf sözlüğü (sozluk.db) ve sülâsî kök ailesi motoru
│   ├── audio_engine.py         # Faster-Whisper STT, Edge-TTS ve mikrofon kayıt motoru
│   └── updater.py              # GitHub otomatik sürüm kontrolü ve kurulum yöneticisi
├── ui/
│   ├── dialogue_mode.py        # Diyalog öğrenme ve karşılıklı canlandırma (Roleplay) modülü
│   ├── dialogs.py              # Sınav/Ders Notu üretici, Dinle & Bul, Shadowing, Raporlar ve Kılavuz
│   ├── admin_panel.py          # Birleşik Yönetim Paneli, Excel yapıştırma ve kalite denetimi
│   └── muallimun_logo.png      # Kurumsal uygulama logosu
├── data/                       # SQLite veritabanları (kelimeler.db, diyaloglar.db, cumleler.db, sozluk.db, ayarlar.db)
├── assets/                     # Görseller (categories/), referans sesler ve TTS önbelleği (tts_cache/)
├── recordings/                 # Öğrenci telaffuz ses kayıtları (.wav)
└── tests/
    └── test_arabic_nlp.py      # 15 otomatik birim testi
~~~

---

## ⌨️ Pratik Klavye Kısayolları

| Kısayol Tuşu | İşlevi |
| :--- | :--- |
| **`Boşluk (Space)`** | Kelime, Cümle ve Canlandırma modlarında ses kaydını başlatır veya durdurur |
| **`Sağ Ok (▶)`** | Sonraki kelime veya cümle kartına geçer |
| **`Sol Ok (◀)`** | Önceki kelime veya cümle kartına geçer |
| **`F1`** | Kapsamlı Kullanım Kılavuzunu ve 7 Adımlı Başlangıç Turunu açar |

---

## 📜 Lisans ve Güvenlik

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Güvenlik bildirimleri ve veri gizliliği ilkeleri için [SECURITY.md](SECURITY.md) dosyasını inceleyebilirsiniz.

---

## 🌐 İletişim ve Katkı

* **Geliştirici & Eğitim Portalı:** [Muallimun.Net](https://www.muallimun.com)
* **GitHub Deposu:** [github.com/muallimun/arapca-telaffuz-asistani](https://github.com/muallimun/arapca-telaffuz-asistani)
* **Sorun Bildirimi & Öneriler:** [GitHub Issues](https://github.com/muallimun/arapca-telaffuz-asistani/issues)