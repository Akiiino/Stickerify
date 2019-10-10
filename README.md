# Stickerify
![PyPI](https://img.shields.io/pypi/v/stickerify)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/stickerify)

Make stickers out of your Telegram messages!

# Installation
You can install from PyPI:
```
pip install --user stickerify
```
or from source:
```
python setup.py install --user
```

## Usage
First you have to make screenshots and put them into a folder. 
See examples in [examples](examples) folder.
Then you can run the program with optional output directory:
```
stickerify input_directory --out output_directory
```
You will see you screenshots. Click on messages you want to save. 
When you click on first message, a contour around all messages will appear.
To proceed to other image or close the program click on space outside of messages.

## Common problems:
If your shell can not find stickerify you might need to add `~/.local/bin` 
to your PATH environment variable: 
```
export PATH=$PATH:~/.local/bin
```
or even add it to your .bashrc: 
```
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
```
---
If you want to use stickerify in virtualenv on MacOS you *might* need to uninstall python, 
install tkinter via `brew install tcl-tk` and install python back.
