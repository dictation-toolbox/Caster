@echo off

cd C:\NatLink\NatLink\MacroSystem

@echo on

git clone https://github.com/synkarius/dragonfly-sorcery.git

@echo off

cd C:\NatLink\NatLink\MacroSystem\dragonfly-sorcery

mv * ../
mv .git ../
mv .gitignore ../

cd C:\NatLink\NatLink\MacroSystem
rmdir dragonfly-sorcery

echo ------------------------------------------
echo Dragonfly Sorcery installation complete...
echo ------------------------------------------

pause