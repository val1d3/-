@echo off
cd /d "%~dp0.."
echo Test: script file does not exist
call run.bat --script no_such_script.txt