import setuptools

with open("ReadMe.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="castervoice",
    version="0.6.10",
    author="synkarius",
    author_email="dconway1985@gmail.com",
    description="Dragonfly-Based Voice Programming Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dictation-toolbox/castervoice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "dragonfly2>=0.11.0",
        "wxpython>=4.0.3",
        "pillow>=5.3.0",
        "toml>=0.10.0",
        "future"
    ],
    package_data={
        "castervoice": [
            "bin/data/configdebug.txt",
            "bin/share/bringme.toml.defaults",
            "bin/reboot.bat",
            "bin/reboot_wsr.bat",
            "lib/dll/tirg-dll.dll",
            "asynch/sikuli/server/xmlrpc_server.sikuli/xmlrpc_server.html",
            "asynch/sikuli/server/xmlrpc_server.sikuli/xmlrpc_server.py"
        ]
    }
)
