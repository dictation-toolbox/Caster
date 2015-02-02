@echo off

cd C:\
mkdir temp_dragonfly
cd temp_dragonfly



git clone https://github.com/t4ngo/dragonfly.git



cd dragonfly\dragonfly
xcopy /Y/E/Q * C:\Python27\Lib\site-packages\dragonfly 

cd C:\
rmdir /S/Q temp_dragonfly

echo ------------------------------------------
echo         Dragonfly Upgrade Complete
echo ------------------------------------------

pause