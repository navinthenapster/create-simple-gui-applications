
## The Book

This book is formatted as a series of coding exercises and snippets to allow you 
to gradually explore and learn the details of PyQt5. However, it is not possible to give 
you a *complete* overview of the Qt system in a book of this size (it's huge, this isn't),
so you are encouraged to experiment and explore along the way.

If you find yourself thinking "I wonder if I can do *that*" the best thing you
can do is put this book down, then *go and find out!* Just keep regular backups of your 
code along the way so you always have something to come back to if you royally mess it up.

I> Throughout this books there are also boxes like this, giving info, tips and warnings.
I> All of them can be safely skipped over if you are in a hurry, but reading them will
I> give you a deeper and more rounded knowledge of the Qt framework.

## Qt and PyQt

When you write applications using PyQt what you area *really* doing is writing
applications in Qt. The PyQt library is simply[^pyqt-simple] a wrapper around the
C++ Qt library, to allow it to be used in Python.

[^pyqt-simple]: Not really *that* simple.

Because this is a Python interface to a C++ library the naming conventions used 
within PyQt do not adhere to PEP8 standards. Most notably functions and variables
are named using `mixedCase` rather than `snake_case`. Whether you adhere to this
standard in your own applications based on PyQt is entirely up to you, however
you may find it useful to help clarify where the PyQt code ends and your own begins.

Further, while there is PyQt specific documentation available, you will often find 
yourself reading the Qt documentation itself as it is more complete. If you do
you will need to translate object syntax and some methods containining Python-reserved function names as follows:

| Qt                                | PyQt                                  |
|-----------------------------------|---------------------------------------|
| `Qt::SomeValue`                   | `Qt.SomeValue`                        |
| `object.exec()`                   | `object.exec_()`                      |
| `object.print()`                  | `object.print_()`                     |



## Python 3

This book is written to be compatible with Python 3.4+. Python 3 is
the future of the language, and if you're starting out now is where you should
be focusing your efforts. However, in recognition of the fact that many 
people are stuck supporting or developing on legacy systems, the examples and 
code used in this book are also tested and confirmed to work on Python 2.7. Any notable incompatiblities or gotchas will be flagged with a meh-face to accurately 
portray the sentiment e.g.

{icon=meh-o}
G> #### Python 2.7
G>
G> In Python 2.7 `map()` returns a `list`. 

If you are using Python 3 you can safely ignore their indifferent gaze.
