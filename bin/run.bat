@echo off
setlocal

set "ROOT_DIR=%~dp0.."
pushd "%ROOT_DIR%" >nul

python src\main.py %*

popd >nul
endlocal
pause
