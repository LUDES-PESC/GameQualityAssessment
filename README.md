GameQualityAssessment 
=====================

The code_pac folder contains python 2.7 code files, including executables to launch graphical user interfaces that allow data viewing.

The main application folder must be in PYTHONPATH to launch the GUI files.

Additional Python modules:
---------
In order to run the program, one need some additional Python modules that are in the `requirements.txt` file and listed down below:

+ backports.functools-lru-cache==1.5
+ cycler==0.10.0
+ kiwisolver==1.0.1
+ matplotlib==2.2.2
+ numpy==1.14.3
+ psycopg2==2.7.4
+ pyparsing==2.2.0
+ python-dateutil==2.7.3
+ pytz==2018.4
+ six==1.11.0
+ subprocess32==3.2.7
+ wxPython==4.0.1
+ xlrd==1.1.0

To install these modules type the following command in the __root__ project folder:

```bash
pip install -r requirements.txt
```

Development libs:
----
Some libs __and its dev versions__ are required to run:

+ gtk+-3.0
+ gstreamer 1.0
+ gstreamer-plugin
+ gstreamer base


Ubuntu:
---------
Within code_pac folder

PYTHONPATH=$(dirname \`pwd\`) python groupViewGui.py

OR

PYTHONPATH=$(dirname \`pwd\`) python DesafioGameGui.py
