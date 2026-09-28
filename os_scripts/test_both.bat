@echo off
cd /d "%~dp0.."
echo Test: --vfs-path and --script together
call run.bat --vfs-path vfs\my_vfs.xml --script startup_scripts\demo.txt