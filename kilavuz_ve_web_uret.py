# -*- coding: utf-8 -*-
"""
kilavuz_ve_web_uret.py — Muallimun.Net Arapça Telaffuz ve Konuşma Asistanı
- Mobil Uyumlu (Responsive) + Windows Bilgisayar Bilgilendirmeli Web Tanıtım Sayfası
- %100 Özelleştirilebilir Açık İçerik Motoru Vurgulu A4 PDF Kullanım Kılavuzu
- Mükerrer Görseller (Screenshot_22, 23, 26, 27) Çıkarılmış (27 Özgün Ekran Görüntüsü)
- Setup.exe İçin QR Kod Kullanılmaz (Sadece PDF İçinde YouTube ve Web Sayfası QR Kodu Yer Alır)
Çalıştırma: .\.venv\Scripts\python.exe kilavuz_ve_web_uret.py
"""

import os
import sys
import base64
import shutil
import subprocess
import urllib.parse
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import filedialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "Kilavuz_ve_Tanitim")
IMG_OUT_DIR = os.path.join(OUT_DIR, "images")
os.makedirs(IMG_OUT_DIR, exist_ok=True)

SETUP_DOWNLOAD_URL = "https://github.com/muallimun/arapca-telaffuz-asistani/releases/latest/download/Arapca_Telaffuz_Asistani_Setup.exe"
GITHUB_REPO_URL = "https://github.com/muallimun/arapca-telaffuz-asistani"
WEBSITE_URL = "https://www.muallimun.com"
WEB_GUIDE_URL = "https://arapca.muallimun.net/arapca-telaffuz-asistani/"
YOUTUBE_VIDEO_ID = "vqttBAoov00"
YOUTUBE_SHORT_URL = f"https://youtu.be/{YOUTUBE_VIDEO_ID}"
YOUTUBE_EMBED_URL = f"https://www.youtube.com/embed/{YOUTUBE_VIDEO_ID}?rel=0"

# Mükerrer olduğu tespit edilen ve kılavuzdan/web sayfasından çıkarılan görseller:
EXCLUDED_DUPLICATE_SCREENSHOTS = {22, 23, 26, 27}


def find_screenshots_dir() -> str:
    candidates = [
        IMG_OUT_DIR,
        BASE_DIR,
        os.path.join(BASE_DIR, "screenshots"),
        os.path.join(BASE_DIR, "ekranlar"),
        os.path.join(BASE_DIR, "resimler"),
        os.path.dirname(BASE_DIR),
    ]
    for cand in candidates:
        if os.path.exists(os.path.join(cand, "Screenshot_1.png")):
            return cand

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected = filedialog.askdirectory(title="Screenshot_1.png .. Screenshot_31.png Görsellerinin Bulunduğu Klasörü Seçin")
    root.destroy()
    return selected or BASE_DIR


def img_to_data_uri(path: str) -> str:
    if not path or not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower().replace(".", "")
    mime = "image/png" if ext == "png" else "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def generate_qr_code_png(target_url: str, save_path: str) -> str:
    try:
        encoded = urllib.parse.quote(target_url, safe="")
        api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=280x280&ecc=M&margin=8&data={encoded}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp, open(save_path, "wb") as out_f:
            out_f.write(resp.read())
    except Exception as ex:
        print(f"⚠️ QR kod indirme uyarısı ({target_url}): {ex}")
    return img_to_data_uri(save_path)


print("=" * 72)
print("📘 ARAPÇA TELAFFUZ ASİSTANI — MOBİL UYUMLU WEB & PDF KILAVUZ ÜRETİCİ")
print("=" * 72)
print(f"🗑️ Çıkarılan mükerrer görseller: Screenshot_22.png, Screenshot_23.png, Screenshot_26.png, Screenshot_27.png")

SCREENSHOTS_DIR = find_screenshots_dir()
icon_path = os.path.join(BASE_DIR, "ui", "app_icon.png")
if not os.path.exists(icon_path):
    alt_ico = os.path.join(BASE_DIR, "assets", "muallimun_logo.png")
    if os.path.exists(alt_ico):
        icon_path = alt_ico

if os.path.exists(icon_path):
    dst_ico = os.path.join(IMG_OUT_DIR, "app_icon.png")
    if os.path.normcase(icon_path) != os.path.normcase(dst_ico):
        shutil.copy2(icon_path, dst_ico)

icon_uri = img_to_data_uri(icon_path)

# Yalnızca YouTube Videosu ve Web Tanıtım Sayfası için QR Kod (Setup.exe için QR kod üretilmez)
qr_yt_path = os.path.join(IMG_OUT_DIR, "qr_youtube.png")
qr_web_path = os.path.join(IMG_OUT_DIR, "qr_web_sayfasi.png")
qr_yt_uri = generate_qr_code_png(YOUTUBE_SHORT_URL, qr_yt_path)
qr_web_uri = generate_qr_code_png(WEB_GUIDE_URL, qr_web_path)

# Klasörde mükerrer görseller kalmışsa otomatik temizle
for dup_no in EXCLUDED_DUPLICATE_SCREENSHOTS:
    dup_file = os.path.join(IMG_OUT_DIR, f"Screenshot_{dup_no}.png")
    if os.path.exists(dup_file):
        try:
            os.remove(dup_file)
            print(f"🧹 Mükerrer dosya temizlendi: {dup_file}")
        except Exception:
            pass

sc_uris = {}
found_count = 0
for i in range(1, 32):
    if i in EXCLUDED_DUPLICATE_SCREENSHOTS:
        continue
    fname = f"Screenshot_{i}.png"
    src_p = os.path.join(SCREENSHOTS_DIR, fname)
    if os.path.exists(src_p):
        dst_p = os.path.join(IMG_OUT_DIR, fname)
        if os.path.normcase(src_p) != os.path.normcase(dst_p):
            shutil.copy2(src_p, dst_p)
        sc_uris[i] = img_to_data_uri(src_p)
        found_count += 1
    else:
        sc_uris[i] = ""
        print(f"⚠️ Uyarı: {fname} bulunamadı ({src_p})")

print(f"✅ {found_count}/27 özgün ekran görüntüsü ve uygulama ikonu yüklendi.")


