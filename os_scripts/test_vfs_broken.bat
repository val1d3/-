@echo off
cd /d "%~dp0.."
echo Test: broken VFS file (invalid format)
call run.bat --vfs-path vfs_examples\broken.xml