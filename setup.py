import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='stickerify',
    version='1.0.1',
    url='https://github.com/Akiiino/Stickerify.git',
    author='Akiiino',
    author_email='akiiino@akiiino.me',
    description='Telegram stickers from screenshots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1, < 3.1',
                      'pillow >= 6.0.0', 'scipy >= 1.0.0',
                      'scikit-image >= 0.10.0'],
    py_modules=['stickerify'],
    entry_points={
        'console_scripts': ['stickerify=stickerify.stickerify:main'],
    },
)
