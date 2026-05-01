@echo off
setlocal
cd /d "%~dp0"

:: Remove old .bat launcher from desktop if it exists
if exist "%USERPROFILE%\Desktop\Local File Search.bat" del "%USERPROFILE%\Desktop\Local File Search.bat"
if exist "%USERPROFILE%\Desktop\Local File Search.lnk" del "%USERPROFILE%\Desktop\Local File Search.lnk"

:: Create a local launcher script to ensure reliability
echo @echo off > run_app.bat
echo cd /d "%%~dp0" >> run_app.bat
echo start "" python desktop_app.py >> run_app.bat

:: Create Desktop Shortcut with custom Icon
echo [INFO] Creating Desktop Shortcut with Icon...
set "VBS_SCRIPT=%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_SCRIPT%"
echo sLinkFile = "%USERPROFILE%\Desktop\Local File Search.lnk" >> "%VBS_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_SCRIPT%"
echo oLink.TargetPath = "%CD%\run_app.bat" >> "%VBS_SCRIPT%"
echo oLink.WorkingDirectory = "%CD%" >> "%VBS_SCRIPT%"
echo oLink.IconLocation = "%CD%\icon.ico" >> "%VBS_SCRIPT%"
echo oLink.WindowStyle = 7 >> "%VBS_SCRIPT%"
echo oLink.Save >> "%VBS_SCRIPT%"

cscript /nologo "%VBS_SCRIPT%"
del "%VBS_SCRIPT%"
echo [INFO] Desktop shortcut created successfully!
