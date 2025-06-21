@echo off
cls
echo I will now attempt to fix the problem that causes the bot to
echo constantly join and leave the voice channel when using the 
echo /tts, /music, and /pbl commands.
pause
del __pycache__\
rmdir __pycache__\
echo Your bot SHOULD function properly now. If not,
echo go to the github page and file a bug report.
pause