# ==============================================================================
# BÖLÜM VE EKRAN VERİ YAPISI (27 ÖZGÜN EKRAN GÖRÜNTÜSÜ + ÖZELLEŞTİRİLEBİLİR MOTOR VURGUSU)
# ==============================================================================
CHAPTERS = [
    {
        "num": "1",
        "id": "bolum-1",
        "title": "Uygulamanın Amacı, %100 Özelleştirilebilir İçerik Motoru ve İlk Açılış",
        "subtitle": "Kullanıcının Kendi Müfredatını, Kelime, Diyalog ve Cümlelerini Kolayca Ekleyebildiği Açık Eğitim Platformu",
        "intro": (
            "Arapça Telaffuz ve Konuşma Asistanı; sadece sabit verilerle sınırlı bir program değil, "
            "öğretmenlerin ve öğrencilerin içeriğini %100 özelleştirebildiği dinamik bir konuşma (muhâdese), sarf (kök/türev) "
            "ve mahreç laboratuvarıdır. Uygulama kurulduğunda hemen çalışmaya başlanabilmesi için içinde zengin bir "
            "başlangıç veri setiyle (örnek kelimeler, sarf sözlüğü, günlük diyaloglar ve anahtar cümleler) birlikte gelir. "
            "Ancak uygulamanın asıl gücü; içinde hiçbir veri olmasa bile kullanıcının hiçbir kodlama bilmeden kendi ders "
            "kitabını, kendi kelimelerini, diyaloglarını, cümlelerini, görsellerini ve ses kayıtlarını dakikalar içinde "
            "sisteme ekleyebilmesidir."
        ),
        "highlights": [
            ("🛠️ %100 Özelleştirilebilir Açık İçerik Motoru:", "Hazır gelen içerikler yalnızca başlangıç örneğidir. Kullanıcı mevcut verileri dilediği gibi düzenleyebilir, silebilir veya Excel'den kopyala-yapıştır (Ctrl+V), CSV/JSON/ZIP ve mikrofon kaydıyla kendi özel müfredatını sıfırdan oluşturabilir."),
            ("🎙️ Çevrimdışı Yapay Zekâ (Faster-Whisper):", "Sonradan eklediğiniz yeni kelime ve cümleler de dahil olmak üzere tüm ses analizleri tamamen bilgisayar içinde (çevrimdışı) gerçekleşir."),
            ("🔊 Otomatik Referans Seslendirme ve Önbellek:", "Sisteme sadece Arapça metin ekleseniz bile uygulama bunu Kadın/Erkek sinirsel sesleriyle otomatik seslendirir veya kendi sesinizi kaydetmenize izin verir."),
            ("🔒 Tek Örnek (Single Instance) Koruması:", "Windows bilgisayarlarda ve akıllı tahtalarda simgeye üst üste tıklansa bile ikinci kopya açılmaz; açık pencere öne getirilir.")
        ],
        "screens": [
            {
                "sc_no": 31,
                "title": "7 Adımlı İnteraktif Başlangıç ve Ekran Tanıtım Turu (Onboarding)",
                "desc": "Uygulama ilk kez çalıştırıldığında kullanıcıyı 7 adımlı interaktif bir rehber karşılar. Bu turda uygulamanın temel amacı, Ana Sayfa, Kelime Modu, Sarf Sözlüğü, Diyalog/Roleplay, Canlı Mahreç Koçu ve Öğretmen İçerik/Sınav Araçları adım adım tanıtılır.",
                "tips": [
                    "Alt kısımdaki 'Bir daha açılışta gösterme' kutusu işaretlenerek tur tamamlandığında sonraki açılışlarda doğrudan ana ekrana geçilir.",
                    "İstenildiği zaman üst menüdeki ℹ️ veya 📖 Kılavuz penceresinden '👋 7 Adımlı Başlangıç Turunu Başlat' butonuyla tekrar açılabilir."
                ]
            },
            {
                "sc_no": 1,
                "title": "Öğrenci / Kullanıcı Profili Kayıt Penceresi",
                "desc": "Başlangıç turunun hemen ardından öğrenci veya öğretmenin adını kaydedebileceği karşılama penceresi açılır. Girilen isim ayarlar veritabanına (ayarlar.db) kaydedilir.",
                "tips": [
                    "Buraya girilen isim; Ana Sayfa karşılama başlığında, Gelişim Karnesinde ve öğretmene gönderilen '.ZIP Ödev Paketi' raporlarında yer alır.",
                    "Kullanıcı adını daha sonra değiştirmek için Ana Sayfanın sağ üst köşesindeki '👤 İsim ✏️' rozetine tıklamak yeterlidir."
                ]
            },
            {
                "sc_no": 30,
                "title": "Uygulama İçi Kapsamlı Kullanım Rehberi (Kısayol: F1)",
                "desc": "Klavyeden F1 tuşuna veya üst çubuktaki 📖 simgesine basıldığında açılan 8 bölümlük uygulama içi kılavuz ekranıdır. İnternet bağlantısı gerektirmeden tüm modüllerin kullanımını ve klavye kısayollarını açıklar.",
                "tips": [
                    "Sağ üsttekiℹ️ (Info) butonuna tıklayarak ayrıca YouTube tanıtım videosuna, Web kılavuz sayfasına ve bu PDF kitapçığına doğrudan ulaşabilirsiniz."
                ]
            }
        ]
    },
    {
        "num": "2",
        "id": "bolum-2",
        "title": "Ana Giriş Ekranı (2x2 Öğrenci Odaklı Çalışma Merkezi)",
        "subtitle": "Canlı İçerik Sayaçları, Günlük Seri (Streak) Takibi, Akıllı Koç Önerisi ve Odaklanma Modu",
        "intro": (
            "Ana Sayfa ekranı; öğrencinin karmaşık menüler arasında kaybolmadan tek tıkla çalışmaya başlayabilmesi "
            "için 2x2 modül ızgarası şeklinde tasarlanmıştır. Kartların üzerindeki paket ve içerik sayıları sabit "
            "değildir; kullanıcı yeni paketler ekledikçe veya özelleştirdikçe veritabanından canlı olarak güncellenir."
        ),
        "highlights": [
            ("📍 Kaldığım Yerden Devam Et:", "Uygulama son çalışılan modu ve paketi hafızada tutar; yeşil butonla tek tıkla son çalışmaya dönülür."),
            ("🎯 Akıllı Koç Önerisi:", "Öğrencinin hata istatistiklerini analiz ederek günlük ısınma tekrarı veya '🎯 Zayıflar' listesine yönlendirme yapar."),
            ("👨‍🏫 Gizlenebilir Öğretmen Barı:", "En alttaki şerit; A4 Yazılı Sınav & Ders Notu Üretici, Gelişim Karnesi ve Yönetim Paneline doğrudan erişim sağlar."),
            ("◧ Odaklanma Modu:", "Üst çubuktaki 'Paneli Gizle' butonuyla sağ panel kapatılarak akıllı tahtalarda tam ekran çalışma alanı elde edilir.")
        ],
        "screens": [
            {
                "sc_no": 3,
                "title": "Ana Giriş Ekranı — Standart Görünüm (Sağ Panel Açık)",
                "desc": "Sol tarafta 4 ana eğitim modülü (Görselli Kelimeler, Sarf Sözlüğü, Günlük Diyaloglar, Anahtar Cümleler), sağ tarafta ise Yönetim Paneli, Tüm Ayarlar, Canlı Mahreç Koçu ve açılır-kapanır akordiyon menüler yer alır.",
                "tips": [
                    "Her modül kartının üzerinde veritabanınızda o an yüklü olan güncel paket, kelime, sözlük maddesi, diyalog ve cümle sayıları canlı olarak listelenir."
                ]
            },
            {
                "sc_no": 2,
                "title": "Ana Giriş Ekranı — Tam Ekran Odaklanma Modu (Sağ Panel Gizli)",
                "desc": "Üst çubuktaki '◧ Paneli Gizle' butonuna basıldığında sağ panel kapanır ve çalışma kartları tüm ekran genişliğine yayılır.",
                "tips": [
                    "Panel gizliyken bile yapılan telaffuz analizlerinin özeti kartın alt kısmında satır içi bilgi çubuğu olarak gösterilir."
                ]
            }
        ]
    },
    {
        "num": "3",
        "id": "bolum-3",
        "title": "Görselli Kelime Modu ve Canlı Mahreç / Kök Harf Analizi",
        "subtitle": "Görsel Hafıza, Kadın/Erkek Referans Sesler, SM-2 Akıllı Tekrar ve Kök Harf Koruma Kilidi",
        "intro": (
            "Kelime Modu; görsel destekli temel kelime paketlerini, tematik sözlük paketlerini ve kullanıcının "
            "kendi eklediği özel kelime paketlerini sesli olarak çalışma imkânı sunar. Öğrenci önce kelimenin "
            "kadın veya erkek referans sesini dinler, ardından '🎤 BAŞLA VE KONUŞ' butonuna basarak mikrofona okur."
        ),
        "highlights": [
            ("📅 Günün 15 Tekrarı (SM-2):", "Bilimsel aralıklı tekrar motoru; zorlanılan, favoriye eklenen veya tekrar günü gelen 15 kelimeyi otomatik seçer."),
            ("🛡️ Kök Harf Koruma Kilidi:", "Kısa kelimelerde tek bir kök harfin değişmesi anlamı değiştirdiği için (نَحْلَة yerine تحلى okunması) hatalı telaffuzun 'Doğru' sayılmasını engeller."),
            ("🔄 Ardışık Tekrar Tekilleştirici:", "Öğrenci kelimeyi peş peşe iki kez okusa bile ('نحلة نحلة' ➔ 'نحلة') sistem bunu otomatik tekilleştirir."),
            ("🎧 Sesimi Dinle & Gölgele:", "Öğrenci kendi kaydını anında dinleyebilir veya dalga boyu grafiğiyle gölgeleme antrenmanı yapabilir.")
        ],
        "screens": [
            {
                "sc_no": 4,
                "title": "Görselli Kelime Kartı ve Hareke & Vokal Rehberi",
                "desc": "Hayvanlar paketindeki 'نَحْلَةٌ (Arı)' kartı. Üst barda Seviye (A1-C1), Paket seçimi, Günün 15 Tekrarı, Dinle & Bul, Tekrarım ve Zayıflar butonları; kart üzerinde ise Tekrar Listeme Ekle, Öğrendim, Seviye etiketi, Kadın/Erkek ses butonları ve Gölgele aracı yer alır.",
                "tips": [
                    "Sağ paneldeki '🎯 HAREKE & VOKAL REHBERİ', kelimedeki Fetha, Kesra, Damme, Şedde ve Sükûn sayısını göstererek kısa harekelerin uzatılmaması konusunda ön rehberlik yapar."
                ]
            },
            {
                "sc_no": 28,
                "title": "Canlı Mahreç ve Harf/Kök Değişimi Yakalama Örneği (Kırmızı Vurgu)",
                "desc": "Öğrenci 'نَحْلَة' kelimesini okurken son harfi değiştirerek 'تحلى' şeklinde telaffuz ettiğinde; sistem doğruluğu %53'e düşürür, '❌ TEKRAR DENE' uyarısı verir ve sağ paneldeki Canlı Mahreç Koçunda hedef kelimeyi kırmızı kutu içinde vurgular.",
                "tips": [
                    "Kayıt yapıldıktan sonra aktifleşen '🎧 Sesimi Dinle' butonuyla öğrenci kendi ses kaydını dinleyip referans sesle karşılaştırabilir."
                ]
            }
        ]
    },
    {
        "num": "4",
        "id": "bolum-4",
        "title": "Sarf Sözlüğü ve Sülâsî Kök Ailesi Keşif Atölyesi",
        "subtitle": "Altıgen Kök Rozeti, Türev Ağacı, Sütun Sıralama ve Özelleştirilebilir Sözlük Veritabanı",
        "intro": (
            "Arapçada kelimeleri kalıcı olarak öğrenmenin anahtarı, kelimenin türediği 3 asli harfi (Sülâsî Kök) "
            "ve aynı kökten türeyen akraba kelimeleri (İştikak Ailesi) tanımaktır. Uygulama ile birlikte gelen "
            "hazır Sarf Sözlüğü (sozluk.db), isimlerin Müfret/Cemî ve fiillerin Mâzî/Muzâri/Masdar çekimlerini "
            "otomatik olarak tematik kategorilere ayırır; ayrıca kullanıcı kendi JSON sözlük dosyalarını da sisteme yükleyebilir."
        ),
        "highlights": [
            ("🔷 Altıgen Sülâsî Kök Rozeti:", "Kelimenin 3 asli kök harfini (Örn: س ل م veya ك ت ب) görsel bir altıgen rozet içinde sunar."),
            ("🔤 Sütun Başlığıyla Sıralama:", "Kök, Tür, Müfret/Mâzî, Cemî/Muzâri ve Türkçe sütun başlıklarına tıklayarak A➔Z (▲) veya Z➔A (▼) sıralama yapılır."),
            ("🌿 Kök Ailesi (İştikak) Ağacı:", "Seçilen kelimenin sağ panelinde aynı sülâsî kökten türeyen diğer akraba kelimeler listelenir."),
            ("🎤 Kartta Telaffuz Çalışma:", "Seçilen sözlük maddesi tek tıkla Kelime Moduna aktarılarak sesli telaffuz pratiği yapılabilir.")
        ],
        "screens": [
            {
                "sc_no": 7,
                "title": "Sarf Sözlüğü ve Sülâsî Kök Ailesi Atölyesi Ekranı",
                "desc": "Üst kısımda anlık kök/kelime/anlam arama kutusu, Tür (isim/fiil) ve Tematik Kategori (🏥 Sağlık, 🍽️ Yemek, ✈️ Seyahat, 🎓 Eğitim vb.) filtreleri yer alır. Sağ panelde seçili kelimenin altıgen kök rozeti, sesli çekim butonları ve '🎤 Bu Kelimeyi Kartta Çalış' butonu bulunur.",
                "tips": [
                    "Arama kutusuna boşluklu veya bitişik olarak 3 kök harfi (örn: 'س ل م' veya 'سلم') yazdığınızda o köke ait tüm türevler anında filtrelenir."
                ]
            }
        ]
    },
    {
        "num": "5",
        "id": "bolum-5",
        "title": "Günlük Diyaloglar (Muhâdesât) ve Karşılıklı Rol Yapma (Roleplay)",
        "subtitle": "Öğrenme Modu, Canlı Diyalog Canlandırma ve Kendi Diyalog Senaryolarınızı Ekleme İmkanı",
        "intro": (
            "Diyalog Modu; öğrencinin günlük hayatta veya ders kitabındaki ünitelerde geçen diyaloglarda "
            "akıcı konuşma pratiği yapmasını sağlar. Hazır gelen diyalogların yanı sıra öğretmenler kendi "
            "diyalog metinlerini Excel'den yapıştırarak veya JSON/CSV olarak ekleyebilir. Modül '📖 Öğrenme Modu' "
            "ve '🎭 Ölçme / Canlandırma (Roleplay) Modu' olmak üzere iki alt modda çalışır."
        ),
        "highlights": [
            ("📖 Öğrenme Modu:", "'▶️ Diyaloğun Tümünü Oynat' ile tüm diyalog satır satır vurgulanarak seslendirilir; her satır tekil olarak çalışılabilir."),
            ("🎭 Ölçme / Canlandırma (Roleplay):", "Öğrenci bir karakteri seçer; karşı rolü bilgisayar seslendirir, sıra öğrenciye geldiğinde mikrofon otomatik açılır."),
            ("🟢 Kademeli Kelime Açma:", "Canlandırma sırasında öğrencinin doğru söylediği kelimeler anında yeşil renkte açılır."),
            ("📊 Diyalog Konuşma Karnesi:", "Canlandırma sonunda cümle bazlı başarı karnesi sunulur ve tek tıkla diğer role geçiş yapılabilir.")
        ],
        "screens": [
            {
                "sc_no": 5,
                "title": "Diyalog Modu — Sohbet Balonları ve Satır İçi Kontroller",
                "desc": "[A1] Tanışmak (التَّعَارُفُ) diyaloğu. Konuşmacıların cinsiyetine göre (Ömer: Erkek sesi, Deniz: Kadın sesi) otomatik ses ataması yapılır. Sağ üstten Hareke, Türkçe çeviri ve yazı boyutu (A- / A+ Punto) anlık olarak ayarlanabilir.",
                "tips": [
                    "Canlandırma (Roleplay) modunda öğrencinin kendi rolüne ait Arapça metin gizlenir; ihtiyaç duyulursa '💡 Türkçe İpucu Göster' butonuna basılabilir."
                ]
            }
        ]
    },
    {
        "num": "6",
        "id": "bolum-6",
        "title": "Anahtar Cümleler Modu ve Gölgeleme (Shadowing) Antrenmanı",
        "subtitle": "Seviyelendirilmiş Cümle Havuzu, Kelime Bazlı Renkli Doğruluk Analizi ve Dalga Boyu Ritmi",
        "intro": (
            "Cümle Modu; A1'den C1'e kadar seviyelendirilmiş hazır cümleler veya kullanıcının kendi eklediği "
            "cümle paketleri üzerinde telaffuz ve cümle kurma pratiği sunar. Öğrenci cümleyi seslendirdiğinde "
            "sistem cümleyi kelime kelime ayrıştırır; doğru okunan kelimeleri yeşil, hatalı okunan kelimeleri "
            "kırmızı renkte ekrana yansıtır."
        ),
        "highlights": [
            ("🙈 Arapçayı Gizle:", "Arapça cümle gizlenerek öğrencinin yalnızca Türkçe anlamdan hareketle Arapça cümleyi kurması sağlanır."),
            ("🗣️ Gölgeleme (Shadowing):", "Referans sesin dalga zarfı (mavi) ile öğrencinin ses dalga zarfını (yeşil) 48 barlık grafikte alt alta karşılaştırır."),
            ("🎵 Ritim ve Tempo Puanı:", "Gölgeleme modunda telaffuz doğruluğunun (%65) yanında konuşma süresi ve ritim uyumu (%35) da puanlanır."),
            ("📐 Piksel Duyarlı RTL Hizalama:", "Uzun Arapça cümleler ekran genişliğine göre doğal durak noktalarından otomatik bölünür.")
        ],
        "screens": [
            {
                "sc_no": 6,
                "title": "Anahtar Cümleler Modu Ekranı",
                "desc": "Filtre (Tümü, 📅 Günün 15 Tekrarı, Favoriler, Öğrendiklerim, Zorlandıklarım) ve Seviye (A1-C1) seçimi, cümle numarasına doğrudan gitme kutusu ('53 Git') ve kelime bazlı değerlendirme alanı.",
                "tips": [
                    "Numara kutusuna istediğiniz cümle numarasını yazıp Enter tuşuna basarak cümleler arasında anında geçiş yapabilirsiniz."
                ]
            },
            {
                "sc_no": 29,
                "title": "Gölgeleme (Shadowing) Akıcılık ve Ritim Antrenmanı Penceresi",
                "desc": "'🎬 Gölgelemeyi Başlat' butonuna basıldığında önce referans ses çalınır ve mavi dalga grafiği çizilir; hemen ardından bip sesiyle mikrofon açılır ve öğrenci beklemeden aynı hız ve tonlamayla cümleyi tekrar eder.",
                "tips": [
                    "Antrenman sonunda hem '🔊 Referansı Dinle' hem de '🎧 Sesimi Dinle' butonlarıyla iki sesin ritim farkı dinlenebilir."
                ]
            }
        ]
    },
    {
        "num": "7",
        "id": "bolum-7",
        "title": "Sağ Panel: Canlı Mahreç Koçu ve Doğal Konumlu Akordiyon Menüler",
        "subtitle": "35+ Mahreç Çifti Matrisi, Hızlı Ayarlar ve İstatistik/Kayıt Yönetimi",
        "intro": (
            "Ekranın sağ tarafında yer alan panel, öğrencinin çalışırken ihtiyaç duyduğu tüm rehberlik ve kontrol "
            "araçlarını tek bir merkezde toplar. Üstte Canlı Mahreç & Hareke Koçu geniş bir alanda yer alırken, "
            "altta yer kaplamaması için açılır-kapanır (akordiyon) yapıda Hızlı Ayarlar ve İstatistikler bulunur."
        ),
        "highlights": [
            ("🎯 35+ Fonem ve Mahreç Matrisi:", "Boğaz (ع-ء, ح-ه), kalın-ince (ص-س, ط-ت, ض-د, ق-ك), peltek (ث-س, ذ-ز, ظ-ز) ve akıcı harf (ن-ر, ل-ن) karışıklıklarını yakalar."),
            ("📏 Med ve Sarf Kalıbı Ayrımı:", "3 harfli kelimelerdeki med yutmalarını (قَالَ ➔ قل) ve 4 harfli isimlerin fiile dönüşmesini (كِتَاب ➔ كتب) ayrı ayrı teşhis eder."),
            ("⚡ Hızlı Ayarlar Akordiyonu:", "Eller Serbest Mod, %25 Yavaş Seslendirme, Otomatik İlerleme ve Rastgele Sıra tek tıkla açılıp kapatılır."),
            ("📊 İstatistik & Kayıt Akordiyonu:", "Mod bazlı başarı yüzdesini gösterir ve biriken .wav kayıtlarını tek tıkla temizler.")
        ],
        "screens": [
            {
                "sc_no": 24,
                "title": "Hızlı Ayarlar Akordiyon Menüsü (Açık Görünüm)",
                "desc": "Ayarlar penceresine gitmeden tek tıkla Eller Serbest Mod (Otomatik Kayıt), Yavaş Seslendirme (%25), Geçişte Otomatik Seslendir, Doğru Bilince Otomatik İlerle, Rastgele Sıra ve Ses Tercihi değiştirilebilir.",
                "tips": [
                    "'🙌 Eller Serbest Mod' açıldığında kart değişir değişmez önce referans ses çalar, ardından bip sesiyle mikrofon otomatik açılır."
                ]
            },
            {
                "sc_no": 25,
                "title": "İstatistikler & Kayıtlar Akordiyon Menüsü (Açık Görünüm)",
                "desc": "Aktif moda ait Doğru, Yanlış ve Başarı yüzdesini gösterir. '🔄 Sıfırla' ile istatistikler sıfırlanabilir, '🧹 Kayıtları Temizle' ile recordings/ klasöründeki ses dosyaları temizlenebilir.",
                "tips": [
                    "Buton üzerinde kayıt klasöründe kaç adet .wav dosyası bulunduğu ve kaç MB yer kapladığı canlı olarak yazar."
                ]
            }
        ]
    },
    {
        "num": "8",
        "id": "bolum-8",
        "title": "Dinle & Bul Sesli Sınav Merkezi ve Gelişim Karnesi / Raporlar",
        "subtitle": "4 Şıklı Sesli Anlama (İstimâ) Sınavı, Başarı Rozetleri, Ses Dinleme ve Ödev ZIP Paketi",
        "intro": (
            "Öğrencinin dinleme-anlama becerisini ölçmek ve çalışma motivasyonunu artırmak için uygulamada "
            "bağımsız bir '🎧 Dinle & Bul Sınav Merkezi' ile kapsamlı bir '📊 Gelişim Karnesi ve Öğretmen Raporu' "
            "modülü yer alır. Kullanıcının sonradan eklediği özel paketler de otomatik olarak sınav havuzuna dahil olur."
        ),
        "highlights": [
            ("🎧 Dinle & Bul Sınav Merkezi:", "Kelime, Sözlük, Cümle veya Diyalog havuzlarından 10, 20, 50 soruluk ya da ♾️ Sınırsız 4 şıklı sesli sınav üretir."),
            ("🏅 6 Başarı Rozeti ve Seviye Unvanları:", "İlk Kıvılcım, Kelime Avcısı, Muhâdese Yıldızı, Cümle Üstadı, İstikrar Abidesi ve Arapça Hatibi rozetleri."),
            ("🎧 Öğrencinin Ses Kaydını (.wav) Dinleme:", "Raporlarda en çok hata yapılan kelimeler seçilerek öğrencinin o kelimedeki gerçek ses kaydı dinlenebilir."),
            ("📦 Öğretmen İçin Ödev Paketi (.ZIP):", "Öğrencinin başarı karnesini (HTML + CSV) ve son 20 ses kaydını (.wav) tek bir .ZIP arşivinde paketler.")
        ],
        "screens": [
            {
                "sc_no": 8,
                "title": "Dinle & Bul — Sesli Sınav ve Pratik Merkezi",
                "desc": "Üst bardan Kaynak, Paket, Seviye ve Soru Hedefi seçildikten sonra '▶️ SINAVI BAŞLAT' butonuna basılır. Sistem Arapça ifadeyi seslendirir ve öğrenci A, B, C, D şıklarından doğru Türkçe karşılığı seçer.",
                "tips": [
                    "İstenirse sağ üstteki '👁️ Arapça Yazılışı Göster (İpucu)' kutusu işaretlenerek seslendirilen metnin Arapça yazılışı da ekranda görülebilir."
                ]
            },
            {
                "sc_no": 9,
                "title": "Gelişim Karnesi, Rozetler, Ses Dinleme ve Öğretmen Raporu Merkezi",
                "desc": "Öğrencinin kazandığı başarı rozetlerini, son Dinle & Bul sınav sonucunu, paket ilerleme grafiklerini ve en çok hata yapılan kayıtları gösterir.",
                "tips": [
                    "Alt bardaki '📥 Raporu CSV / Excel Aktar' ve '📦 Ödev & Ses Paketi Oluştur (.ZIP)' butonlarıyla öğrenci performansı öğretmene kolayca iletilebilir."
                ]
            }
        ]
    },
    {
        "num": "9",
        "id": "bolum-9",
        "title": "Öğretmenler İçin A4 Yazılı Sınav, Karma Quiz ve Ders Notu (Handout) Üretici",
        "subtitle": "Ayrık Havuzlu 6 Soru Tipi, Ayrı Sayfada Cevap Anahtarı ve Sınavsız Okuma Metni Çıktısı",
        "intro": (
            "Öğretmenlerin hem hazır paketlerden hem de kendi yükledikleri ünite/ders paketlerinden saniyeler içinde "
            "A4 yazılı sınav, yaprak test veya okuma metni (Handout) üretebilmesini sağlayan 2'si 1 arada materyal "
            "motorudur. Üretilen belge tarayıcıda açılır ve 'Ctrl+P' ile doğrudan PDF veya yazıcı çıktısına dönüştürülür."
        ),
        "highlights": [
            ("🌟 Karma Sınav & Ayrık Havuz:", "Kelime, Diyalog ve Cümlelerden karma sınav üretir; 1. Bölümde sorulan ifade 2. Bölümde tekrar sorulmaz."),
            ("📐 2x2 Hizalı Çoktan Seçmeli Test:", "A, B, C, D şıkları CSS Grid ile simetrik 2x2 kutular halinde dizilir; cevap anahtarı ayrı sayfaya basılır."),
            ("🌿 Sarf Alıştırma Tablosu:", "Kelimelerin Sülâsî Köklerini ve Müfret➔Cemî / Mâzî➔Muzâri dönüşümlerini soran özel tablo üretir."),
            ("📖 Temiz Ders Notu (Handout):", "Sınavsız Yan Yana (İki Sütun %50-%50), Alt Alta, Sonda Toplu veya Sadece Arapça okuma yaprağı üretir.")
        ],
        "screens": [
            {
                "sc_no": 10,
                "title": "A4 Yazılı Sınav, Ders Notu ve Quiz Üretici Ayar Ekranı",
                "desc": "6 farklı soru bölümünün (Arapça➔Türkçe, Türkçe➔Arapça, Boşluk Doldurma, 4 Şıklı Test, Eşleştirme, Sarf Tablosu) soru sayıları 0 ile 50 arasında ayrı ayrı belirlenebilir; Diyalog ve Cümleler için 'Ders Notu / Okuma Metni Formatı' seçilebilir.",
                "tips": [
                    "Sınav kağıdında yer almasını istemediğiniz bölümün soru sayısını '0' yapmanız yeterlidir; o bölüm kağıda hiç eklenmez.",
                    "İki sütunlu ('Yan Yana') ders notu seçildiğinde sol sütunda %50 genişlikte büyük puntolu Arapça metin (RTL), sağ sütunda ise Türkçe tercümesi yer alır."
                ]
            },
            {
                "sc_no": 11,
                "title": "Üretilen A4 Yazılı Sınav Kağıdının Tarayıcı ve Baskı Önizlemesi",
                "desc": "Kurumsal antet, logo, Öğrenci Adı Soyadı / Sınıf / Tarih / Puan kutusu ve geniş yazma satırlarıyla oluşturulan A4 sınav kağıdı. Üstteki yeşil butonla doğrudan yazıcıya gönderilebilir veya PDF olarak kaydedilebilir.",
                "tips": [
                    "Yazdırma sırasında üstteki koyu renkli kontrol çubuğu otomatik olarak gizlenir (@media print) ve kağıda yalnızca temiz sınav içeriği basılır."
                ]
            }
        ]
    },
    {
        "num": "10",
        "id": "bolum-10",
        "title": "Sekmeli Uygulama ve Eğitim Ayarları (6 Sekmeli Kontrol Merkezi)",
        "subtitle": "Çalışma Akışı, Ses & TTS, Diyalog Ölçme, Tema, Depolama Bakımı ve GitHub Güncelleme",
        "intro": (
            "Sağ paneldeki '⚙️ Tüm Ayarlar (Sekmeli)' butonuna tıklandığında açılan pencere, uygulamanın tüm "
            "pedagojik ve teknik parametrelerini 6 düzenli sekme altında yönetme imkânı verir."
        ),
        "highlights": [
            ("🏠 1. Sekme — Genel & Çalışma:", "Otomatik ilerleme, Eller Serbest Mod, Rastgele sıra, Edit modu, Öğretmen barı ve deneme hakkı sayısı."),
            ("🔊 2. Sekme — Ses & TTS:", "Kadın/Erkek/Sırayla ses tercihi, geçişte otomatik seslendirme, %25 yavaş TTS ve tekrar sayısı (1-3)."),
            ("💬 3. Sekme — Diyalog & Ölçme:", "Roleplay modunda cümle başına deneme hakkı (1-5) ve doğru kelimelerin anlık yeşil açılması."),
            ("🎨 4-6. Sekmeler — Tema, Bakım & Güncelleme:", "Aydınlık/Karanlık tema, kayıt temizliği, Metin Doktoru ve GitHub otomatik sürüm güncelleme.")
        ],
        "screens": [
            {
                "sc_no": 12,
                "title": "Ayarlar 1. Sekme: 🏠 Genel & Çalışma Ayarları",
                "desc": "Çalışma akışı, öğrenci adı, deneme hakkı sınırı (1, 2, 3, 5 Kez veya Sınırsız) ve Sınav Modu (Arapçayı Gizle) kontrolleri.",
                "tips": [
                    "'✏️ Düzenleme (Edit) Modunu Aç' kutusu işaretlendiğinde Kelime, Diyalog ve Cümle ekranlarının üst barında hızlı '✏️ Düzenle' butonları belirir."
                ]
            },
            {
                "sc_no": 13,
                "title": "Ayarlar 2. Sekme: 🔊 Ses & TTS Ayarları",
                "desc": "Seslendirme cinsiyeti tercihi, yavaş seslendirme (%25) ve referans sesin peş peşe kaç kez (1-3) çalınacağının belirlendiği sekme.",
                "tips": [
                    "Yeni başlayan (A1) öğrenciler için '🐢 Yavaş Seslendirme' ve Referans Tekrar Sayısının '2' yapılması önerilir."
                ]
            },
            {
                "sc_no": 14,
                "title": "Ayarlar 3. Sekme: 💬 Diyalog & Ölçme Ayarları",
                "desc": "Karşılıklı diyalog canlandırma (Roleplay) sırasında öğrenciye her cümle için tanınacak deneme hakkı ve kademeli kelime açma ayarı.",
                "tips": [
                    "Cümle bitmeden doğru söylenen kelimelerin yeşil renkte açılması öğrencinin motivasyonunu artırır."
                ]
            },
            {
                "sc_no": 15,
                "title": "Ayarlar 4. Sekme: 🎨 Görünüm & Tema Ayarları",
                "desc": "Aydınlık ve Karanlık mod geçişi ile Kelime, Diyalog ve Cümle modlarında hareke ve Türkçe çeviri görünürlük ayarları.",
                "tips": [
                    "Sınıf içi akıllı tahtalarda yüksek kontrastlı '☀️ Aydınlık Mod', bireysel gece çalışmalarında ise '🌙 Karanlık Mod' tercih edilebilir."
                ]
            },
            {
                "sc_no": 16,
                "title": "Ayarlar 5. Sekme: 🛠️ Depolama & Bakım Ayarları",
                "desc": "recordings/ klasöründe biriken öğrenci ses kayıtlarının diskte yer kaplamaması için son 10 kaydı tutup eskileri otomatik silme ayarı ve Veritabanı Metin Doktoru.",
                "tips": [
                    "'🪄 Metin Doktorunu Çalıştır' butonu; dışarıdan yüklenen paketlerdeki parantez içi rakamları ve sayfa numaralarını tek tıkla temizler."
                ]
            },
            {
                "sc_no": 17,
                "title": "Ayarlar 6. Sekme: 🔄 GitHub Otomatik Güncelleme Merkezi",
                "desc": "Uygulamanın kurulu sürümünü ve resmi GitHub deposunu gösterir; manuel güncelleme kontrolü başlatır.",
                "tips": [
                    "Güncelleme yapıldığında öğrencinin ve öğretmenin kendi eklediği veritabanları ile ses kayıtları korunur; hiçbir veri silinmez."
                ]
            }
        ]
    },
    {
        "num": "11",
        "id": "bolum-11",
        "title": "Uygulamanın Kalbi: İçerik Üreticileri İçin %100 Özelleştirilebilir Paket & Yönetim Stüdyosu",
        "subtitle": "Uygulamada Hiç Veri Olmasa Bile Kendi Müfredatınızı Sıfırdan Oluşturma, Excel Yapıştırma ve Medya Eşleştirme",
        "intro": (
            "Uygulamanın en önemli ve ayırt edici özelliği; son kullanıcının veya öğretmenin hazır gelen içeriklere "
            "bağımlı olmamasıdır. Yönetim & Paket Paneli (Admin) sayesinde mevcut tüm paketleri silebilir, değiştirebilir "
            "veya uygulama içinde tek bir kelime dahi olmasa kendi ders kitabınızın kelimelerini, diyaloglarını ve "
            "cümlelerini 5 farklı yöntemle dakikalar içinde sisteme yükleyip '.ZIP' paketi olarak öğrencilerinizle paylaşabilirsiniz."
        ),
        "highlights": [
            ("📥 1) Birleştir vs. Tam Sıfırlama:", "CSV, JSON veya ZIP paketi yüklerken mevcut veritabanıyla birleştirme veya eski verileri tamamen silip sıfırdan sadece kendi müfredatınızı kurma seçeneği sunar."),
            ("📋 2) Excel'den Kopyala-Yapıştır (Ctrl+V):", "Hiçbir dosya formatıyla uğraşmadan Excel veya Word tablosundaki satırları kopyalayıp doğrudan sisteme aktarır; eksik satırları numarasıyla raporlar."),
            ("🖼️ 3) Toplu Medya Eşleştirme:", "Klasördeki görsel (.jpg/.png) ve ses (.mp3/.wav) dosyalarını kelime ID'si veya Türkçe adına göre ('Arı' ➔ 'ari.jpg') otomatik bağlar."),
            ("🎙️ 4) Mikrofondan Kayıt & ⚡ TTS Hazırla:", "Alt formdan doğrudan kendi sesinizi kaydedebilir veya '⚡ TTS Hazırla' ile eklediğiniz yeni metinlerin seslerini çevrimdışı önbelleğe indirebilirsiniz.")
        ],
        "screens": [
            {
                "sc_no": 18,
                "title": "Yönetim & Paket Paneli Ana Ekranı (Sütun Sıralamalı ve Çoklu Seçimli)",
                "desc": "Üstte Kelimeler, Diyaloglar ve Cümleler sekmeleri; ortada paket aksiyon butonları ve sıralanabilir tablo; en altta ise tekil kayıt ekleme, güncelleme, toplu seviye atama ve mikrofon/medya bağlama formu yer alır.",
                "tips": [
                    "Tablodaki herhangi bir sütun başlığına tıklayarak listeyi A➔Z (▲) veya Z➔A (▼) sıralayabilir; Shift/Ctrl ile çoklu seçim yapıp toplu seviye atayabilirsiniz."
                ]
            },
            {
                "sc_no": 19,
                "title": "Uygulama İçi Paket, Sözlük ve Medya Hazırlama Rehberi",
                "desc": "Yönetim Panelinin sağ üst köşesindeki '📘 Paket Rehberi' butonuna basıldığında açılan ve 5 farklı içerik ekleme yöntemini örnek şablonlarla anlatan rehber ekranı.",
                "tips": [
                    "CSV, JSON ve sozluk.json örnek şablonlarını bu pencereden kopyalayabilir veya '📄 Şablon' butonuyla doğrudan bilgisayarınıza indirebilirsiniz."
                ]
            },
            {
                "sc_no": 20,
                "title": "Excel / Panodan (Clipboard) Hızlı Yapıştır ve Aktar Penceresi",
                "desc": "'📋 Excel Yapıştır' butonuna basıldığında açılır. Hedef Paket ID, Paket Başlığı ve Seviye seçildikten sonra Excel'den kopyalanan satırlar metin alanına yapıştırılır ve tek tıkla veritabanına aktarılır.",
                "tips": [
                    "Sistem Tab (Excel), noktalı virgül (;) veya virgül (,) ayırıcılarını otomatik tanır ve eksik satırları numarasıyla raporlar."
                ]
            },
            {
                "sc_no": 21,
                "title": "Paket Kalite Denetleyicisi Raporu Ekranı",
                "desc": "'🔍 Denetim' butonuna basıldığında seçili paketteki tüm kayıtları tarar; harekesiz Arapça metinleri, boş Türkçe çevirileri ve bulunamayan ses dosyalarını listeler.",
                "tips": [
                    "Denetim listesindeki kusurlu bir satıra çift tıkladığınızda Yönetim Panelinde doğrudan o kaydın satırı seçilerek düzenleme formuna yüklenir."
                ]
            }
        ]
    }
]


