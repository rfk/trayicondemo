
Tray Icon Daemon Demo
=====================

This is a small demo app, showing how to build and deploy a desktop daemon
with tray icon across Windows, MacOSX and Linux machines.  It uses:

 * PySide and Qt4 for the GUI and System Tray integration
 * myppy for building the dependencies in a portable fashion
 * esky, along with py2exe, py2app and cxfreeze for freezing the application


Instructions for Windows
------------------------

 1) Install PySide using the pre-compiled binary packages
 2) Install myppy and esky from github master branch
 3) Run "python trayicon.py" to check that it works
 4) Run "python setup.py bdist_esky" to build the application bundle


Instructions for MacOSX
-----------------------

 1) Install myppy from github master
 2) Run "myppy PortablePython init" to initialize a portable python build
 3) Run "myppy PortablePython install py_pyside py_py2app" to get deps
 4) Run "myppy PortablePython shell" to get a shell using that python
 5)     Run "pip install esky" to install esky dependency
 6)     Run "python setup.py bdist_esky" to build the application bundle


Instructions for Linux
----------------------

 1) Ensure you're on an LSB-compatible system capable of building 32-bit.
 2) Install myppy from github master
 3) Run "myppy PortablePython init" to initialize a portable python build
 4) Run "myppy PortablePython install py_pyside py_cxfreeze" to get deps
 5) Run "myppy PortablePython shell" to get a shell using that python
 6)     Run "pip install esky" to install esky dependency
 7)     Run "python setup.py bdist_esky" to build the application bundle
  
