@echo off
echo [FORCE PUSH] Forcing all files to GitHub
echo =========================================
echo.

cd /d F:\AiKlientBank\KingLearComic

echo [WARNING] This will REPLACE everything on GitHub with your local version!
echo.
pause

echo.
echo [STEP 1] Force pushing to GitHub...
git push origin main --force

echo.
echo =========================================
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] All files force pushed to GitHub!
    echo.
    echo Your project is now live at:
    echo https://github.com/Alex16111977/comic-website
) else (
    echo [ERROR] Push failed. Try manual commands:
    echo   git pull origin main
    echo   git push origin main
)
echo.
pause
