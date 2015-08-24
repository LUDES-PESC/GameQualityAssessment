GameQualityAssessment 
=====================

The code_pac folder contains python 2.7 code files, including executables to launch graphical user interfaces that allow data viewing.

The main application folder must be in PYTHONPATH to launch the GUI files.

Additional Python modules:
---------
In order to run the program, one need some additional Python modules:

+ ConfigParser
+ wxPython

Ubuntu:
---------
Within code_pac folder

PYTHONPATH=$(dirname \`pwd\`) python groupViewGui.py

OR

PYTHONPATH=$(dirname \`pwd\`) python DesafioGameGui.py
