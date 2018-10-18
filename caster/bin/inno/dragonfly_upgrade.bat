@echo off

cd C:\
mkdir temp_dragonfly
cd temp_dragonfly



git clone --recursive https://github.com/Danesprite/dragonfly.git
cd dragonfly
python setup.py install

echo ------------------------------------------
echo         Dragonfly Upgrade Complete
echo ------------------------------------------

git submodule foreach python setup.py install


echo ------------------------------------------
echo         Dragonfly Submodules installed
echo ------------------------------------------

python -m pip install  .[sphinx]


cd C:\
rmdir /S/Q temp_dragonfly


pause