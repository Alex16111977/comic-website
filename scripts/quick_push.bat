@echo off
echo [QUICK PUSH] Fast commit and push to GitHub
echo.

cd /d F:\AiKlientBank\KingLearComic

REM Проверяем статус
git status --short

echo.
set /p message="Enter commit message (or press Enter for 'update: changes'): "
if "%message%"=="" set message=update: changes

echo.
echo [1/3] Adding files...
git add .

echo [2/3] Creating commit: %message%
git commit -m "%message%"

echo [3/3] Pushing to GitHub...
git push

echo.
echo [SUCCESS] Changes pushed to https://github.com/Alex16111977/comic-website
echo.
pause
