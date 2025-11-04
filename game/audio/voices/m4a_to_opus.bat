@echo off
for %%a in (*.wav) do ffmpeg -i "%%a" -c:a libopus -b:a 64k "%%~na.opus"
pause
