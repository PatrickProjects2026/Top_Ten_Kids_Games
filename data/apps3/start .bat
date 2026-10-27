@echo off
cls
echo =======================================
echo      LAUNCHING ADVANCED ENGINE
echo =======================================

:: 1. Compile C++ with optimization
echo [*] Compiling C++ Physics Engine...
g++ -O3 physics.cpp -o physics.exe
if %errorlevel% neq 0 goto :fail

:: 2. Compile Java Logger
echo [*] Compiling Java Logger...
javac Logger.java
if %errorlevel% neq 0 goto :fail

:: 3. Run the Game
echo [*] Success! Starting Pygame...
python game.py

pause
exit

:fail
echo.
echo [!] ERROR: Compilation failed. 
echo [!] Check if you have g++ (MinGW) and JDK installed.
pause