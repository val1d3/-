@echo off
cd /d "%~dp0.."
echo Test: VFS with 3+ levels of nesting
call run.bat --vfs-path vfs_examples\deep_tree.xml