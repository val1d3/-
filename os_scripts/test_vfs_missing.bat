@echo off
cd /d "%~dp0.."
echo Test: VFS file does not exist
call run.bat --vfs-path vfs_examples\no_such_file.xml