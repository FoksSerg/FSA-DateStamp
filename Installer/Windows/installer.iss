[Setup]
AppName=FSA-DateStamp
AppVersion=1.01.25.249
AppPublisher=AW-Software
AppPublisherURL=https://github.com/foksserg
AppSupportURL=https://github.com/foksserg
AppUpdatesURL=https://github.com/foksserg
DefaultDirName={autopf}\AW-Software\FSA-DateStamp
DefaultGroupName=AW-Software\FSA-DateStamp
AllowNoIcons=yes
LicenseFile=
OutputDir=installer_output
OutputBaseFilename=FSA-DateStamp-Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
MinVersion=6.1

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
; Windows 7 версия
Source: "..\..\Distrib\Windows7\FSA-DateStamp.exe"; DestDir: "{app}\Windows7"; Flags: ignoreversion; Check: IsWindows7
; Windows 8 версия  
Source: "..\..\Distrib\Windows8\FSA-DateStamp.exe"; DestDir: "{app}\Windows8"; Flags: ignoreversion; Check: IsWindows8
; Windows 10 версия
Source: "..\..\Distrib\Windows10\FSA-DateStamp.exe"; DestDir: "{app}\Windows10"; Flags: ignoreversion; Check: IsWindows10
; Windows 11 версия
Source: "..\..\Distrib\Windows11\FSA-DateStamp.exe"; DestDir: "{app}\Windows11"; Flags: ignoreversion; Check: IsWindows11
; Универсальная версия (fallback)
Source: "..\..\Distrib\Universal\FSA-DateStamp.exe"; DestDir: "{app}\Universal"; Flags: ignoreversion; Check: IsUnknownWindows

; Копируем нужную версию в корень приложения
Source: "{app}\Windows7\FSA-DateStamp.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: IsWindows7
Source: "{app}\Windows8\FSA-DateStamp.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: IsWindows8
Source: "{app}\Windows10\FSA-DateStamp.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: IsWindows10
Source: "{app}\Windows11\FSA-DateStamp.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: IsWindows11
Source: "{app}\Universal\FSA-DateStamp.exe"; DestDir: "{app}"; Flags: ignoreversion; Check: IsUnknownWindows

[Icons]
Name: "{group}\FSA-DateStamp"; Filename: "{app}\FSA-DateStamp.exe"
Name: "{group}\{cm:UninstallProgram,FSA-DateStamp}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\FSA-DateStamp"; Filename: "{app}\FSA-DateStamp.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\FSA-DateStamp"; Filename: "{app}\FSA-DateStamp.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\FSA-DateStamp.exe"; Description: "{cm:LaunchProgram,FSA-DateStamp}"; Flags: nowait postinstall skipifsilent

[Code]
function IsWindows7: Boolean;
begin
  Result := (GetWindowsVersion shr 16) = 6.1;
end;

function IsWindows8: Boolean;
var
  Version: Cardinal;
begin
  Version := GetWindowsVersion;
  Result := ((Version shr 16) = 6.2) or ((Version shr 16) = 6.3);
end;

function IsWindows10: Boolean;
begin
  Result := (GetWindowsVersion shr 16) = 10.0;
end;

function IsWindows11: Boolean;
var
  Version: Cardinal;
  BuildNumber: Cardinal;
begin
  Version := GetWindowsVersion;
  BuildNumber := Version and $FFFF;
  Result := ((Version shr 16) = 10.0) and (BuildNumber >= 22000);
end;

function IsUnknownWindows: Boolean;
begin
  Result := not (IsWindows7 or IsWindows8 or IsWindows10 or IsWindows11);
end;
