; Inno Setup 6 Script — Arapça Telaffuz ve Konuşma Asistanı
; Muallimun.Net (v40.0 Gold Master)

#define MyAppName "Arapça Telaffuz ve Konuşma Asistanı"
#define MyAppVersion "40.0"
#define MyAppPublisher "Muallimun.Net"
#define MyAppURL "https://www.muallimun.com"
#define MyAppExeName "ArapcaAsistani.exe"

[Setup]
AppId={{D37F8E41-89B2-4A8E-BF88-39F80C9C7E41}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL=https://github.com/muallimun/arapca-telaffuz-asistani
DefaultDirName={autopf}\Muallimun\ArapcaAsistani
DisableProgramGroupPage=yes
LicenseFile=LICENSE
OutputDir=Output
OutputBaseFilename=Arapca_Telaffuz_Asistani_v40_Kurulum
SetupIconFile=ui\app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\ArapcaAsistani\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "ui\app_icon.ico"; DestDir: "{app}\ui"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\ui\app_icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\ui\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent