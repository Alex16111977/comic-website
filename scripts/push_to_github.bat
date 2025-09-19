@echo off
echo [INFO] Finalizing Git setup for King Lear Comic Generator
echo.

cd /d F:\AiKlientBank\KingLearComic

echo [STEP 1] Creating initial commit...
git commit -m "Initial commit: King Lear Comic Generator - Educational German learning site through Shakespeare"

echo.
echo [STEP 2] Pushing to GitHub...
echo Note: If repository already has content, you may need to use --force
git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Normal push failed. Try force push? (y/n)
    set /p force=
    if "%force%"=="y" (
        echo [FORCING] Force pushing to origin...
        git push -u origin main --force
    )
)

echo.
echo [SUCCESS] Repository linked to https://github.com/Alex16111977/comic-website
echo.
pause
