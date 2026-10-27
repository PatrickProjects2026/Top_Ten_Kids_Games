@echo off
setlocal enabledelayedexpansion
title Polyglot Build System

:start
cls
echo =======================================
echo     POLYGLOT BUILD PIPELINE
echo =======================================

echo [1/3] Compiling C++ Engine...
:: Changed -o engine.exe to -o physics.exe to match game.py
g++ -O3 physics.cpp -o physics.exe
if %errorlevel% neq 0 goto :fail

echo [2/3] Compiling Java Boss...
javac Logger.java
if %errorlevel% neq 0 goto :fail

echo [3/3] Launching Python Game...
echo ---------------------------------------
:: Ensuring the script runs in the local directory
python game.py
echo ---------------------------------------

echo.
echo Success! Press any key to rebuild...
pause > nul
goto start

:fail
echo.
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
echo    BUILD FAILED - CHECK ERRORS
echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
pause
goto start