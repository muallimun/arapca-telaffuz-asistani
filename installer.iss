; =====================================================================
; Inno Setup 6 Profesyonel Kurulum Betiği (installer.iss)
; Uygulama : Arapça Telaffuz ve Konuşma Asistanı v40.0 Gold Master
; Yayıncı  : Muallimun.Net (https://www.muallimun.com)
; =====================================================================

#define MyAppName "Arapça Telaffuz ve Konuşma Asistanı"
#define MyAppShortName "Arapça Telaffuz Asistanı"
#define MyAppVersion "40.0"
#define MyAppPublisher "Muallimun.Net"
#define MyAppURL "https://www.muallimun.com"
#define MyAppRepoURL "https://github.com/muallimun/arapca-telaffuz-asistani"
#define MyAppExeName "ArapcaAsistani.exe"
#define MySourceDir "ArapcaAsistani"

[Setup]
AppId={{D37F8E41-89B2-4A8E-BF88-39F80C9C7E41}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppRepoURL}
AppUpdatesURL={#MyAppRepoURL}
AppCopyright=Copyright (C) 2026 {#MyAppPublisher}
AppMutex=Muallimun_ArapcaAsistani_SingleInstance_Mutex_v40

; Kurulum Dizini ve Başlat Menüsü Grubu
DefaultDirName={autopf}\Muallimun\ArapcaAsistani
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; Tanıtım, Lisans ve Kurulum Sonrası Bilgilendirme Sayfaları
LicenseFile=setup_files\lisans_sozlesmesi.txt
InfoBeforeFile=setup_files\tanitim_ve_adimlar.txt
InfoAfterFile=setup_files\ilk_kullanim_rehberi.txt

; Görsel Tasarım ve İkonlar
SetupIconFile=ui\app_icon.ico
WizardStyle=modern
WizardSizePercent=115,115
WizardImageFile=setup_files\wizard_large.bmp
WizardSmallImageFile=setup_files\wizard_small.bmp

; Kaldırma (Uninstall) ve Denetim Masası Entegrasyonu
Uninstallable=yes
UninstallDisplayName={#MyAppName} v{#MyAppVersion}
UninstallDisplayIcon={app}\{#MyAppExeName}
CreateUninstallRegKey=yes

; Çıktı ve Yüksek Sıkıştırma Ayarları (~300 MB -> ~100 MB)
OutputDir=Output
OutputBaseFilename=Arapca_Telaffuz_Asistani_Setup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Messages]
turkish.WelcomeLabel1={#MyAppName} Kurulum Sihirbazına Hoş Geldiniz
turkish.WelcomeLabel2=Bu sihirbaz bilgisayarınıza {#MyAppName} (v{#MyAppVersion}) uygulamasını kuracaktır.%n%nYapay zekâ destekli Arapça telaffuz (mahreç), sarf sözlüğü, diyalog canlandırma ve yazılı sınav/ders notu üretim araçları tek pakette sunulmaktadır.%n%nDevam etmeden önce açık olan diğer uygulamaları kapatmanız önerilir.
turkish.FinishedHeadingLabel={#MyAppName} Kurulumu Tamamlandı!
turkish.FinishedLabel=Uygulama bilgisayarınıza başarıyla kuruldu. Masaüstündeki veya Başlat Menüsündeki simgeye tıklayarak programı çalıştırabilirsiniz.

[Tasks]
Name: "desktopicon"; Description: "Masaüstünde kısayol simgesi oluştur (Önerilen)"; GroupDescription: "Kısayol Seçenekleri:"
Name: "quicklaunchicon"; Description: "Hızlı Başlat çubuğunda kısayol oluştur"; GroupDescription: "Kısayol Seçenekleri:"; Flags: unchecked

; Program Files içine kurulduğunda veritabanı ve ses kayıtlarının hata vermemesi için yazma izinleri
[Dirs]
Name: "{app}"; Permissions: users-modify
Name: "{app}\data"; Permissions: users-modify
Name: "{app}\assets"; Permissions: users-modify
Name: "{app}\assets\tts_cache"; Permissions: users-modify
Name: "{app}\assets\custom_audio"; Permissions: users-modify
Name: "{app}\assets\categories"; Permissions: users-modify
Name: "{app}\recordings"; Permissions: users-modify

[Files]
Source: "{#MySourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "ui\app_icon.ico"; DestDir: "{app}\ui"; Flags: ignoreversion

[Icons]
; Başlat Menüsü Kısayolları (Uygulama + Kaldırma Sihirbazı)
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\ui\app_icon.ico"; Comment: "Yapay Zekâ Destekli Arapça Telaffuz ve Konuşma Laboratuvarı"
Name: "{group}\🌐 Muallimun.Net Web Sitesi"; Filename: "{#MyAppURL}"
Name: "{group}\🗑️ {#MyAppShortName} Uygulamasını Kaldır"; Filename: "{uninstallexe}"

; Masaüstü ve Hızlı Başlat Kısayolları
Name: "{autodesktop}\{#MyAppShortName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\ui\app_icon.ico"; Tasks: desktopicon; Comment: "{#MyAppName} v{#MyAppVersion}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppShortName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\ui\app_icon.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{#MyAppName} uygulamasını şimdi başlat"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\__pycache__"
Type: files; Name: "{app}\uygulama.log"

[Code]
// Kaldırma (Uninstall) sırasında kullanıcıya çalışma verilerini ve ses kayıtlarını silmek isteyip istemediğini sorar
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if DirExists(ExpandConstant('{app}\recordings')) or DirExists(ExpandConstant('{app}\data')) then
    begin
      if MsgBox('Uygulama dosyaları kaldırıldı.' + #13#10 + #13#10 +
                'Öğrenci çalışma istatistiklerinizi, sonradan eklediğiniz ses kayıtlarını (recordings/) ve önbellek dosyalarını da tamamen silmek ister misiniz?' + #13#10 +
                '(Daha sonra tekrar kurmayı düşünüyorsanız "Hayır" diyerek verilerinizi koruyabilirsiniz.)',
                mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES then
      begin
        DelTree(ExpandConstant('{app}'), True, True, True);
      end;
    end;
  end;
end;
