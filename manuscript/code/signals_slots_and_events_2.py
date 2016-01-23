from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Only needed for access to command line arguments
import sys


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        # QHBoxLayout is a horizontally stacking layout with new widgets
        # added to the right of previous widgets.
        layout = QHBoxLayout()
        
        for n in range(10):
            # Create a push button labeled with the loop number 0-9
            btn = QPushButton(str(n))
            # SIGNAL: The .pressed signal fires whenever the button is pressed.
            # We connect this to self.my_custom_fn via a lambda to pass in
            # additional data.
            # IMPORTANT: You must pass the additional data in as a named 
            # parameter on the lambda to create a new namespace. Otherwise
            # the value of n will be bound to the final value in the parent
            # for loop (always 9).
            btn.pressed.connect( lambda n=n: self.my_custom_fn(n) )
 
            # Add the button to the layout. It will go to the right by default.
            layout.addWidget(btn)
        
        # Create a empty widget to hold the layout containing our buttons.
        widget = QWidget()
        
        # Set the layout containing our buttons onto the blank widget. We only
        # need to do this here because we can't set a layout on a QMainWindow.
        # So instead we're setting a layout on a widget, and then adding that 
        # widget to the window(!)
        widget.setLayout(layout)
        
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
        

    # SLOT: This function will receive the single value passed from the signal
    def my_custom_fn(self, a):
        print(a)
        

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

window = MainWindow()
window.show() # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()


# Your application won't reach here until you exit and the event 
# loop has stopped.






