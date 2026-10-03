@echo off
cd /d "%~dp0.."
echo Test: VFS with several files
call run.bat --vfs-path vfs_examples\several_files.xml