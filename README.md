# Create Simple GUI Applications with Python &amp; Qt

Welcome to *Creating Simple GUI Applications* where we will discover how
to use Python and Qt to do just that.

If you want to learn how to write GUI applications it
can be pretty tricky to get started. There are a lot of new concepts 
you need to understand to get *anything* to work. A lot of tutorials offer
nothing but screencasts, or short code snippets without any explanation
of the underlying systems and how they work together. But, like any code,
writing GUI applications requires you to learn to think about the problem
in the right way.

In this book I will give you the real useful basics that you need to get
building functional applications with the PyQt framework.  I’ll include explanations, 
diagrams, walkthroughs and code to make sure you know what you’re doing every step of 
the way. 

In no time at all you will have a fully functional Qt application - 
ready to customise as you like.

The source code for each step is included, but don't just copy and paste and move on.
You will learn much more if you experiment along the way!

So, lets get started!

## The Book

This book is formatted as a series of coding exercises and snippets to allow you 
to gradually explore and learn the details of PyQt5. However, it is not possible to give 
you a *complete* overview of the Qt system in a book of this size (it's huge, this isn't),
so you are encouraged to experiment and explore along the way.

If you find yourself thinking "I wonder if I can do *that*" the best thing you
can do is put this book down, then *go and find out!* Just keep regular backups of your 
code along the way so you always have something to come back to if you royally mess it up.

{% hint style='info' %}
Throughout this books there are also boxes like this, giving info, tips and warnings.
All of them can be safely skipped over if you are in a hurry, but reading them will
give you a deeper and more rounded knowledge of the Qt framework.
{% endhint %}

## Qt and PyQt

When you write applications using PyQt what you area *really* doing is writing
applications in Qt. The PyQt library is simply[^1] a wrapper around the
C++ Qt library, to allow it to be used in Python.

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
code used in this book are also tested and confirmed to work on Python 2.7. Any notable 
incompatiblities or gotchas will be flagged to accurately 
portray the sentiment e.g.

{% hint style='meh' %}
In Python 2.7 `map()` returns a `list`. 
{% endhint %}

If you are using Python 3 you can safely ignore their indifferent gaze.

[^1]: Not really *that* simple.
