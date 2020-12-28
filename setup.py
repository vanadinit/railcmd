from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='railcmd',
    version='0.0.1',
    description='Railroad Command Shell (Python 3 Port)',
    keywords=['SRCP', 'rcsh', 'model railroad', 'railroad'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vanadinit/railcmd',
    author='Johannes Paul',
    author_email='vanadinit@quantentunnel.de',
    license='GPL',
    python_requires='>=3.6',
    packages=['railcmd'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)
