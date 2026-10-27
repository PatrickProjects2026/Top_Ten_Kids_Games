@echo off
:start
cls
echo [1/3] Compiling C++ Engine...
g++ engine.cpp -o engine.exe
if %errorlevel% neq 0 (
    echo !!! C++ Compilation Failed !!!
    pause
    goto start
)

echo [2/3] Compiling Java Boss...
javac Boss.java
if %errorlevel% neq 0 (
    echo !!! Java Compilation Failed !!!
    pause
    goto start
)

echo [3/3] Launching Polyglot Chain...
echo ---------------------------------------
java Boss
echo ---------------------------------------

echo.
echo Press any key to recompile and run again...
pause > nul
goto start