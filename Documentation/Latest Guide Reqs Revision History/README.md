# ML4CyberVinciPython

This repo contains the VINCI ML Tool code and resources.
The GUI was designed using PyQt5 and Qt Designer.
TO SELECT WHIOCH VERSION OF PYTHON TO RUN WITH THE SCRIP py -3.11 script.py

# Installation

Make sure you are using Python 3.8

To install dependency packages, issue the following command:

    $ pip install -r requirements.txt

After this, you should be able to launch the App with the following command:

    $ python gui/app.py

# Creating an executable file

To generate an executable file, run the following command:

    $ cd gui
    $ pyinstaller --clean --onefile --windowed --icon=app.ico  app.py

To save executable to another folder, use --distpath:

    $ pyinstaller --clean --onefile --windowed --icon=app.ico --distpath=distUbuntu/  app.py

# Testing

We have a shared Google Doc for basic management of use case testing:

https://docs.google.com/document/d/1k2x6IXskD80r-5NXWBERk8iX_ZVzuKyThklfUNsXEsU/edit