# ==============================================================================
# İÇERİK ÜRETİCİLERİ İÇİN KOMPAKT 2 SÜTUNLU TEKNİK PAKET ŞABLONLARI BLOĞU
# ==============================================================================
CREATOR_MANUAL_HTML = """
<div class="creator-guide-box">
  <h3>🛠️ Kendi İçeriğinizi Oluşturun: Veri Formatları ve Dosya Şablonları (UTF-8)</h3>
  <p style="font-size:11.5px;margin:2px 0 8px 0;color:#334155;">
    Uygulama içindeki hazır verileri tamamen silseniz bile aşağıdaki şablonlarla kendi kelime, diyalog, cümle ve sözlük paketlerinizi sıfırdan oluşturabilirsiniz:
  </p>
  <div class="tpl-grid">
    <div class="tpl-card">
      <h4>1) 📋 Excel Kopyala-Yapıştır (Kelime &amp; Cümle)</h4>
      <pre><code>كِتَابٌ	Kitap
مُحَاضَرَةٌ	Konferans	B1
w_101	مُسْتَشْفَى	Hastane	A2</code></pre>
    </div>
    <div class="tpl-card">
      <h4>2) 📋 Excel Kopyala-Yapıştır (Diyalog Satırları)</h4>
      <pre><code>Ömer	E	السَّلَامُ عَلَيْكُمْ.	Selamün aleyküm.
Deniz	K	وَعَلَيْكُمُ السَّلَامُ.	Aleyküm selam.</code></pre>
    </div>
    <div class="tpl-card">
      <h4>3) 🏠 Kelime Paketi CSV (kelimeler.csv)</h4>
      <pre><code>id;arapca;turkce;gorsel;ses;seviye
ari;نَحْلَةٌ;Arı;ari.jpg;ari_f.mp3;A1
kitap;كِتَابٌ;Kitap;;;A1</code></pre>
    </div>
    <div class="tpl-card">
      <h4>4) 📜 Anahtar Cümleler CSV (cumleler.csv)</h4>
      <pre><code>id;arapca;turkce;ses;seviye
s_01;يَتَأَلَّفُ الكِتَابُ مِنْ عَشْرَةِ فُصُولٍ.;Kitap on bölümden oluşuyor.;;A2</code></pre>
    </div>
    <div class="tpl-card">
      <h4>5) 💬 Günlük Diyalog JSON (diyaloglar.json)</h4>
      <pre><code>[{"id": "dlg_01", "baslik_tr": "Tanışma", "seviye": "A1",
  "satirlar": [{"sira": 1, "konusmaci": "Ömer", "cinsiyet": "E",
    "arapca": "مَرْحَباً.", "turkce": "Merhaba!"}]}]</code></pre>
    </div>
    <div class="tpl-card">
      <h4>6) 📖 Sarf Sözlüğü JSON &amp; Tam Paket (.ZIP) Yapısı</h4>
      <pre><code>[{"id":"k_1","tur":"isim","kok":"ط ب ب","mufret":"طَبِيبٌ","cemi":"أَطِبَّاءُ","anlam_tr":"doktor"}]
# ZIP Arşivi: paket.json + images/ + sounds/ (id_f.mp3, id_m.mp3)</code></pre>
    </div>
  </div>
</div>
"""


