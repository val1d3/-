@echo off
cd /d "%~dp0.."
echo Test: only --vfs-path
call run.bat --vfs-path vfs\my_vfs.xml