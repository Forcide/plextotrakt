@ECHO OFF

IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
  >nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
  >nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

IF '%ERRORLEVEL%' NEQ '0' (
  ver > nul
  GOTO UACPrompt
) ELSE (
  GOTO gotAdmin
  )

:UACPrompt
  ECHO SET UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
  SET params= %*
  ECHO UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

  "%temp%\getadmin.vbs"
  DEL "%temp%\getadmin.vbs"
  EXIT /B

:gotAdmin
  PUSHD "%CD%"
  CD /D "%~dp0"

python traktapi.py
IF %ERRORLEVEL% EQU 1 (
  ECHO ERROR CONNECTING TO TRAKT
  GOTO :EOF
)
python timezone.py 1
TIMEOUT /T 2 /NOBREAK
START python webhook.py
TIMEOUT /T 5 /NOBREAK
python timezone.py 2
