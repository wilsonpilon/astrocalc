@echo off
setlocal

set "EMULATOR=%~dp0..\MSXgl\tools\build\standalone\Emulicious\Emulicious.exe"
set "DISK=%~dp0emul\dsk\DOS2_matstar.dsk"

if not exist "%EMULATOR%" (
	echo Error: Emulicious was not found at:
	echo %EMULATOR%
	exit /b 1
)

if not exist "%DISK%" (
	echo Error: Build the project before running it.
	echo Missing: %DISK%
	exit /b 1
)

start "" "%EMULATOR%" ^
	-set System=MSX ^
	-set MSXModel=1 ^
	-set MSXPAL=true ^
	-set MSXRAMBankShift=4 ^
	"%DISK%"
