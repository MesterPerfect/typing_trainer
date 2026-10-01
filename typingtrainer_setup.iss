#define MyAppName "TypingTrainer - برنامج تدريب الطباعة الميسر"
#define MyAppVersion "1.0.0"
#define AppVersion "1.0.0"
#define MyAppPublisher "MesterPerfect"
#define MyAppURL "https://github.com/MesterPerfect/typing_trainer"
#define MyAppExeName "TypingTrainer.exe"
#define BuildDir "dist\TypingTrainer" 

[Setup]
AppName={#MyAppName}
AppId={{C7B8E9F1-2345-6789-ABCD-EF0123456789}
AppVersion={#AppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
VersionInfoDescription=TypingTrainer - Accessible Typing Tutor
AppPublisher={#MyAppPublisher}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoCopyright=copyright, ©2026; {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoOriginalFileName=TypingTrainer_Setup.exe
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
UninstallDisplayName=TypingTrainer - برنامج تدريب الطباعة الميسر
ArchitecturesAllowed=x64compatible arm64
ArchitecturesInstallIn64BitMode=x64compatible arm64
; Icon file
SetupIconFile=assets\icon.ico

; توجيه التثبيت للمسار المناسب بناءً على صلاحيات المستخدم
DefaultDirName={autopf}\{#MyAppName}

DisableProgramGroupPage=yes
DisableDirPage=no

; الصلاحيات المنخفضة لضمان التحديث الصامت والتثبيت السلس
PrivilegesRequired=lowest

OutputDir=build_installer
OutputBaseFilename=TypingTrainer_Setup_v{#MyAppVersion}
Compression=lzma
CloseApplications=force
restartApplications=yes
SolidCompression=yes
WizardStyle=modern dark polar
DisableWelcomePage=no
MinVersion=0,6.2

Uninstallable=IsNormalInstall
UsedUserAreasWarning=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[CustomMessages]
english.AppLNGfile=English
arabic.AppLNGfile=Arabic
english.DeleteSettingsPrompt=Do you want to delete the user data, settings, and typing results folder?
arabic.DeleteSettingsPrompt=هل تريد حذف مجلد بيانات المستخدم، الإعدادات وسجل نتائج الطباعة؟

english.InstallModeTitle=Installation Mode
arabic.InstallModeTitle=نوع التثبيت
english.InstallModeDesc=Please select how you want to install {#MyAppName}.
arabic.InstallModeDesc=الرجاء تحديد كيف تريد تثبيت {#MyAppName}.
english.InstallModeText=Select Normal Installation for a standard setup with shortcuts, or Portable Version to extract files into a standalone folder without modifying your system registry.
arabic.InstallModeText=حدد "تثبيت عادي" لإعداد قياسي مع اختصارات، أو "نسخة محمولة" لاستخراج الملفات في مجلد مستقل دون تعديل سجل النظام الخاص بك.
english.InstallModeNormal=Normal Installation (Recommended)
arabic.InstallModeNormal=تثبيت عادي (مستحسن)
english.InstallModePortable=Portable Version
arabic.InstallModePortable=نسخة محمولة

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Check: IsNormalInstall

[Files]
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Check: IsNormalInstall
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Check: IsNormalInstall

[UninstallRun]
RunOnceId: "KillTypingTrainer"; Filename: "taskkill"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall

[Code]
var
  InstallModePage: TInputOptionWizardPage;
  IsPortableMode: Boolean;
  UserProvidedDir: String;

function HasCmdLineParam(const ParamName: String): Boolean;
var
  I: Integer;
begin
  Result := False;
  for I := 1 to ParamCount do
  begin
    if CompareText(ParamStr(I), ParamName) = 0 then
    begin
      Result := True;
      Exit;
    end;
  end;
end;

function InitializeSetup(): Boolean;
begin
  IsPortableMode := HasCmdLineParam('/PORTABLE');
  UserProvidedDir := ExpandConstant('{param:DIR}');
  Result := True;
end;

function GetDefaultDirName(Param: String): String;
begin
  if IsPortableMode then
    Result := ExpandConstant('{src}\{#MyAppName}_Portable')
  else
    Result := ExpandConstant('{autopf}\{#MyAppName}');
end;

function IsNormalInstall: Boolean;
begin
  Result := not IsPortableMode;
end;

function IsPortableInstall: Boolean;
begin
  Result := IsPortableMode;
end;

procedure DeleteUserDataFolder();
begin
  DelTree(ExpandConstant('{userappdata}\{#MyAppName}'), True, True, True);
end;

procedure InitializeWizard;
begin
  InstallModePage := CreateInputOptionPage(wpWelcome,
    CustomMessage('InstallModeTitle'), 
    CustomMessage('InstallModeDesc'),
    CustomMessage('InstallModeText'),
    True, False);

  InstallModePage.Add(CustomMessage('InstallModeNormal'));
  InstallModePage.Add(CustomMessage('InstallModePortable'));

  if IsPortableMode then
  begin
    InstallModePage.Values[0] := False;
    InstallModePage.Values[1] := True;
  end
  else
  begin
    InstallModePage.Values[0] := True;
    InstallModePage.Values[1] := False;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  ExpectedNormalDir, ExpectedPortableDir: String;
begin
  if CurPageID = InstallModePage.ID then
  begin
    ExpectedNormalDir := ExpandConstant('{autopf}\{#MyAppName}');
    ExpectedPortableDir := ExpandConstant('{src}\{#MyAppName}_Portable');

    if (UserProvidedDir = '') and
       ((CompareText(WizardForm.DirEdit.Text, ExpectedNormalDir) = 0) or
        (CompareText(WizardForm.DirEdit.Text, ExpectedPortableDir) = 0)) then
    begin
      IsPortableMode := InstallModePage.Values[1];
      if IsPortableMode then
        WizardForm.DirEdit.Text := ExpectedPortableDir
      else
        WizardForm.DirEdit.Text := ExpectedNormalDir;
    end
    else
    begin
      IsPortableMode := InstallModePage.Values[1];
    end;
  end;
  Result := True;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  if ((PageID = wpSelectProgramGroup) or (PageID = wpSelectTasks)) and IsPortableMode then
    Result := True
  else
    Result := False;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    if IsPortableInstall then
    begin
      SaveStringToFile(ExpandConstant('{app}\.portable'), 'This file tells TypingTrainer to run in portable mode.', False);
    end;
  end;
end;

procedure DeinitializeUninstall();
begin
  if MsgBox(
      ExpandConstant('{cm:DeleteSettingsPrompt}') + #13#10 +
      ExpandConstant('{userappdata}\{#MyAppName}'),
      mbConfirmation, MB_YESNO) = IDYES then
  begin
    DeleteUserDataFolder();
  end;
end;
