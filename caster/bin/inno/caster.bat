@echo off

cd C:\NatLink\NatLink\MacroSystem

@echo on

git clone https://github.com/synkarius/caster.git

@echo off

cd C:\NatLink\NatLink\MacroSystem\caster

mv * ../
mv .git ../
mv .gitignore ../

cd C:\NatLink\NatLink\MacroSystem
rmdir caster

echo ------------------------------------------
echo      Caster Installation Complete
echo ------------------------------------------

pause