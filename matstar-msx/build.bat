:: ____________________________
:: ██▀▀█▀▀██▀▀▀▀▀▀▀█▀▀█        │   ▄▄▄                ▄▄
:: ██  ▀  █▄  ▀██▄ ▀ ▄█ ▄▀▀ █  │  ▀█▄  ▄▀██ ▄█▄█ ██▀▄ ██  ▄███
:: █  █ █  ▀▀  ▄█  █  █ ▀▄█ █▄ │  ▄▄█▀ ▀▄██ ██ █ ██▀  ▀█▄ ▀█▄▄
:: ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀────────┘                 ▀▀
::  by Guillaume 'Aoineko' Blanchard under CC BY-SA license
::────────────────────────────────────────────────────────────────────
@echo off

setlocal
pushd "%~dp0"
for /f "delims=" %%I in ('wsl.exe wslpath -a "%CD%"') do set "WSL_PROJECT=%%I"

if not defined WSL_PROJECT (
	echo Error: WSL is required because Windows Application Control blocks the bundled sdcpp.exe.
	popd
	exit /b 1
)

wsl.exe sh -lc "cd '%WSL_PROJECT%' && ./build.sh %*"
set "BUILD_RESULT=%ERRORLEVEL%"
popd
exit /b %BUILD_RESULT%