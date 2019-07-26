import setuptools
import os
import codecs
import re
import atexit
from setuptools.command.install import install
from setuptools.command.develop import develop


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
    from post_setup import runpostinstall
    runpostinstall()


class new_install(install):
    def run(self):
        atexit.register(_post_install)
        install.run(self)


class dev_install(develop):
    def run(self):
        develop.run(self)

with open("docs/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="castervoice",
    version=find_version("castervoice/lib", "version.py"),
    author="synkarius",
    author_email="dconway1985@gmail.com",
    description="Dragonfly-Based Voice Programming Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dictation-toolbox/Caster",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "dragonfly2>=0.14.1",
        "wxpython",
        "pillow",
        "toml",
        "future",
        "mock",
    ],
    cmdclass={'install': new_install,
              'develop': dev_install,
              },
)
