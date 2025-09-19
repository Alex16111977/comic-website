@echo off
echo [FULL PUSH] Pushing ALL project files to GitHub
echo ============================================
echo.

cd /d F:\AiKlientBank\KingLearComic

echo [STEP 1] Adding ALL files to Git...
git add .

echo.
echo [STEP 2] Creating commit with all files...
git commit -m "Complete project: King Lear Comic Generator with all 12 characters, generators, and output"

echo.
echo [STEP 3] Pushing everything to GitHub...
git push origin main

echo.
echo ============================================
echo [SUCCESS] All files pushed to GitHub!
echo.
echo Check: https://github.com/Alex16111977/comic-website
echo.
pause
