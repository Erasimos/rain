@echo off

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b
)

echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies. Please check the error messages above and fix the issues.
    pause
    exit /b
)

IF EXIST "dist\rain.exe" (
    echo Executable already exists. Skipping PyInstaller packaging step.
) ELSE (
    echo Packaging the application with PyInstaller...
    python -m PyInstaller --onefile --add-data "resources/rain.mp4;resources" --add-data "resources/rain.mp3;resources" --add-data "resources/rain.ico;resources" rain.py
    IF %ERRORLEVEL% NEQ 0 (
        echo Error during PyInstaller build process.
        pause
        exit /b
    )
)

IF NOT EXIST "dist\rain.exe" (
    echo Error: Executable not found. Build failed.
    pause
    exit /b
)

echo Installation complete.

pause
