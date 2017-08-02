# Getting Started

Before you start coding you will first need to have a working installation of 
PyQt and Qt on your system. The following sections will guide you through this
process for the main available platforms. If you already have a working installation
of PyQt on your Python system you can safely skip this part and get straight
onto the fun.


> #### warning::GPL Only
>
> Note that the following instructions are ***only*** for installation of the GPL
> licensed version of PyQt. If you need to use PyQt in a non-GPL project you will
> need to purchase an alternative license from [Riverbank Computing](https://www.riverbankcomputing.com) in order to release your software.


## Installation Windows

PyQt5 for Windows can be installed as for any other application or library. The only
slight complication is that you must first determine whether your system supports
32bit or 64bit software. You can determine whether your system supports 32bit or 64bit 
by looking at the System panel accessible from the control panel.

![The Windows system panel, where you can find out if you're running 64 or 32bit.](images/windows-system-panel.png)

If your system *does* support 64bit (and most modern systems do) then you 
should also check whether your current Python install is 32 or 64 bit. Open a command
prompt (Start > `cmd`):

    C:\> python3
    
Look at the top line of the Python output, where you should be able to see whether
you have 32bit or 64bit Python installed. If you want to switch to 32bit or 64bit 
Python you should do so at this point.

## PyQt5 for Python 3

A PyQt5 installer for Windows is available direct from the developer [Riverbank Computing](https://www.riverbankcomputing.com/software/pyqt/download5). Download the `.exe` files from the linked page, making sure you download the currently 64bit or 32bit version for your
systme. You can install this file as for any other Windows application/library.

After install is finished, you should be able to run `python` and `import PyQt5`.

> #### info::Documentation?
>
> The PyQt packages from Riverbank do not include the Qt documentation. However this
> is available online at [docs.qt.io](http://docs.qt.io). If you *do* want to 
> download the documentation you can do so from [www.qt.io](http://www.qt.io).


## PyQt5 for Python 2.7

Unfortunately, if you want to use PyQt5 on Python 2.7 there are no official installers
available to do this. This part of a policy by Riverbank Computing to encourage
transition to Python 3 and reduce their support burden.

However, there is nothing technically stopping PyQt5 being compiled for Python 2.7 and
the helpful group at [Abstract Factory](http://abstractfactory.io) have 
[done exactly that](http://blog.abstractfactory.io/pyqt5-1-1-for-python-2-7/).

Simply download the above `.rar` file and unpack it with 7zip (or other unzip application).
You can then copy the resulting folder to your Python site-packages folder — usually
in `C:\Python27\lib\site-packages\`.

Once that is done, you should be able to run `python` and `import PyQt5`.

## Installation Mac

OS X comes with a pre-installed version of Python (2.7), however attempting to 
install PyQt5 into this is more trouble than it is worth. If you are planning to 
do a lot of Python development, and you should, it will be easier in the long
run to create a distinct installation of Python separate from the system.

By far the simplest way to do this is to use [Homebrew](http://brew.sh/). Homebrew
is a package manager for command-line software on MacOS X. Helpfully Homebrew also
has a pre-built version of PyQt5 in their repositories.

![Homebrew — the missing package manager for OS X](images/homebrew.png)

To install homebrew run the following from the command line:

    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

T> This is also available to copy and paste from the Homebrew homepage.

Once the Homebrew installation has completed, you can then install Python 3 and PyQt5 
as follows:

    brew install python3
    brew install pyqt5 --with-python-3
    
After that has completed, you should be able to run `python3` and `import PyQt5`.    

## Installation Linux (Ubuntu)

Installation on Linux is very straightforward as packages for PyQt5 are available in
the repositories of most distributions. In Ubuntu you can install either from
the command line or via "Software Center". The packages you are looking for are
named `python3-pyqt5` or `python-pyqt5` depending on which version you are installing for.

You can also install these from the command line as follows:

    apt-get install python3-pyqt5
    
Or for Python 2.7:

    apt-get install python-pyqt5

Once the installtion is finished, you should be able to run `python3` or `python` and `import PyQt5`.    
    
    
    

    
    