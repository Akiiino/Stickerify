from setuptools import setup, find_packages

setup(
    name='stickerify',
    version='1.0.0',
    url='https://github.com/Akiiino/Stickerify.git',
    author='Akiiino',
    author_email='akiiino@akiiino.me',
    description='Telegram stickers from screenshots',
    packages=find_packages(),
    install_requires=['numpy >= 1.11.1', 'matplotlib >= 1.5.1',
                      'pillow >= 6.0.0', 'scipy >= 1.0.0',
                      'scikit-image >= 0.10.0'],
    py_modules=['stickerify'],
    entry_points={
        'console_scripts': ['stickerify=stickerify.stickerify:main'],
    },
)
