# -*- coding: utf-8 -*-
"""
setup_hazirla.py — Inno Setup İçin Tanıtım Metinleri, Banner Görselleri ve installer.iss Üretici
Çalıştırma: .\.venv\Scripts\python.exe setup_hazirla.py
"""

import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETUP_ASSETS_DIR = os.path.join(BASE_DIR, "setup_files")
os.makedirs(SETUP_ASSETS_DIR, exist_ok=True)

# 1. Sihirbaz Görsellerini (BMP) ui/app_icon.png'den Otomatik Üret
icon_png = os.path.join(BASE_DIR, "ui", "app_icon.png")
small_bmp = os.path.join(SETUP_ASSETS_DIR, "wizard_small.bmp")
large_bmp = os.path.join(SETUP_ASSETS_DIR, "wizard_large.bmp")

if os.path.exists(icon_png):
    img = Image.open(icon_png).convert("RGBA")

    # Sağ üst köşe logosu (128x128)
    bg_small = Image.new("RGB", (128, 128), (15, 23, 42))  # #0f172a
    ico_s = img.copy()
    ico_s.thumbnail((112, 112), Image.LANCZOS)
    bg_small.paste(ico_s, ((128 - ico_s.width) // 2, (128 - ico_s.height) // 2), ico_s)
    bg_small.save(small_bmp, format="BMP")

    # Sol karşılama banner görseli (164x314)
    bg_large = Image.new("RGB", (164, 314), (15, 23, 42))  # #0f172a
    ico_l = img.copy()
    ico_l.thumbnail((136, 136), Image.LANCZOS)
    bg_large.paste(ico_l, ((164 - ico_l.width) // 2, 70), ico_l)
    bg_large.save(large_bmp, format="BMP")
    print("✅ Kurulum sihirbazı BMP görselleri oluşturuldu.")

# 2. Lisans Sözleşmesi Metni (UTF-8 BOM)
lisans_metni = """========================================================================
ARAPÇA TELAFFUZ VE KONUŞMA ASİSTANI
KULLANIM VE LİSANS SÖZLEŞMESİ — MUALLİMUN.NET
========================================================================

1. KULLANIM AMACI VE LİSANS HAKKI
Bu yazılım; Arapça öğrenen öğrenciler, öğretmenler, İmam Hatip Liseleri,
İlahiyat Fakülteleri ve bireysel kullanıcılar için Muallimun.Net tarafından
geliştirilmiş yapay zekâ destekli bir telaffuz (mahreç), sarf (kök/türev)
ve konuşma (muhâdese) eğitim laboratuvarıdır.

2. EĞİTİMDE ÜCRETSİZ KULLANIM VE DAĞITIM
• Bu uygulama eğitim kurumlarında, akıllı tahtalarda ve kişisel bilgisayarlarda
  ücretsiz olarak kurulabilir, kullanılabilir ve çoğaltılabilir.
• Öğretmenler uygulama içindeki "Yönetim & Paket Paneli" ve "Yazılı Sınav &
  Ders Notu Üretici" araçlarıyla kendi eğitim materyallerini hazırlayabilir.

3. VERİ GİZLİLİĞİ VE ÇEVRİMDIŞI ÇALIŞMA
• Uygulama içindeki konuşma tanıma motoru (Faster-Whisper) ve veritabanları
  (SQLite) tamamen bilgisayarınızda yerel (çevrimdışı) olarak çalışır.
• Öğrenci ses kayıtları yalnızca kendi bilgisayarınızdaki "recordings/"
  klasöründe saklanır; dış sunuculara gönderilmez.

Resmî Web Sitesi : https://www.muallimun.com
GitHub Deposu    : https://github.com/muallimun/arapca-telaffuz-asistani
========================================================================
"""

# 3. Kurulum Öncesi Program Tanıtımı ve Kurulum Adımları (UTF-8 BOM)
tanitim_metni = """========================================================================
🌟 ARAPÇA TELAFFUZ VE KONUŞMA ASİSTANI'NA HOŞ GELDİNİZ!
========================================================================

Bu kurulum sihirbazı, "Arapça Telaffuz ve Konuşma Asistanı"
uygulamasını bilgisayarınıza kuracaktır.

------------------------------------------------------------------------
📌 PROGRAMIN TEMEL ÖZELLİKLERİ VE MODÜLLERİ
------------------------------------------------------------------------
1. 🏠 Görselli Kelime Modu & Gölgeleme (Shadowing):
   • Kadın ve erkek referans sesleriyle kelimeleri dinleyin.
   • Mikrofona konuşarak yapay zekâ ile telaffuz doğruluğunuzu test edin.
   • "Günün 15 Tekrarı (SM-2)" ile kelimeleri kalıcı hafızaya aktarın.

2. 📖 Sarf Sözlüğü & Sülâsî Kök Ailesi Atölyesi:
   • 1.500+ kelimenin 3 harfli sülâsî köklerini (Altıgen Kök Rozeti),
     Müfret/Cemî ve Mâzî/Muzâri/Masdar çekimlerini etkileşimli keşfedin.

3. 💬 Günlük Diyaloglar (Muhâdesât) & Karşılıklı Rol Yapma (Roleplay):
   • Günlük hayat diyaloglarını satır satır dinleyin veya bir rol seçerek
     bilgisayarla karşılıklı Arapça konuşma canlandırması yapın.

4. 📜 Anahtar Cümleler & 🎯 Canlı Mahreç Koçu:
   • Cümle içindeki doğru (yeşil) ve hatalı (kırmızı) kelimeleri anında görün.
   • Birbirine karıştırılan harfler (ص-س, ذ-ز, ع-ء, ط-ت, ق-ك vb.) ve med
     uzatmaları için Canlı Mahreç Koçundan anında pedagojik ipucu alın.

5. 🎧 Dinle & Bul Sınav Merkezi ve 🖨️ A4 Yazılı Sınav / Ders Notu Üretici:
   • 4 şıklı sesli dinleme sınavları çözün.
   • Öğretmenler için tek tıkla cevap anahtarlı A4 yazılı sınav kağıdı veya
     iki sütunlu/harekeli temiz ders notu (PDF/HTML) üretin.

------------------------------------------------------------------------
🛠️ KURULUM ADIMLARI (5 KOLAY ADIM)
------------------------------------------------------------------------
• Adım 1 : Lisans sözleşmesini onaylayın ve bu tanıtım ekranını geçin.
• Adım 2 : Kurulum klasörünü seçin (Varsayılan klasör önerilir).
• Adım 3 : "Masaüstü kısayolu oluştur" seçeneğini işaretleyin.
• Adım 4 : "Kur (Install)" butonuna basarak dosyaların kopyalanmasını bekleyin.
• Adım 5 : Kurulum tamamlandığında uygulamayı doğrudan başlatın.
========================================================================
"""

# 4. Kurulum Sonrası İlk Kullanım ve Kısayol Rehberi (UTF-8 BOM)
sonraki_metin = """========================================================================
🎉 KURULUM BAŞARIYLA TAMAMLANDI! — İLK KULLANIM İPUÇLARI
========================================================================

Uygulama bilgisayarınıza başarıyla kuruldu. Başlamadan önce şu pratik
bilgilere göz atabilirsiniz:

🎙️ 1. MİKROFON İZNİ VE KULLANIMI
• Telaffuz değerlendirmesi için bilgisayarınıza bağlı bir mikrofon bulunmalıdır.
• Windows "Ayarlar > Gizlilik > Mikrofon" bölümünden masaüstü uygulamalarının
  mikrofon erişimine izin verildiğinden emin olun.

⌨️ 2. PRATİK KLAVYE KISAYOLLARI
• [Boşluk / Space]   : Ses kaydını başlatır veya durdurur.
• [Sağ Ok / Sol Ok]  : Sonraki veya önceki kelime/cümle kartına geçer.
• [F1]               : Uygulama içi kapsamlı Kullanım Kılavuzunu açar.

🔄 3. OTOMATİK GÜNCELLEME VE KALDIRMA (UNINSTALL)
• Uygulama, üst çubuktaki "🔄" butonuyla GitHub üzerinden yeni sürümleri
  otomatik kontrol eder ve verilerinizi koruyarak günceller.
• Uygulamayı istediğiniz zaman "Denetim Masası > Program Ekle/Kaldır"
  veya Başlat Menüsündeki "Arapça Asistanı'nı Kaldır" kısayoluyla
  bilgisayarınızdan tamamen kaldırabilirsiniz.
========================================================================
"""

with open(os.path.join(SETUP_ASSETS_DIR, "lisans_sozlesmesi.txt"), "w", encoding="utf-8-sig") as f:
    f.write(lisans_metni)

with open(os.path.join(SETUP_ASSETS_DIR, "tanitim_ve_adimlar.txt"), "w", encoding="utf-8-sig") as f:
    f.write(tanitim_metni)

with open(os.path.join(SETUP_ASSETS_DIR, "ilk_kullanim_rehberi.txt"), "w", encoding="utf-8-sig") as f:
    f.write(sonraki_metin)

print("✅ Kurulum metin dosyaları (UTF-8 BOM) oluşturuldu.")

# 5. Öncelikli olarak yeni derlenen dist\ArapcaAsistani klasörünü seç
if os.path.exists(os.path.join(BASE_DIR, "dist", "ArapcaAsistani", "ArapcaAsistani.exe")):
    source_dir = r"dist\ArapcaAsistani"
else:
    source_dir = "ArapcaAsistani"

iss_content = f"""; =====================================================================
; Inno Setup 6 Profesyonel Kurulum Betiği (installer.iss)
; Uygulama : Arapça Telaffuz ve Konuşma Asistanı 
; Yayıncı  : Muallimun.Net (https://www.muallimun.com)
; =====================================================================

#define MyAppName "Arapça Telaffuz ve Konuşma Asistanı"
#define MyAppShortName "Arapça Telaffuz Asistanı"
#define MyAppVersion "40.0"
#define MyAppPublisher "Muallimun.Net"
#define MyAppURL "https://www.muallimun.com"
#define MyAppRepoURL "https://github.com/muallimun/arapca-telaffuz-asistani"
#define MyAppExeName "ArapcaAsistani.exe"
#define MySourceDir "{source_dir}"

[Setup]
AppId={{{{D37F8E41-89B2-4A8E-BF88-39F80C9C7E41}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppVerName={{#MyAppName}} v{{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppRepoURL}}
AppUpdatesURL={{#MyAppRepoURL}}
AppCopyright=Copyright (C) 2026 {{#MyAppPublisher}}
AppMutex=Muallimun_ArapcaAsistani_SingleInstance_Mutex_v40

; Kurulum Dizini ve Başlat Menüsü Grubu
DefaultDirName={{autopf}}\\Muallimun\\ArapcaAsistani
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes

; Tanıtım, Lisans ve Kurulum Sonrası Bilgilendirme Sayfaları
LicenseFile=setup_files\\lisans_sozlesmesi.txt
InfoBeforeFile=setup_files\\tanitim_ve_adimlar.txt
InfoAfterFile=setup_files\\ilk_kullanim_rehberi.txt

; Görsel Tasarım ve İkonlar
SetupIconFile=ui\\app_icon.ico
WizardStyle=modern
WizardSizePercent=115,115
WizardImageFile=setup_files\\wizard_large.bmp
WizardSmallImageFile=setup_files\\wizard_small.bmp

; Kaldırma (Uninstall) ve Denetim Masası Entegrasyonu
Uninstallable=yes
UninstallDisplayName={{#MyAppName}} v{{#MyAppVersion}}
UninstallDisplayIcon={{app}}\\{{#MyAppExeName}}
CreateUninstallRegKey=yes

; Standart Çıktı Dosyası Adı ve Yüksek Sıkıştırma Ayarları
OutputDir=Output
OutputBaseFilename=Arapca_Telaffuz_Asistani_Setup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\\Turkish.isl"

[Messages]
turkish.WelcomeLabel1={{#MyAppName}} Kurulum Sihirbazına Hoş Geldiniz
turkish.WelcomeLabel2=Bu sihirbaz bilgisayarınıza {{#MyAppName}} (v{{#MyAppVersion}}) uygulamasını kuracaktır.%n%nYapay zekâ destekli Arapça telaffuz (mahreç), sarf sözlüğü, diyalog canlandırma ve yazılı sınav/ders notu üretim araçları tek pakette sunulmaktadır.%n%nDevam etmeden önce açık olan diğer uygulamaları kapatmanız önerilir.
turkish.FinishedHeadingLabel={{#MyAppName}} Kurulumu Tamamlandı!
turkish.FinishedLabel=Uygulama bilgisayarınıza başarıyla kuruldu. Masaüstündeki veya Başlat Menüsündeki simgeye tıklayarak programı çalıştırabilirsiniz.

[Tasks]
Name: "desktopicon"; Description: "Masaüstünde kısayol simgesi oluştur (Önerilen)"; GroupDescription: "Kısayol Seçenekleri:"
Name: "quicklaunchicon"; Description: "Hızlı Başlat çubuğunda kısayol oluştur"; GroupDescription: "Kısayol Seçenekleri:"; Flags: unchecked

; Program Files içine kurulduğunda veritabanı ve ses kayıtlarının hata vermemesi için yazma izinleri
[Dirs]
Name: "{{app}}"; Permissions: users-modify
Name: "{{app}}\\data"; Permissions: users-modify
Name: "{{app}}\\assets"; Permissions: users-modify
Name: "{{app}}\\assets\\tts_cache"; Permissions: users-modify
Name: "{{app}}\\assets\\custom_audio"; Permissions: users-modify
Name: "{{app}}\\assets\\categories"; Permissions: users-modify
Name: "{{app}}\\recordings"; Permissions: users-modify

[Files]
Source: "{{#MySourceDir}}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "ui\\app_icon.ico"; DestDir: "{{app}}\\ui"; Flags: ignoreversion

[Icons]
; Başlat Menüsü Kısayolları (Uygulama + Kaldırma Sihirbazı)
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; WorkingDir: "{{app}}"; IconFilename: "{{app}}\\ui\\app_icon.ico"; Comment: "Yapay Zekâ Destekli Arapça Telaffuz ve Konuşma Laboratuvarı"
Name: "{{group}}\\🌐 Muallimun.Net Web Sitesi"; Filename: "{{#MyAppURL}}"
Name: "{{group}}\\🗑️ {{#MyAppShortName}} Uygulamasını Kaldır"; Filename: "{{uninstallexe}}"

; Masaüstü ve Hızlı Başlat Kısayolları
Name: "{{autodesktop}}\\{{#MyAppShortName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; WorkingDir: "{{app}}"; IconFilename: "{{app}}\\ui\\app_icon.ico"; Tasks: desktopicon; Comment: "{{#MyAppName}} v{{#MyAppVersion}}"
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{{#MyAppShortName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; WorkingDir: "{{app}}"; IconFilename: "{{app}}\\ui\\app_icon.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{#MyAppName}} uygulamasını şimdi başlat"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{app}}\\__pycache__"
Type: files; Name: "{{app}}\\uygulama.log"

[Code]
// 1. Mevcut kurulumun kaldırma (Uninstall) dosya yolunu Kayıt Defteri'nden bulur
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := 'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{{D37F8E41-89B2-4A8E-BF88-39F80C9C7E41}}_is1';
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    if not RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString) then
      if not RegQueryStringValue(HKLM32, sUnInstPath, 'UninstallString', sUnInstallString) then
        RegQueryStringValue(HKCU32, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

// 2. Kurulum başlarken uygulama zaten kuruluysa kullanıcıyı uyarır, önce eski sürümü kaldırır ve sonra yenisini kurar
function InitializeSetup(): Boolean;
var
  sUnInstallString: String;
  iResultCode: Integer;
  iWaitCount: Integer;
begin
  Result := True;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then
  begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if FileExists(sUnInstallString) then
    begin
      if MsgBox('Bilgisayarınızda "' + '{{#MyAppName}}' + '" zaten kurulu görünüyor.' + #13#10 + #13#10 +
                'Yeni kurulumun temiz ve sorunsuz yapılabilmesi için önce mevcut kurulum kaldırılacak, hemen ardından yeni kurulum başlatılacaktır.' + #13#10 + #13#10 +
                'Önceki kurulumu kaldırıp yeni kuruluma devam etmek istiyor musunuz?',
                mbConfirmation, MB_YESNO or MB_DEFBUTTON1) = IDYES then
      begin
        if not Exec(sUnInstallString, '/SILENT /NORESTART', '', SW_SHOW, ewWaitUntilTerminated, iResultCode) then
        begin
          MsgBox('Önceki sürüm kaldırılırken bir hata oluştu (Hata Kodu: ' + IntToStr(iResultCode) + '). Kurulum iptal edildi.', mbError, MB_OK);
          Result := False;
        end
        else
        begin
          // Arka plandaki kaldırma işleminin dosyaları tamamen temizlemesini bekle
          iWaitCount := 0;
          while FileExists(sUnInstallString) and (iWaitCount < 60) do
          begin
            Sleep(300);
            iWaitCount := iWaitCount + 1;
          end;
        end;
      end
      else
      begin
        Result := False;
      end;
    end;
  end;
end;

// 3. Kaldırma (Uninstall) sırasında kullanıcıya çalışma verilerini ve ses kayıtlarını silmek isteyip istemediğini sorar
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if DirExists(ExpandConstant('{{app}}\\recordings')) or DirExists(ExpandConstant('{{app}}\\data')) then
    begin
      if MsgBox('Uygulama dosyaları kaldırıldı.' + #13#10 + #13#10 +
                'Öğrenci çalışma istatistiklerinizi, sonradan eklediğiniz ses kayıtlarını (recordings/) ve önbellek dosyalarını da tamamen silmek ister misiniz?' + #13#10 +
                '(Yeni sürümü kuruyorsanız veya verilerinizi korumak istiyorsanız "Hayır" seçeneğine tıklayın.)',
                mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
      begin
        DelTree(ExpandConstant('{{app}}'), True, True, True);
      end;
    end;
  end;
end;
"""

iss_path = os.path.join(BASE_DIR, "installer.iss")
with open(iss_path, "w", encoding="utf-8-sig") as f:
    f.write(iss_content)

print(f"✅ 'installer.iss' başarıyla oluşturuldu (Kaynak: {source_dir}, Çıktı: Arapca_Telaffuz_Asistani_Setup.exe).")