from setuptools import setup,find_packages
with open("README.md","r") as rm:
    long_d=rm.read()
with open("LICENSE.md","r") as lc:
    _license=lc.read()
setup(
    name="caster",
    version="0.5.10",
    author="synkarius",
    packages=find_packages(exclude=("user",)),
    long_description=long_d,
    license=_license,
    url= "https://github.com/synkarius/caster",
    install_requires=[
        "pywin32;platform_system=='Windows'",
        

        "Pillow",
    ],
    dependency_links=[
        "git+ssh://git@github.com/Danesprite/dragonfly.git#egg=dragonfly",
    ]

)