# ==============================================================================
# 1. ÇIKTI: A4 TAM DOLULUKLU KURUMSAL PDF KULLANIM KILAVUZU
# ==============================================================================
toc_items_html = ""
chapters_body_html = ""

for ch in CHAPTERS:
    toc_items_html += f"""
    <li>
      <a href="#{ch['id']}">
        <span class="toc-num">Bölüm {ch['num']}</span>
        <span class="toc-title">{ch['title']}</span>
        <span class="toc-meta">{len(ch['screens'])} Ekran Görüntüsü</span>
      </a>
    </li>"""

    hl_html = ""
    for h_title, h_desc in ch["highlights"]:
        hl_html += f"<div class='hl-item'><b>{h_title}</b> {h_desc}</div>"

    screens_html = ""
    first_card_html = ""
    for idx_s, sc in enumerate(ch["screens"]):
        sno = sc["sc_no"]
        uri = sc_uris.get(sno, "")
        img_tag = f"<img src='{uri}' alt='Screenshot_{sno}' class='sc-img'/>" if uri else f"<div class='missing-img'>Screenshot_{sno}.png</div>"
        tips_li = "".join([f"<li>💡 {t}</li>" for t in sc["tips"]])

        card_html = f"""
        <div class="screen-card">
          <div class="screen-hdr">
            <span class="sc-badge">📸 Ekran #{sno} (Screenshot_{sno}.png)</span>
            <span class="sc-name">{sc['title']}</span>
          </div>
          <div class="sc-img-wrap">{img_tag}</div>
          <p class="sc-desc">{sc['desc']}</p>
          <ul class="sc-tips">{tips_li}</ul>
        </div>"""

        if idx_s == 0:
            first_card_html = card_html
        else:
            screens_html += card_html

    extra_block = CREATOR_MANUAL_HTML if ch["num"] == "11" else ""

    chapters_body_html += f"""
    <section class="chapter-section" id="{ch['id']}">
      <div class="chapter-start-group">
        <div class="ch-banner">
          <div class="ch-num-badge">BÖLÜM {ch['num']}</div>
          <div>
            <h2>{ch['title']}</h2>
            <div class="ch-sub">{ch['subtitle']}</div>
          </div>
        </div>
        <p class="ch-intro">{ch['intro']}</p>
        <div class="hl-box">
          <h4>🌟 Öne Çıkan Özellikler ve Özelleştirilebilir Kabiliyetler</h4>
          <div class="hl-grid">{hl_html}</div>
        </div>
        {first_card_html}
      </div>
      {screens_html}
      {extra_block}
    </section>"""

