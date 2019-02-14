import setuptools, os, codecs, re
from distutils.command.install import install as _install

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def _post_install():
    from post_setup import main
    main()


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post install task")


with open("ReadMe.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="castervoice",
    version=find_version("castervoice/lib", "version.py"),
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
        "dragonfly2>=0.11.1",
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
    },

    cmdclass={'install': install
              },
)
