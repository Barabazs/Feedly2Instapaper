import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Feedly2Instapaper',
    version='0.1.2',
    packages=setuptools.find_packages(),
    package_data={
        'feedly2instapaper': ['settings.yaml'],
    },
    install_requires=['setuptools', 'instapaper', 'feedly-client', 'PyYAML'],
    url='https://github.com/Barabazs/Feedly2Instapaper',
    license='GNU GPLv3',
    author='Barabazs',
    author_email='',
    description='Feedly2Instapaper adds your "Saved for later" entries to Instapaper and removes those entries in Feedly.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