icon_cover_html = f"<img src='{icon_uri}' class='cover-logo' alt='Uygulama İkonu'/>" if icon_uri else ""
qr_yt_img_html = f"<img src='{qr_yt_uri}' class='qr-img' alt='YouTube QR'/>" if qr_yt_uri else ""
qr_web_img_html = f"<img src='{qr_web_uri}' class='qr-img' alt='Web QR'/>" if qr_web_uri else ""

manual_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Arapça Telaffuz ve Konuşma Asistanı — Kapsamlı Tanıtım ve Kullanım Kılavuzu</title>
<style>
  @page {{ size: A4 portrait; margin: 10mm 12mm; }}
  * {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #0f172a;
    background: #cbd5e1;
    margin: 0;
    padding: 0;
    line-height: 1.42;
  }}
  .no-print-bar {{
    position: sticky; top: 0; z-index: 999;
    background: #0f172a; color: #f8fafc;
    padding: 10px 24px; display: flex; justify-content: space-between; align-items: center;
    border-bottom: 2px solid #ffd369;
  }}
  .btn-print {{
    background: #00e676; color: #0f172a; font-weight: 800; border: none;
    padding: 8px 20px; border-radius: 6px; cursor: pointer; font-size: 13.5px;
  }}
  .doc-wrapper {{
    max-width: 210mm;
    margin: 14px auto;
    background: #ffffff;
    padding: 10mm 12mm;
    box-shadow: 0 10px 35px rgba(0,0,0,0.18);
  }}
  /* 1. SAYFA: TAM A4 KAPAK SAYFASI */
  .cover-page {{
    height: 272mm;
    max-height: 272mm;
    overflow: hidden;
    background: linear-gradient(145deg, #0f172a 0%, #1e293b 58%, #0f172a 100%);
    color: #f8fafc;
    padding: 12mm 14mm 10mm 14mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    page-break-after: always;
    break-after: page;
    border-bottom: 5px solid #ffd369;
    border-radius: 6px;
  }}
  .cover-logo {{
    width: 98px; height: 98px;
    border-radius: 20px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.45);
    border: 3px solid #ffd369;
    margin: 0 auto 6px auto;
  }}
  .cover-ar {{
    font-family: 'Traditional Arabic', 'Amiri', serif;
    font-size: 25px; color: #ffd369; font-weight: bold;
    margin-bottom: 3px; direction: rtl;
  }}
  .cover-title {{
    font-size: 24px; font-weight: 900; color: #ffffff;
    margin: 2px 0; letter-spacing: 0.3px;
  }}
  .cover-sub {{
    font-size: 12.5px; color: #cbd5e1; font-weight: 500;
    max-width: 580px; margin: 4px auto 8px auto; line-height: 1.38;
  }}
  .custom-engine-Highlight {{
    background: rgba(0, 230, 118, 0.12);
    border: 1px solid #00e676;
    border-radius: 8px; padding: 8px 12px; margin: 6px 0;
    font-size: 11.5px; color: #f8fafc; text-align: left; line-height: 1.4;
  }}
  .custom-engine-Highlight b {{ color: #00e676; }}
  .cover-badges {{
    display: flex; flex-wrap: wrap; justify-content: center; gap: 6px;
    margin: 6px 0;
  }}
  .c-badge {{
    background: rgba(255,211,105,0.13);
    border: 1px solid rgba(255,211,105,0.45);
    color: #ffd369; padding: 4px 10px; border-radius: 16px;
    font-size: 10.5px; font-weight: 700;
  }}
  .cover-stats-grid {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
    margin: 6px 0; text-align: center;
  }}
  .c-stat-box {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.16);
    border-radius: 8px; padding: 7px 5px;
  }}
  .c-stat-num {{ font-size: 16px; font-weight: 800; color: #00e676; }}
  .c-stat-lbl {{ font-size: 10px; color: #cbd5e1; margin-top: 2px; }}

  .cover-qr-row {{
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
    margin: 6px 0; text-align: left;
  }}
  .cover-qr-card {{
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(255, 211, 105, 0.45);
    border-radius: 8px; padding: 7px 10px;
    display: flex; align-items: center; gap: 10px;
  }}
  .qr-img {{
    width: 60px; height: 60px; border-radius: 6px;
    background: #ffffff; padding: 2px; flex-shrink: 0;
  }}
  .qr-info h4 {{ margin: 0 0 2px 0; font-size: 11px; color: #ffd369; }}
  .qr-info p {{ margin: 0 0 2px 0; font-size: 9.8px; color: #cbd5e1; line-height: 1.28; }}
  .qr-info a {{ color: #00e676; font-size: 10px; font-weight: 800; text-decoration: underline; word-break: break-all; }}

  .cover-footer {{
    border-top: 1px solid rgba(255,255,255,0.18);
    padding-top: 7px; font-size: 11px; color: #e2e8f0;
    display: flex; justify-content: space-between; align-items: center;
  }}
  .cover-footer a {{ color: #ffd369; text-decoration: none; font-weight: 700; }}

  /* 2. SAYFA: İÇİNDEKİLER */
  .toc-page {{
    padding: 2mm 2mm;
    page-break-after: always;
    break-after: page;
  }}
  .toc-page h2 {{
    font-size: 19px; color: #0f172a; border-bottom: 3px solid #1e3a8a;
    padding-bottom: 5px; margin: 0 0 6px 0;
  }}
  .toc-list {{ list-style: none; padding: 0; margin: 6px 0 12px 0; }}
  .toc-list li {{ border-bottom: 1px dashed #cbd5e1; padding: 5px 4px; }}
  .toc-list a {{
    text-decoration: none; color: #0f172a;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 12.5px; font-weight: 600;
  }}
  .toc-num {{
    background: #1e3a8a; color: #ffd369; font-weight: 800;
    padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-right: 10px;
    min-width: 74px; text-align: center;
  }}
  .toc-title {{ flex: 1; }}
  .toc-meta {{ color: #475569; font-size: 11px; font-weight: 700; }}
  .shortcuts-table {{ width: 100%; border-collapse: collapse; margin-top: 6px; font-size: 11.5px; }}
  .shortcuts-table th, .shortcuts-table td {{ border: 1px solid #cbd5e1; padding: 5px 9px; text-align: left; }}
  .shortcuts-table th {{ background: #0f172a; color: #ffd369; }}

  .toc-video-banner {{
    margin-top: 12px;
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    color: #ffffff; border-radius: 8px; padding: 10px 14px;
    border-left: 5px solid #ef4444;
    display: flex; align-items: center; justify-content: space-between; gap: 14px;
  }}
  .toc-video-banner a {{ color: #ffd369; font-weight: 800; text-decoration: underline; }}

  /* BÖLÜMLER VE EKRAN KARTLARI */
  .chapter-section {{ margin-bottom: 12px; }}
  .chapter-start-group {{ page-break-inside: avoid; break-inside: avoid; }}
  .ch-banner {{
    background: linear-gradient(90deg, #0f172a, #1e3a8a);
    color: #ffffff; padding: 8px 14px; border-radius: 6px;
    display: flex; align-items: center; gap: 12px;
    border-left: 5px solid #ffd369;
    margin-bottom: 6px; margin-top: 8px;
  }}
  .ch-num-badge {{
    background: #ffd369; color: #0f172a; font-weight: 900;
    padding: 4px 10px; border-radius: 5px; font-size: 12px; white-space: nowrap;
  }}
  .ch-banner h2 {{ margin: 0; font-size: 15.5px; color: #ffffff; line-height: 1.25; }}
  .ch-sub {{ font-size: 11px; color: #cbd5e1; margin-top: 2px; }}
  .ch-intro {{ font-size: 11.8px; color: #1e293b; text-align: justify; margin: 5px 0 7px 0; }}
  .hl-box {{
    background: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #0d9488;
    border-radius: 6px; padding: 7px 12px; margin-bottom: 9px;
  }}
  .hl-box h4 {{ margin: 0 0 5px 0; color: #0f766e; font-size: 12px; }}
  .hl-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; font-size: 11px; }}
  .hl-item {{ line-height: 1.35; color: #1e293b; }}

  .screen-card {{
    border: 1px solid #cbd5e1; border-radius: 6px;
    background: #ffffff; padding: 8px 11px; margin-bottom: 9px;
    page-break-inside: avoid; break-inside: avoid;
  }}
  .screen-hdr {{
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid #e2e8f0; padding-bottom: 4px; margin-bottom: 6px;
  }}
  .sc-badge {{
    background: #0f172a; color: #ffd369; font-size: 10.5px; font-weight: 800;
    padding: 2px 8px; border-radius: 4px; white-space: nowrap;
  }}
  .sc-name {{ font-size: 13px; font-weight: 800; color: #1e3a8a; }}
  .sc-img-wrap {{
    text-align: center; background: #0f172a; padding: 5px; border-radius: 5px; margin-bottom: 6px;
  }}
  .sc-img {{
    max-width: 100%; max-height: 60mm; width: auto; height: auto;
    border-radius: 3px; border: 1px solid #334155; display: inline-block;
  }}
  .sc-desc {{ font-size: 11.4px; color: #1e293b; margin: 4px 0; text-align: justify; line-height: 1.38; }}
  .sc-tips {{
    list-style: none; padding: 5px 9px; margin: 4px 0 0 0;
    background: #fffbeb; border: 1px solid #fde68a; border-radius: 4px;
    font-size: 11px; color: #92400e; font-weight: 600; line-height: 1.35;
  }}
  .sc-tips li {{ margin-bottom: 2px; }}

  .creator-guide-box {{
    background: #f8fafc; border: 2px solid #1e3a8a; border-radius: 6px;
    padding: 10px 12px; margin-top: 8px;
    page-break-inside: avoid; break-inside: avoid;
  }}
  .creator-guide-box h3 {{ margin: 0 0 4px 0; color: #1e3a8a; font-size: 14px; }}
  .tpl-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
  .tpl-card {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px 8px; }}
  .tpl-card h4 {{ margin: 0 0 4px 0; color: #0f172a; font-size: 11.5px; }}
  pre {{
    background: #0f172a; color: #f8fafc; padding: 6px 8px;
    border-radius: 4px; font-family: 'Consolas', monospace; font-size: 10px;
    overflow-x: auto; margin: 0; line-height: 1.35;
  }}

  @media print {{
    body {{ background: #ffffff; }}
    .no-print-bar {{ display: none !important; }}
    .doc-wrapper {{ box-shadow: none; margin: 0; padding: 0; max-width: 100%; }}
  }}
</style>
</head>
<body>
  <div class="no-print-bar">
    <div>📘 <b>Arapça Telaffuz ve Konuşma Asistanı</b> — %100 Özelleştirilebilir İçerik Motoru &amp; Kullanım Kılavuzu</div>
    <button class="btn-print" onclick="window.print()">🖨️ PDF Olarak Kaydet / Yazdır (Ctrl+P)</button>
  </div>

  <div class="doc-wrapper">
    <!-- 1. SAYFA: KAPAK SAYFASI -->
    <div class="cover-page">
      <div>
        <div style="font-size:11px;font-weight:800;color:#ffd369;letter-spacing:1.4px;text-transform:uppercase;margin-bottom:6px;">
          MUALLİMUN.NET EĞİTİM TEKNOLOJİLERİ — KILAVUZ VE TEKNİK DOKÜMAN
        </div>
        {icon_cover_html}
        <div class="cover-ar">مُخْتَبَرُ النُّطْقِ وَالصَّرْفِ وَالْمُحَادَثَةِ بِالذَّكَاءِ الِاصْطِنَاعِيِّ</div>
        <h1 class="cover-title">ARAPÇA TELAFFUZ VE KONUŞMA ASİSTANI</h1>
        <div class="cover-sub">
          Yapay Zekâ Destekli Telaffuz (Mahreç), Sülâsî Kök &amp; Sarf Sözlüğü, Günlük Diyalog Canlandırma (Roleplay),
          Gölgeleme (Shadowing) ve Öğretmen Sınav/Materyal Üretim Platformu — Sürüm
        </div>

        <div class="custom-engine-Highlight">
          🛠️ <b>%100 ÖZELLEŞTİRİLEBİLİR AÇIK İÇERİK MOTORU:</b> Uygulama kurulduğunda zengin bir başlangıç veri setiyle
          (kelime, sözlük, diyalog ve cümle paketleri) hazır gelir. Ancak uygulamanın asıl gücü; <b>içinde hiçbir veri olmasa bile</b>
          kullanıcının veya öğretmenin hiçbir kodlama bilmeden <b>Excel'den kopyala-yapıştır (Ctrl+V), CSV/JSON/ZIP veya doğrudan
          mikrofon kaydıyla kendi müfredatını, ders kitabını, görsellerini ve seslerini kolayca ekleyebilmesidir!</b>
        </div>

        <div class="cover-badges">
          <span class="c-badge">🛠️ %100 Özelleştirilebilir Müfredat</span>
          <span class="c-badge">🎙️ Çevrimdışı Faster-Whisper AI</span>
          <span class="c-badge">📖 Sarf Sözlüğü &amp; Kök Atölyesi</span>
          <span class="c-badge">💬 Diyalog Canlandırma (Roleplay)</span>
          <span class="c-badge">🎯 Canlı Mahreç &amp; Hareke Koçu</span>
          <span class="c-badge">🖨️ A4 Yazılı Sınav &amp; Ders Notu Üretici</span>
        </div>
      </div>

      <div class="cover-stats-grid">
        <div class="c-stat-box">
          <div class="c-stat-num">Sınırsız</div>
          <div class="c-stat-lbl">Kendi Paket &amp; Müfredatını Ekle</div>
        </div>
        <div class="c-stat-box">
          <div class="c-stat-num">Excel / ZIP</div>
          <div class="c-stat-lbl">Tek Tıkla Kopyala-Yapıştır Aktarım</div>
        </div>
        <div class="c-stat-box">
          <div class="c-stat-num">%100 Offline</div>
          <div class="c-stat-lbl">Faster-Whisper Ses Analiz Motoru</div>
        </div>
        <div class="c-stat-box">
          <div class="c-stat-num">Hazır Set</div>
          <div class="c-stat-lbl">Sözlük, Diyalog ve Cümlelerle Gelir</div>
        </div>
      </div>

      <!-- KAPAK SAYFASI QR KODLU YOUTUBE VİDEO VE WEB ERİŞİM KARTLARI (SETUP İÇİN QR KOD YOKTUR) -->
      <div class="cover-qr-row">
        <div class="cover-qr-card">
          {qr_yt_img_html}
          <div class="qr-info">
            <h4>🎬 Videolu Tanıtım &amp; Rehber (YouTube)</h4>
            <p>QR kodu okutarak veya bağlantıya tıklayarak 7:50 dk'lık kapsamlı sesli ve görüntülü tanıtımı izleyin:</p>
            <a href="{YOUTUBE_SHORT_URL}" target="_blank">{YOUTUBE_SHORT_URL}</a>
          </div>
        </div>
        <div class="cover-qr-card">
          {qr_web_img_html}
          <div class="qr-info">
            <h4>🌐 Web Tanıtım &amp; Kılavuz Sayfası</h4>
            <p>Çevrimiçi kılavuzu inceleyin ve Windows bilgisayarınızdan kurulum paketini indirin:</p>
            <a href="{WEB_GUIDE_URL}" target="_blank">{WEB_GUIDE_URL}</a>
          </div>
        </div>
      </div>

      <div class="cover-footer">
        <div>🌐 <b>Web Kılavuz:</b> <a href="{WEB_GUIDE_URL}">arapca.muallimun.net</a></div>
        <div>🎬 <b>YouTube:</b> <a href="{YOUTUBE_SHORT_URL}">{YOUTUBE_SHORT_URL}</a></div>
        <div>💻 <b>Platform:</b> Windows 10/11 &amp; Akıllı Tahta</div>
      </div>
    </div>

    <!-- 2. SAYFA: İÇİNDEKİLER, KISAYOLLAR VE VİDEO BANNER -->
    <div class="toc-page">
      <h2>📑 İçindekiler ve Bölüm Rehberi</h2>
      <p style="font-size:12px;color:#475569;margin:3px 0 6px 0;">
        Bu kılavuz; uygulamanın kurulumundan sınıf içi kullanımına, öğrenci telaffuz antrenmanlarından
        kullanıcıların kendi özel kelime/diyalog/cümle paketlerini ve yazılı sınavlarını üretmesine kadar tüm süreçleri adım adım açıklar.
      </p>
      <ul class="toc-list">
        {toc_items_html}
      </ul>

      <h3 style="margin:10px 0 5px 0;color:#1e3a8a;font-size:15px;">⌨️ Hızlı Klavye Kısayolları ve Temel Kontroller</h3>
      <table class="shortcuts-table">
        <thead>
          <tr>
            <th style="width:200px;">Klavye Tuşu / Buton</th>
            <th>İşlevi ve Çalıştığı Ekranlar</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><b>[Boşluk / Space]</b></td><td>Kelime, Cümle ve Diyalog Canlandırma (Roleplay) modlarında ses kaydını başlatır veya durdurur.</td></tr>
          <tr><td><b>[Sağ Ok ▶] / [Sol Ok ◀]</b></td><td>Kelime ve Anahtar Cümle modlarında sonraki veya önceki karta hızlı geçiş yapar.</td></tr>
          <tr><td><b>[F1] veya [ℹ️ İkonu]</b></td><td>Uygulama içi Kullanım Kılavuzunu, YouTube videosunu ve PDF/Web bağlantı merkezini açar.</td></tr>
          <tr><td><b>[Enter] (Cümle No Kutusunda)</b></td><td>Cümle modunda numara kutusuna yazılan cümleye doğrudan atlar.</td></tr>
          <tr><td><b>[Shift / Ctrl + Sol Tık]</b></td><td>Yönetim Panelinde birden fazla kaydı seçerek toplu seviye (A1-C1) ataması veya silme yapar.</td></tr>
        </tbody>
      </table>

      <div class="toc-video-banner">
        {qr_yt_img_html}
        <div style="flex:1;font-size:12px;line-height:1.45;">
          <div style="font-size:13.5px;font-weight:800;color:#ffd369;margin-bottom:2px;">
            ▶️ SESLİ VE GÖRÜNTÜLÜ UYGULAMA REHBERİ (YOUTUBE — 07:50 DK)
          </div>
          Uygulamanın tüm modüllerini, mahreç koçunu ve kendi içeriğinizi nasıl ekleyebileceğinizi sesli anlatımla izlemek için:<br>
          🎬 <b>YouTube Video Linki:</b> <a href="{YOUTUBE_SHORT_URL}" target="_blank">{YOUTUBE_SHORT_URL}</a> &nbsp;|&nbsp;
          🌐 <b>Web Sayfası:</b> <a href="{WEB_GUIDE_URL}" target="_blank">{WEB_GUIDE_URL}</a>
        </div>
      </div>
    </div>

    <!-- 11 BÖLÜM VE 27 ÖZGÜN EKRAN GÖRÜNTÜSÜ -->
    {chapters_body_html}
  </div>
</body>
</html>
"""

manual_html_path = os.path.join(OUT_DIR, "Arapca_Telaffuz_Asistani_Kullanim_Kilavuzu.html")
with open(manual_html_path, "w", encoding="utf-8") as f:
    f.write(manual_html)
print(f"✅ Basılabilir HTML Kılavuz güncellendi: {manual_html_path}")


# ==============================================================================
# 2. ÇIKTI: MOBİL UYUMLU (RESPONSIVE) VE WINDOWS UYARILI WEB TANITIM SAYFASI
# ==============================================================================
gallery_cards_html = ""
for ch in CHAPTERS:
    for sc in ch["screens"]:
        sno = sc["sc_no"]
        img_rel = f"images/Screenshot_{sno}.png"
        gallery_cards_html += f"""
        <div class="g-card" data-cat="ch-{ch['num']}">
          <div class="g-img-box">
            <img src="{img_rel}" alt="{sc['title']}" loading="lazy" onclick="openLightbox(this.src, '{sc['title']}')"/>
          </div>
          <div class="g-body">
            <span class="g-tag">Bölüm {ch['num']} • Ekran #{sno}</span>
            <h4>{sc['title']}</h4>
            <p>{sc['desc']}</p>
          </div>
        </div>"""

web_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Arapça Telaffuz ve Konuşma Asistanı — Muallimun.Net</title>
<style>
  :root {{
    --bg: #0f172a;
    --card: #1e293b;
    --panel: #162032;
    --gold: #ffd369;
    --green: #00e676;
    --blue: #3b82f6;
    --red: #ef4444;
    --text: #f8fafc;
    --muted: #94a3b8;
    --border: #2b3b55;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--bg); color: var(--text); line-height: 1.6;
    overflow-x: hidden;
  }}
  a {{ color: var(--gold); text-decoration: none; }}
  .container {{ max-width: 1240px; margin: 0 auto; padding: 0 20px; }}

  /* ÜST GEZİNTİ BARI (MOBİLDE TAŞMA YAPMAYAN ESNEK YAPI) */
  header {{
    background: rgba(15, 23, 42, 0.96); backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 100;
    padding: 10px 0;
  }}
  .nav-row {{
    display: flex; justify-content: space-between; align-items: center;
    min-height: 52px; flex-wrap: wrap; gap: 12px;
  }}
  .brand {{
    display: flex; align-items: center; gap: 10px;
    font-weight: 800; font-size: 17.5px; color: var(--gold);
  }}
  .brand img {{ width: 40px; height: 40px; border-radius: 10px; border: 1px solid var(--gold); flex-shrink: 0; }}
  .nav-links {{
    display: flex; gap: 14px; align-items: center;
    font-size: 14px; font-weight: 600; flex-wrap: wrap;
  }}
  .nav-links a {{ padding: 4px 6px; border-radius: 6px; }}
  .btn-dl-top {{
    background: var(--green); color: #0f172a !important; padding: 8px 16px !important;
    border-radius: 8px !important; font-weight: 800; transition: 0.2s;
    display: inline-flex; align-items: center; gap: 6px;
  }}
  .btn-dl-top:hover {{ transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,230,118,0.35); }}

  /* HERO ALANI */
  .hero {{
    padding: 44px 0 42px 0; text-align: center;
    background: radial-gradient(circle at 50% 10%, #1e3a8a 0%, #0f172a 68%);
    border-bottom: 1px solid var(--border);
  }}
  .hero-logo {{
    width: 104px; height: 104px; border-radius: 22px;
    border: 3px solid var(--gold); box-shadow: 0 12px 30px rgba(0,0,0,0.5);
    margin-bottom: 12px;
  }}
  .hero-ar {{
    font-family: 'Traditional Arabic', serif; font-size: 28px; color: var(--gold);
    margin-bottom: 6px; direction: rtl; padding: 0 10px;
  }}
  .hero h1 {{ font-size: 34px; margin: 0 0 12px 0; font-weight: 900; line-height: 1.25; }}
  .hero p {{
    max-width: 820px; margin: 0 auto 20px auto; font-size: 16.5px; color: #cbd5e1;
  }}

  /* ÖZELLEŞTİRİLEBİLİR AÇIK İÇERİK MOTORU VURGU KUTUSU */
  .customizable-banner {{
    max-width: 900px; margin: 0 auto 24px auto;
    background: rgba(0, 230, 118, 0.10); border: 1px solid rgba(0, 230, 118, 0.55);
    border-radius: 12px; padding: 14px 20px; text-align: left;
    font-size: 14.5px; color: #f8fafc; line-height: 1.55;
  }}
  .customizable-banner b {{ color: var(--green); }}

  /* WINDOWS BİLGİSAYAR UYARI BANDI (ÖZELLİKLE MOBİL KULLANICILAR İÇİN) */
  .os-notice-box {{
    max-width: 760px; margin: 0 auto 22px auto;
    background: rgba(255, 211, 105, 0.12); border: 1px solid rgba(255, 211, 105, 0.45);
    border-radius: 10px; padding: 10px 16px; font-size: 13.5px; color: var(--gold);
    font-weight: 600;
  }}
  .mobile-only-warning {{
    display: none;
    max-width: 680px; margin: 0 auto 18px auto;
    background: rgba(239, 68, 68, 0.16); border: 1px solid #ef4444;
    color: #fecaca; border-radius: 10px; padding: 12px 16px;
    font-size: 13.5px; font-weight: 700; text-align: left;
  }}

  .cta-row {{ display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; margin-bottom: 32px; }}
  .btn-main-dl {{
    background: var(--green); color: #0f172a; padding: 14px 26px;
    border-radius: 10px; font-size: 16px; font-weight: 900;
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    box-shadow: 0 10px 25px rgba(0,230,118,0.3);
  }}
  .btn-yt-dl {{
    background: var(--red); color: #ffffff; padding: 14px 22px;
    border-radius: 10px; font-size: 15.5px; font-weight: 800;
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    box-shadow: 0 10px 25px rgba(239,68,68,0.3);
  }}
  .btn-sec-dl {{
    background: var(--card); color: var(--text); border: 1px solid var(--border);
    padding: 14px 20px; border-radius: 10px; font-size: 15px; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  }}

  /* YOUTUBE 16:9 VİDEO OYNATICI */
  .video-showcase {{
    max-width: 960px; margin: 0 auto 20px auto;
    background: var(--card); border: 2px solid var(--gold);
    border-radius: 14px; overflow: hidden;
    box-shadow: 0 22px 55px rgba(0,0,0,0.65);
  }}
  .video-hdr {{
    background: #090e1a; padding: 12px 18px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    border-bottom: 1px solid var(--border);
  }}
  .video-hdr span {{ font-weight: 800; color: var(--gold); font-size: 14.5px; }}
  .video-responsive {{
    position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; background: #000;
  }}
  .video-responsive iframe {{
    position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;
  }}
  .video-footer-bar {{
    padding: 12px 18px; background: var(--panel);
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;
    text-align: left; font-size: 13.5px;
  }}

  .stats-bar {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px; margin: 36px 0;
  }}
  .stat-card {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px; text-align: center;
  }}
  .stat-num {{ font-size: 24px; font-weight: 900; color: var(--gold); }}
  .stat-lbl {{ font-size: 13.5px; color: var(--muted); margin-top: 4px; }}
  .section-title {{ text-align: center; margin: 48px 0 28px 0; }}
  .section-title h2 {{ font-size: 28px; color: var(--gold); margin: 0 0 8px 0; }}
  .section-title p {{ color: var(--muted); max-width: 720px; margin: 0 auto; }}
  .features-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 18px;
  }}
  .f-card {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; padding: 22px;
  }}
  .f-card h3 {{ margin: 0 0 8px 0; color: var(--gold); font-size: 18px; }}
  .f-card p {{ margin: 0; color: #cbd5e1; font-size: 14px; }}
  .gallery-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px; margin-bottom: 56px;
  }}
  .g-card {{
    background: var(--card); border: 1px solid var(--border);
    border-radius: 12px; overflow: hidden; display: flex; flex-direction: column;
  }}
  .g-img-box {{
    background: #090e1a; padding: 8px; border-bottom: 1px solid var(--border);
    cursor: zoom-in;
  }}
  .g-img-box img {{ width: 100%; height: 200px; object-fit: contain; display: block; }}
  .g-body {{ padding: 15px; flex: 1; }}
  .g-tag {{
    background: rgba(59,130,246,0.2); color: #93c5fd;
    font-size: 11.5px; font-weight: 800; padding: 3px 9px; border-radius: 4px;
  }}
  .g-body h4 {{ margin: 10px 0 6px 0; font-size: 15.5px; color: var(--gold); }}
  .g-body p {{ margin: 0; font-size: 13.2px; color: #cbd5e1; }}

  #lightbox {{
    display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.90);
    z-index: 9999; justify-content: center; align-items: center; flex-direction: column; padding: 16px;
  }}
  #lightbox img {{ max-width: 96%; max-height: 82vh; border-radius: 8px; border: 2px solid var(--gold); }}
  #lightbox-caption {{ color: var(--gold); font-size: 15px; font-weight: 700; margin-top: 10px; text-align: center; }}

  footer {{
    background: #090e1a; border-top: 1px solid var(--border);
    padding: 32px 0; text-align: center; color: var(--muted); font-size: 13.5px;
  }}

  /* 📱 MOBİL EKRAN UYUMLULUK KURALLARI (ÜST ÜSTE BİNMEYİ KESİN OLARAK ÖNLER) */
  @media (max-width: 768px) {{
    header {{ position: relative; padding: 12px 0; }}
    .nav-row {{ flex-direction: column; align-items: stretch; text-align: center; gap: 10px; }}
    .brand {{ justify-content: center; font-size: 16px; }}
    .nav-links {{
      justify-content: center; gap: 8px; font-size: 13px;
      background: var(--panel); padding: 8px; border-radius: 8px;
    }}
    .btn-dl-top {{ display: none !important; }} /* Mobilde üst menüde .exe indirme butonunu gizle */
    .hero {{ padding: 28px 0 32px 0; }}
    .hero-logo {{ width: 84px; height: 84px; }}
    .hero-ar {{ font-size: 21px; }}
    .hero h1 {{ font-size: 24px; }}
    .hero p {{ font-size: 14.5px; }}
    .customizable-banner {{ font-size: 13.2px; padding: 12px 14px; }}
    .mobile-only-warning {{ display: block; }}
    .cta-row {{ flex-direction: column; align-items: stretch; }}
    .btn-main-dl, .btn-yt-dl, .btn-sec-dl {{ width: 100%; font-size: 14.5px; padding: 12px 16px; }}
    .btn-main-dl {{
      background: #334155; color: #cbd5e1; box-shadow: none;
      border: 1px dashed #94a3b8; font-size: 13.5px;
    }}
    .features-grid, .gallery-grid {{ grid-template-columns: 1fr; }}
    .section-title h2 {{ font-size: 22px; }}
  }}
</style>
</head>
<body>
  <header>
    <div class="container nav-row">
      <div class="brand">
        <img src="images/app_icon.png" alt="Logo"/>
        <span>Arapça Telaffuz ve Konuşma Asistanı</span>
      </div>
      <nav class="nav-links">
        <a href="#tanitim-videosu">🎬 Tanıtım Videosu</a>
        <a href="#ozellestirilebilir">🛠️ Kendi İçeriğini Ekle</a>
        <a href="#ozellikler">🌟 Özellikler</a>
        <a href="#ekranlar">📸 Ekranlar</a>
        <a href="Arapca_Telaffuz_Asistani_Kullanim_Kilavuzu.pdf" target="_blank">📕 PDF Kılavuz</a>
        <a href="{SETUP_DOWNLOAD_URL}" class="btn-dl-top">💻 Windows İçin İndir (.exe)</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <img src="images/app_icon.png" alt="App Icon" class="hero-logo"/>
      <div class="hero-ar">مُخْتَبَرُ النُّطْقِ وَالصَّرْفِ وَالْمُحَادَثَةِ بِالذَّكَاءِ الِاصْطِنَاعِيِّ</div>
      <h1>Arapça Telaffuz ve Konuşma Asistanı</h1>
      <p>
        Arapçayı sadece gözle okuyarak değil, mikrofona sesli konuşarak öğrenin! Yapay zekâ destekli mahreç analizi,
        sülâsî kök sözlüğü, karşılıklı diyalog canlandırma ve öğretmenler için A4 yazılı sınav/ders notu üretim platformu.
      </p>

      <div class="customizable-banner" id="ozellestirilebilir">
        🛠️ <b>%100 ÖZELLEŞTİRİLEBİLİR AÇIK İÇERİK MOTORU:</b> Uygulama kurulduğunda zengin bir başlangıç veri setiyle
        (örnek kelime paketleri, sarf sözlüğü, günlük diyaloglar ve anahtar cümleler) hazır olarak gelir. Ancak programın
        asıl gücü; <b>içinde hiçbir veri olmasa bile kullanıcının veya öğretmenin hiçbir kodlama bilmeden kendi ders kitabını,
        kendi kelimelerini, diyaloglarını, cümlelerini, görsellerini ve seslerini (Excel'den kopyala-yapıştır, CSV/JSON/ZIP
        veya mikrofon kaydıyla) dakikalar içinde ekleyip tamamen özelleştirebilmesidir!</b>
      </div>

      <div class="os-notice-box">
        💻 <b>Sistem Bilgisi:</b> Bu yazılım <b>Windows 10 / 11 (64-bit)</b> masaüstü/dizüstü bilgisayarlar ve
        etkileşimli akıllı tahtalar için geliştirilmiştir (<code>.exe</code>).
      </div>

      <div class="mobile-only-warning">
        📱 <b>Mobil Cihaz Bilgilendirmesi:</b> Şu anda bu sayfayı telefon veya tabletten görüntülüyorsunuz.
        Kurulum dosyası (<code>Setup.exe</code>) yalnızca <b>Windows bilgisayarlarda</b> çalışır. Mobil cihazınızdan
        aşağıdaki <b>YouTube Tanıtım Videosunu</b> izleyebilir ve <b>PDF Kullanım Kılavuzunu</b> inceleyebilirsiniz;
        kurulumu ise bilgisayarınızdan indiriniz.
      </div>

      <div class="cta-row">
        <a href="{YOUTUBE_SHORT_URL}" target="_blank" class="btn-yt-dl">
          ▶️ YouTube Tanıtım Videosunu İzle (07:50 dk)
        </a>
        <a href="Arapca_Telaffuz_Asistani_Kullanim_Kilavuzu.pdf" target="_blank" class="btn-sec-dl">
          📘 Resimli PDF Kullanım Kılavuzu
        </a>
        <a href="{SETUP_DOWNLOAD_URL}" class="btn-main-dl">
          💻 Windows Bilgisayar İçin İndir (Setup.exe)
        </a>
        <a href="{GITHUB_REPO_URL}" target="_blank" class="btn-sec-dl">
          🌐 GitHub Deposu
        </a>
      </div>

      <!-- YOUTUBE 16:9 TANITIM VİDEOSU (SETUP İÇİN QR KOD YOKTUR) -->
      <div class="video-showcase" id="tanitim-videosu">
        <div class="video-hdr">
          <span>🎬 Sesli ve Görüntülü Tanıtım &amp; Kullanım Kılavuzu (07:50 dk)</span>
          <a href="{YOUTUBE_SHORT_URL}" target="_blank" style="font-size:13.5px;font-weight:700;">🔗 {YOUTUBE_SHORT_URL} ↗</a>
        </div>
        <div class="video-responsive">
          <iframe
            src="{YOUTUBE_EMBED_URL}"
            title="Arapça Telaffuz ve Konuşma Asistanı Tanıtım ve Kullanım Kılavuzu"
            referrerpolicy="strict-origin-when-cross-origin"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen>
          </iframe>
        </div>
        <div class="video-footer-bar">
          <div>
            📺 Videoyu tam ekran izlemek veya paylaşmak için:
            <a href="{YOUTUBE_SHORT_URL}" target="_blank" style="text-decoration:underline;font-weight:800;">{YOUTUBE_SHORT_URL}</a>
          </div>
          <a href="{YOUTUBE_SHORT_URL}" target="_blank" class="btn-yt-dl" style="padding:8px 16px;font-size:13.5px;">
            ▶️ YouTube'da Aç
          </a>
        </div>
      </div>
    </div>
  </section>

  <div class="container">
    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-num">%100 Özelleştirilebilir</div>
        <div class="stat-lbl">Kendi Kelime, Diyalog ve Cümlelerini Ekle</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">Excel'den Yapıştır</div>
        <div class="stat-lbl">Kod Yazmadan Saniyeler İçinde Paket Üret</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">%100 Çevrimdışı AI</div>
        <div class="stat-lbl">Faster-Whisper Yerel Ses ve Mahreç Analizi</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">Zengin Başlangıç Seti</div>
        <div class="stat-lbl">Hazır Sözlük, Diyalog ve Cümlelerle Gelir</div>
      </div>
    </div>

    <div class="section-title" id="ozellikler">
      <h2>🌟 Öne Çıkan Eğitim ve İçerik Üretim Özellikleri</h2>
      <p>Hem hazır veri setleriyle hemen çalışmaya başlayın hem de kendi müfredatınızı oluşturun.</p>
    </div>

    <div class="features-grid">
      <div class="f-card">
        <h3>🛠️ Kendi Müfredatınızı Oluşturun (Açık Motor)</h3>
        <p>Uygulama içindeki tüm verileri sıfırlasanız bile Excel'den kopyala-yapıştır (Ctrl+V), CSV/JSON/ZIP veya mikrofondan ses kaydıyla kendi ders içeriğinizi kolayca oluşturup paylaşabilirsiniz.</p>
      </div>
      <div class="f-card">
        <h3>🏠 Görselli Kelime Modu &amp; SM-2 Tekrar</h3>
        <p>Kadın ve erkek referans sesleriyle kelimeleri dinleyin, mikrofona okuyun ve Günün 15 Tekrarı (SM-2 algoritması) ile kelimeleri kalıcı hafızaya aktarın.</p>
      </div>
      <div class="f-card">
        <h3>📖 Sarf Sözlüğü &amp; Sülâsî Kök Atölyesi</h3>
        <p>Altıgen kök rozetiyle kelimelerin 3 asli harfini, Müfret/Cemî ve Mâzî/Muzâri/Masdar çekimlerini ve aynı kökten türeyen akraba kelimeleri keşfedin.</p>
      </div>
      <div class="f-card">
        <h3>💬 Günlük Diyaloglar &amp; Roleplay</h3>
        <p>Diyalogları satır satır dinleyin veya bir rol seçip bilgisayarla karşılıklı Arapça konuşma canlandırması yaparak konuşma karnenizi alın.</p>
      </div>
      <div class="f-card">
        <h3>🎯 Canlı Mahreç &amp; Kök Harf Koçu</h3>
        <p>Birbirine karıştırılan 35+ harf çiftini (ص-س, ذ-ز, ع-ء, ط-ت, ق-ك vb.), kök harf değişimlerini ve med uzatmalarını anında tespit eden pedagojik koç.</p>
      </div>
      <div class="f-card">
        <h3>🖨️ A4 Yazılı Sınav &amp; Ders Notu Üretici</h3>
        <p>Hem hazır paketlerden hem de kendi eklediğiniz paketlerden tek tıkla cevap anahtarlı A4 yazılı sınav kağıdı veya iki sütunlu temiz ders notu (PDF/HTML) üretin.</p>
      </div>
    </div>

    <div class="section-title" id="ekranlar">
      <h2>📸 Uygulama Ekran Görüntüleri ve Modül Rehberi</h2>
      <p>Görselleri tam ekran incelemek için üzerlerine tıklayabilirsiniz.</p>
    </div>

    <div class="gallery-grid">
      {gallery_cards_html}
    </div>
  </div>

  <div id="lightbox" onclick="this.style.display='none'">
    <img id="lightbox-img" src="" alt=""/>
    <div id="lightbox-caption"></div>
  </div>

  <footer>
    <div class="container">
      <p><b>Arapça Telaffuz ve Konuşma Asistanı</b> — <a href="{WEBSITE_URL}">Muallimun.Net</a></p>
      <p>
        🎬 <a href="{YOUTUBE_SHORT_URL}" target="_blank">YouTube Tanıtım Videosu</a> •
        📕 <a href="Arapca_Telaffuz_Asistani_Kullanim_Kilavuzu.pdf" target="_blank">PDF Kılavuz</a> •
        📦 <a href="{GITHUB_REPO_URL}" target="_blank">GitHub</a> •
        💻 <a href="{SETUP_DOWNLOAD_URL}">Windows Kurulum Paketi (.exe)</a>
      </p>
    </div>
  </footer>

  <script>
    function openLightbox(src, title) {{
      document.getElementById('lightbox-img').src = src;
      document.getElementById('lightbox-caption').innerText = title;
      document.getElementById('lightbox').style.display = 'flex';
    }}
  </script>
</body>
</html>
"""

web_html_path = os.path.join(OUT_DIR, "tanitim_web_sayfasi.html")
with open(web_html_path, "w", encoding="utf-8") as f:
    f.write(web_html)
print(f"✅ Mobil Uyumlu Web Tanıtım Sayfası güncellendi: {web_html_path}")
# ==============================================================================
# 2.5 ÇIKTI: NOTEBOOKLM İÇİN GÜNCELLENMİŞ TAM KAYNAK METNİ (NotebookLM_Kaynak_Metni.md)
# ==============================================================================
md_lines = [
    "# ARAPÇA TELAFFUZ VE KONUŞMA ASİSTANI — KAPSAMLI TEKNİK VE PEDAGOJİK KILAVUZ\n",
    f"- **Geliştirici & Eğitim Portalı:** Muallimun.Net ({WEBSITE_URL})",
    f"- **Uygulama Tanıtım ve Kılavuz Web Sayfası:** {WEB_GUIDE_URL}",
    f"- **Resmî GitHub Deposu:** {GITHUB_REPO_URL}",
    f"- **Çalıştığı Platform:** Windows 10 / 11 (64-bit) Bilgisayarlar ve Etkileşimli Akıllı Tahtalar (.exe)\n",
    "---\n",
    "## 🔥 UYGULAMANIN TEMEL FELSEFESİ VE EN ÖNEMLİ ÖZELLİĞİ: %100 ÖZELLEŞTİRİLEBİLİR AÇIK İÇERİK MOTORU\n",
    "**Çok Önemli Mimari Not:** Ekran görüntülerinde yer alan kelime, sözlük (1.500+ madde), diyalog (60 diyalog) ve cümle (7.952 cümle) sayıları yalnızca uygulama ilk kurulduğunda kullanıcının boş bir ekranla karşılaşmaması için sunulan **hazır başlangıç veri setidir**.",
    "- Uygulamanın asıl devrimsel gücü, sabit içerikli bir program olmaması; **%100 özelleştirilebilir bir eğitim ve içerik motoru** olmasıdır.",
    "- **Uygulama içerisinde hiçbir veri olmasa bile (veya kullanıcı mevcut tüm verileri sıfırlasa bile)**, her öğretmen, öğrenci veya eğitim kurumu hiçbir kodlama bilmeden kendi ders kitabını, kendi kelimelerini, kendi diyalog senaryolarını, cümlelerini, görsellerini ve referans seslerini dakikalar içinde sisteme ekleyebilir.",
    "- Kullanıcılar yeni içerik yüklerken mevcut verilerle **Birleştirme/Güncelleme** yapabilecekleri gibi, **Tam Sıfırlama** seçeneğiyle varsayılan verileri silip programı tamamen kendi özel müfredatlarına dönüştürebilir ve hazırladıkları bu yeni paketleri `.ZIP` arşivi olarak dışa aktarıp öğrencileriyle paylaşabilirler.\n",
    "---\n",
    "## ℹ️ YENİ ÜST BAR UYGULAMA İKONU VE 'HAKKINDA & KILAVUZ MERKEZİ' PENCERESİ\n",
    "- Uygulamanın sağ üst köşesinde uygulamanın kendi özel logosu (`app_icon.png`) ve yanında **`ℹ️` (Info / Hakkında)** ikonu yer alır.",
    "- Kullanıcı `ℹ️` ikonuna tıkladığında global mağaza uygulamaları tarzında şık bir **Uygulama Hakkında ve Kılavuz Merkezi** penceresi açılır.",
    "- Bu pencereden tek tıkla **1) YouTube Sesli & Görüntülü Tanıtım Videosuna**, **2) Web Tanıtım ve Kılavuz Sayfasına (`arapca.muallimun.net`)** ve **3) Kapsamlı A4 PDF Kullanım Kılavuzuna** doğrudan erişilir. Pencerenin alt barında ise Muallimun.Net geliştirici imzası ve bağlantısı yer alır.\n",
    "---\n"
]

for ch in CHAPTERS:
    md_lines.append(f"## Bölüm {ch['num']}: {ch['title']}")
    md_lines.append(f"**{ch['subtitle']}**\n")
    md_lines.append(ch["intro"] + "\n")
    md_lines.append("### Öne Çıkan Özellikler ve Kabiliyetler:")
    for ht, hd in ch["highlights"]:
        md_lines.append(f"- **{ht}** {hd}")
    md_lines.append("\n### İlgili Ekran Görüntüleri ve Kullanım İpuçları (Toplam 27 Özgün Ekran):")
    for sc in ch["screens"]:
        md_lines.append(f"#### 📸 Ekran #{sc['sc_no']} (Screenshot_{sc['sc_no']}.png): {sc['title']}")
        md_lines.append(sc["desc"])
        for t in sc["tips"]:
            md_lines.append(f"  - *Kullanım İpucu:* {t}")
        md_lines.append("")

md_lines.extend([
    "---\n",
    "## 🛠️ İÇERİK ÜRETİCİLERİ VE ÖĞRETMENLER İÇİN 5 FARKLI VERİ EKLEME YÖNTEMİ\n",
    "Kullanıcılar Yönetim & Paket Paneli (`Screenshot_18.png` .. `Screenshot_21.png`) üzerinden şu 5 yöntemle kendi içeriklerini oluşturabilirler:",
    "1. **Alt Formdan Tekil Ekleme ve Mikrofon Kaydı:** Paket adı, CEFR seviyesi (A1-C1), Türkçe ve Arapça metin girilerek tek tıkla kayıt eklenir. Öğretmen '🎙️ Kaydet' butonuyla kendi sesini doğrudan referans ses olarak kaydedebilir.",
    "2. **Excel veya Word Tablosundan Doğrudan Kopyala-Yapıştır (`📋 Excel Yapıştır` - `Screenshot_20.png`):** Dosya kaydetmeye gerek kalmadan Excel'deki 2 sütunlu (Arapça | Türkçe), 3 sütunlu (Arapça | Türkçe | Seviye) veya 4 sütunlu hücreler kopyalanıp doğrudan yapıştırılır. Hatalı veya boş satırlar işlemi durdurmaz; satır numarasıyla raporlanır.",
    "3. **CSV ve JSON Dosyaları İle Toplu Paket Yükleme (`📥 Paket Yükle`):** `kelimeler.csv`, `cumleler.csv` veya `diyaloglar.json` şablonlarıyla binlerce kayıt saniyeler içinde aktarılır.",
    "4. **Görselli ve Sesli Tam Paket Arşivi (`.ZIP`) Yükleme ve Dışa Aktarma (`📤 Dışa Aktar`):** İçinde veri dosyası, `images/` ve `sounds/` klasörleri bulunan `.ZIP` paketleri tek tıkla kurulur veya mevcut bir paket tüm medyasıyla `.ZIP` olarak dışa aktarılır.",
    "5. **Sarf Sözlüğü (`sozluk.json`) ve Klasörden Toplu Medya Eşleştirme (`🖼️ Toplu Medya Eşleştir`):** Klasördeki görsel (`.jpg/.png`) ve ses (`.mp3/.wav`) dosyaları, kelimenin ID'si veya Türkçe adına göre ('Arı' ➔ `ari.jpg`, `ari_f.mp3`) otomatik olarak eşleştirilir."
])

md_path = os.path.join(OUT_DIR, "NotebookLM_Kaynak_Metni.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))
print(f"✅ NotebookLM Kaynak Dokümanı güncellendi: {md_path}")


# ==============================================================================
# 3. ÇIKTI: OTOMATİK A4 PDF DÖNÜŞTÜRME
# ==============================================================================
pdf_out_path = os.path.join(OUT_DIR, "Arapca_Telaffuz_Asistani_Kullanim_Kilavuzu.pdf")
browser_candidates = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
browser_exe = next((b for b in browser_candidates if os.path.exists(b)), None)

if browser_exe:
    print("⏳ Yeni A4 PDF Kılavuzu üretiliyor...")
    try:
        file_url = "file:///" + os.path.abspath(manual_html_path).replace("\\", "/")
        subprocess.run([
            browser_exe,
            "--headless",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_out_path}",
            file_url
        ], check=True, timeout=60)
        if os.path.exists(pdf_out_path):
            sz_mb = round(os.path.getsize(pdf_out_path) / (1024 * 1024), 2)
            print(f"🎉 YENİ PDF KULLANIM KILAVUZU HAZIR! ({sz_mb} MB) ➔ {pdf_out_path}")
    except Exception as ex:
        print(f"ℹ️ Otomatik PDF yazdırma bilgisi: {ex}. Açık olan PDF varsa kapatıp tekrar deneyin.")

webbrowser.open("file:///" + os.path.abspath(pdf_out_path).replace("\\", "/"))
webbrowser.open("file:///" + os.path.abspath(web_html_path).replace("\\", "/"))
print("=" * 72)