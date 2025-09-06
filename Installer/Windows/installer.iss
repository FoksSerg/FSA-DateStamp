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

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "C:\FSA-DateStamp\Distrib\Windows\FSA-DateStamp.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\FSA-DateStamp\Distrib\Windows\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FSA-DateStamp"; Filename: "{app}\FSA-DateStamp.exe"
Name: "{group}\{cm:UninstallProgram,FSA-DateStamp}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\FSA-DateStamp"; Filename: "{app}\FSA-DateStamp.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\FSA-DateStamp"; Filename: "{app}\FSA-DateStamp.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\FSA-DateStamp.exe"; Description: "{cm:LaunchProgram,FSA-DateStamp}"; Flags: nowait postinstall skipifsilent
