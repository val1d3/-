@echo off
cd /d "%~dp0.."
echo Test: minimal VFS
call run.bat --vfs-path vfs_examples\minimal.xml