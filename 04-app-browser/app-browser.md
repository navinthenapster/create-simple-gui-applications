# Mozarella Ashbadger

Mozarella Ashbadger is the latest revolution in web browsing! Go back and forward!
Print! Save files! Get help! (you'll need it). Any similarity to other browsers is
entirely coincidental.

.Mozarella Ashbadger.
image::app/browser-home.png[scaledwidth=50%,align="center"]

[TIP]
.Suggested reading
====
This application makes use of features covered in <<signals>>,
<<widgets>> and <<widgets-complex>>.
====

The source code for Mozarella Ashbadger is provided in two forms, one
with tabbed browsing and one without. Adding tabs complicates
the signal handling a little bit, so the tab-less version is covered
first.

## Source code

The full source for the tab-less browser is included in the downloads for this
book. The browser code has the name `browser.py`.

{% hint style='terminal' %}
python3 browser.py
{% endhint %}

====
icon:rocket[] *Run it!* Explore the _Mozzarella Ashbadger_
interface and features before moving onto the code.
====


## The browser widget

The core of our browser is the `QWebView` which we import from `PyQt5.QWebKitWidgets`.
This provides a complete browser window, which handles the rendering of the downloaded pages.

Below is the bare-minimum of code required to use web browser widget in PyQt.

[source,python]
----
include::code/browser_skeleton.py[]
----

If you click around a bit you'll discover that the browser behaves as expected — links work
correctly, and you can interact with the pages. However, you'll also notice
things you take for granted are missing — like an URL bar, controls or any sort of
interface whatsoever. This makes it a little tricky to use.

## Navigation

To convert this bare-bones browser into something usable we add some controls, as a
series of `QActions` on a `QToolbar`. We add these definitions to the `__init__` block
of the `QMainWindow`.

[source,python]
----
include::code/app/browser.py[tags=navigation1]
----

The `QWebEngineView` includes slots for forward,
back and reload navigation, which we can connect to directly to our
action's `.triggered` signals.

We use the same `QAction` structure for the remaining controls.

[source,python]
----
include::code/app/browser.py[tags=navigation2]
----

Notice that while forward, back and reload can use built-in slots, the navigate
home button requires a custom slot function.
The slot function is defined on our `QMainWindow` class, and simply sets the
URL of the browser to the Google homepage. Note that the URL must be passed
 as a `QUrl` object.

[source,python]
----
include::code/app/browser.py[tags=navigationHome]
----

[TIP]
.Challenge
====
Try making the home navigation location configurable. You could create a
Preferences `QDialog` with an input field.
====

Any decent web browser also needs an URL bar, and some way to stop the
navigation — either when it's by mistake, or the page is taking too long.

[source,python]
----
include::code/app/browser.py[tags=navigation3]
----

As before the 'stop' functionality is available on the `QWebEngineView`,
and we can simply connect the `.triggered` signal from the stop button
to the existing slot. However, other features of the URL bar we must
handle independently.

First we add a `QLabel` to hold our SSL or non-SSL icon
to indicate whether the page is secure. Next, we add the URL bar
which is simply a `QLineEdit`. To trigger the loading of the URL
in the bar when entered (return key pressed) we connect to the
`.returnPressed` signal on the widget to drive a custom slot
function to trigger navigation to the specified URL.

[source,python]
----
include::code/app/browser.py[tags=navigationURL]
----

We also want the URL bar to update in response to page changes.
To do this we can use the `.urlChanged` and `.loadFinished`
signals from the `QWebEngineView`. We set up the connections
from the signals in the `__init__` block as follows:

[source,python]
----
include::code/app/browser.py[tags=navigationSignals]
----

Then we define the target slot functions which for these
signals. The first, to update the URL bar accepts a `QUrl`
object and determines whether this is a `http` or
`https` URL, using this to set the SSL icon.

{% hint style='danger' %}
This is a terrible way to test if a connection is 'secure'.
To be correct we should perform a certificate validation.
{% endhint %}

The `QUrl` is converted to a string and the URL bar is
updated with the value. Note that we also set the cursor
position back to the beginning of the line to prevent
the `QLineEdit` widget scrolling to the end.

[source,python]
----
include::code/app/browser.py[tags=navigationURLBar]
----

It's also a nice touch to update the title of the
application window with the title of the current page.
We can get this via `browser.page().title()` which
returns the contents of the `<title></title>` tag
in the currently loaded web page.

[source,python]
----
include::code/app/browser.py[tags=navigationTitle]
----

#### File operations

A standard File menu with `self.menuBar().addMenu("&File")`
is created assigning the `F` key as a Alt-shortcut (as normal).
Once we have the menu object, we can can assign `QAction` objects
to create the entries. We create two basic entries here, for opening
and saving HTML files (from a local disk). These both require
custom slot functions.

[source,python]
----
include::code/app/browser.py[tags=menuFile]
----

The slot function for opening a file uses the built-in
`QFileDialog.getOpenFileName()` function to create a
file-open dialog and get a name. We restrict the names by
default to files matching `\*.htm` or `*.html`.

We read the file into a variable `html` using standard
Python functions, then use `.setHtml()` to load the HTML
into the browser.

[source,python]
----
include::code/app/browser.py[tags=menuFilefnOpen]
----

Similarly to save the HTML from the current page,
we use the built-in `QFileDialog.getSaveFileName()` to
get a filename. However, this time we get the HTML
from `self.browser.page().toHtml()` and write it
to the selected filename. Again we use standard
Python functions for the file handler.

[source,python]
----
include::code/app/browser.py[tags=menuFilefnSave]
----

## Printing

We can add a print option to the File menu using the
same approach we used earlier. Again this needs a
custom slot function to perform the print action.

[source,python]
----
include::code/app/browser.py[tags=menuPrint]
----

Qt provides a complete print framework.
`QPrintPreviewDialog` to request the settings from
the user. The dialog object has a `.paintRequested`
signal, which we can connect to the print handler of
the widget we wish to print. Thankfully, the `QWebEngineView`
provides a compatible interface for us to connect to.

The `.paintRequested` signal will be triggered if
the dialog is accepted, and the page will be printed.

[source,python]
----
include::code/app/browser.py[tags=menuPrintfn]
----

==== Help

Finally, to complete the standard interface we
can add a Help menu. This is defined as before,
two two custom slot functions to handle the
display of a About dialog, and to load the
'browser page' with more information.

[source,python]
----
include::code/app/browser.py[tags=menuHelp]
----

We define two methods to be used as slots for
the Help menu signals. The first `navigate_mozzarella`
opens up a page with more information on the browser
(or in this case, this book). The second creates
and executes a custom `QDialog` class `AboutDialog` which
we will define next.

[source,python]
----
include::code/app/browser.py[tags=menuHelpfn]
----

The definition for the about dialog is given below. The
structure follows that seen earlier in the book, with
a `QDialogButtonBox` and associated signals to handle
user input, and a series of `QLabels` to display the
application information and a logo.

The only trick here is adding all the elements to
the layout, then iterate over them to set the alignment
to the center in a single loop. This saves
duplication for the individual sections.

[source,python]
----
include::code/app/browser.py[tags=aboutDialog]
----

## Tabbed Browsing

.Mozarella Ashbadger (Tabbed).
image::app/browser-tabbed-home.png[scaledwidth=50%,align="center"]


[TIP]
.Suggested reading
====
This application makes use of features covered in <<signals>>,
<<signals-more>>, <<widgets>> and <<widgets-complex>>.
====


## Source code

The full source for the tabbed browser is included in the downloads for this
book. The browser code has the name `browser_tabs.py`.

====
icon:rocket[] *Run it!* Explore the Mozzarella Ashbadger _Tabbed Edition_
before moving onto the code.
====

## Creating a `QTabWidget`

Adding a tabbed interface to our browser is simple using a
`QTabWidget`. This provides a simple container for
multiple widgets (in our case `QWebEngineView` widgets)
with a built-in tabbed interface for switching between them.

Two customisations we use here are `.setDocumentMode(True)` which
provides a Safari-like interface on Mac, and `.setTabsClosable(True)`
which allows the user to close the tabs in the application.

We also connect `QTabWidget` signals `tabBarDoubleClicked`, `currentChanged`
and `tabCloseRequested` to custom slot methods to handle these behaviours.

[source,python]
----
include::code/app/browser_tabs.py[tags=tabWidget]
----

The three slot methods accept an `i` (index) parameter which indicates
which tab the signal resulted from (in order).

We use a double-click on
an empty space in the tab bar (represented by an index of `-1` to
trigger creation of a new tab. For removing a tab, we use the index
directly to remove the widget (and so the tab), with a simple check to
ensure there are at least 2 tabs — closing the last tab would leave you unable
to open a new one.

The `current_tab_changed` handler uses a `self.tabs.currentWidget()` construct
to access the widget (`QWebEngineView` browser) of the currently active tab,
and then uses this to get the URL of the current page. This same construct is
used throughout the source for the tabbed browser, as a simple way to interact
with the current browser view.

[source,python]
----
include::code/app/browser_tabs.py[tags=tabWidgetSlots]
----

[source,python]
----
include::code/app/browser_tabs.py[tags=addNewTab]
----

## Signal & Slot changes

While the setup of the `QTabWidget` and associated signals is simple,
things get a little trickier in the browser slot methods.


Whereas before we had a single `QWebEngineView` now there are multiple
views, all with their own signals. If signals for hidden tabs are handled
things will get all mixed up. For example, the slot handling a
`loadCompleted` signal must check that the source view is in a visible tab.

We can do this using our trick for sending additional data with signals. In
the tabbed browser we're using the `lambda` style syntax to do this.

Below is an example of doing this when creating a new `QWebEngineView` in
the `add_new_tab` function.

[source,python]
----
include::code/app/browser_tabs.py[tags=addNewTabSignals]
----

As you can see, we set a `lambda` as the slot for the `urlChanged` signal,
accepting the `qurl` parameter that is sent by this signal. We add the
recently created `browser` object to pass into the `update_urlbar` function.

The result is, whenever this `urlChanged` signal fires `update_urlbar` will
receive both the new URL and the browser it came from. In the slot method
we can then check to ensure that the source of the signal matches the
currently visible browser — if not, we simply discard the signal.

[source,python]
----
include::code/app/browser_tabs.py[tags=updateURLbar]
----

## Going further

Explore the rest of the source code for the tabbed version of the browser
paying particular attention to the user of `self.tabs.currentWidget()` and
passing additional data with signals. This a good practical use case for
what you've learnt, so experiment and see if you can break/improve it in
interesting ways.

[TIP]
.Challenges
====
You might like to try adding some additional features —

* Bookmarks (or Favorites) — you could store these in a simple text file, and show them in a menu.
* Favicons — those little website icons, would look great on the tabs.
* View source code — add a menu option to see the source code for the page.
* Open in New Tab — add a right-click context menu, or keyboard shortcut, to open a link in a new tab.

====

