# Moonsweeper

Explore the mysterious moon of Q'tee without getting too close to the alien natives!

Moonsweeper is a single-player puzzle video game. The objective of the game is to
explore the area around your landed space rocket, without coming too close to the
deadly B'ug aliens. Your trusty tricounter will tell you the number of B'ugs in the
vicinity.


[TIP]
.Suggested reading
====
This application makes use of features covered in <<signals>>,
<<events>> and <<custom-widgets>>.
====

.Moonsweeper.
image::app/minesweeper-playing.png[scaledwidth=50%,align="center"]


This a simple single-player exploration game modelled on _Minesweeper_
where you must reveal all the tiles without hitting hidden mines.
This implementation uses custom `QWidget` objects for the tiles, which
individually hold their state as mines, status and the
adjacent count of mines. In this version, the mines are replaced with
alien bugs (B'ug) but they could just as easily be anything else.

In many *Minesweeper* variants the initial turn is considered a free
go — if you hit a mine on the first click, it is moved somewhere else.
Here we cheat a little bit by taking the first go for the player, ensuring that
it is on a non-mine spot. This allows us not to worry about the bad first move
which would require us to recalculate the adjacencies.
We can explain this away as the "initial exploration around the rocket"
and make it sound completely sensible.

[TIP]
.Challenge
====
If you want to implement this, you can catch the first click on a
position and at that point generate mines/adjacencies,
excluding your location, before handling the click.
You will need to give your custom widgets access
to the parent window object.
====

==== Source code

The full source for the _Moonsweeper_ game is included in the downloads for this
book. The game file is saved with the name `minesweeper.py`.

{% hint style='terminal' %}
python3 minesweeper.py
{% endhint %}

==== Playing Field

The playing area for Moonsweeper is a NxN grid, containing a set number of mines.
The dimensions and mine counts we'll used are taken from the default values for
the Windows version of Minesweeper. The values used are shown in the table below:

.Table Dimensions and mine counts
|===
|Level  |Dimensions |Number of Mines

|Easy   |8 x 8      |10
|Medium |16 x 16    |40
|Hard   |24 x 24    |99
|===

We store these values as a constant `LEVELS` defined at the top of the file. Since
all the playing fields are square we only need to store the value once (8, 16 or 24).

[source,python]
----
include::code/app/minesweeper.py[tags=levels]
----

The playing grid could be represented in a number of ways, including for
example a 2D 'list of lists' representing the different states of the playing
positions (mine, revealed, flagged).

However, in our implementation we'll be using an object-orientated approach,
where individual positions on the map hold all relevant data about themselves.
Taking this a step further, we can make these objects individually responsible
for drawing themselves. In Qt we can do this simply by subclassing from `QWidget`
and then implementing a custom paint function.

We'll cover the construction and behaviour of these custom widgets before
moving onto it's appearance. Since our tile objects are subclassing from `QWidget`
we can lay them out like any other widget. We do this, by setting up a `QGridLayout`.

[source,python]
----
include::code/app/minesweeper.py[tags=grid]
----

Next we need to set up the playing field, creating our position
tile widgets and adding them our grid. The initial setup for
the level is defined in custom method, which reads from `LEVELS`
and assigns a number of variables to the window. The window title
and mine counter are updated, and then the setup of the grid is
begun.

[source,python]
----
include::code/app/minesweeper.py[tags=levelsInit]
----

The setup functions will be covered next.

We're using a custom
`Pos` class here, which we'll look at in detail later. For now you
just need to know that this holds all the relevant information
for the relevant position in the map — including, for example,
whether it's a mine, revealed, flagged and the number of mines
in the immediate vicinity.

Each `Pos` object also has 3 custom signals _clicked_, _revealed_
and _expandable_ which we connect to custom slot methods. Finally,
we call resize to adjust the size of the window to the
new contents. Note that this is actually only necessary when the
window _shrinks_ — it will grow automatically.

[source,python]
----
include::code/app/minesweeper.py[tags=initMap]
----
<1> The `singleShot` timer is required to ensure the resize runs after
Qt is aware of the new contents. By using a timer we guarantee
control will return to Qt _before_ the resize occurs.

We also need to implement the inverse of the `init_map` function to remove
tile objects from the map. Removing tiles will be necessary when moving from a
higher to a lower level. It would be possible to be a little smarter here
and adding/removing only those tiles that are necessary to get to the correct size.
But, since we already have the function to add all up to the right size,
we can cheat a bit.

[TIP]
.Challenge
====
Update this code to add/remove the neccessary tiles to size the new level dimensions.
====

Notice that we both remove the item from the grid with `self.grid.removeItem(c)` and
clear the parent `c.widget().setParent(None)`. This second step is necessary, since
adding the items assigning them the parent window as a parent. Just removing them
leaves them floating in the window outside the layout.

[source,python]
----
include::code/app/minesweeper.py[tags=clearMap]
----
<1> To ensure we clear all sizes of maps we take the dimension of the highest level.
<2> If there isn't anything in the grid at this location, we can skip it.

Now we have our grid of positional tile objects in place, we can
begin creating the initial conditions of the playing board. This
process is rather complex, so it's broken down into a number of
functions. We name them `_reset`
(the leading underscore is a convention to indicate a private function,
not intended for external use). The main function `reset_map` calls these functions
in turn to set it up.

The process is as follows —

1. Remove all mines (and reset data) from the field.
2. Add new mines to the field.
3. Calculate the number of mines adjacent to each position.
4. Add a starting marker (the rocket) and trigger initial exploration.
5. Reset the timer.

[source,python]
----
include::code/app/minesweeper.py[tags=resetMap]
----

The separate steps from 1-5 are described in detail in turn below,
with the code for each step.

The first step is to reset the data for each position on the
map. We iterate through every position on the board, calling
`.reset()` on the widget at each point. The code for the `.reset()`
function is defined on our custom `Pos` class, we'll explore in
detail later. For now it's enough to know it clears mines, flags
and sets the position back to being unrevealed.

[source,python]
----
include::code/app/minesweeper.py[tags=resetMap1]
----

Now all the positions are blank, we can begin the process of adding
mines to the map. The maximum number of mines `n_mines` is defined
by the level settings, described earlier.

[source,python]
----
include::code/app/minesweeper.py[tags=resetMap2]
----

With mines in position, we can now calculate the 'adjacency' number
for each position — simply the number of mines in the immediate vicinity,
using a 3x3 grid around the given point. The custom function `get_surrounding`
simply returns those positions around a given `x` and `y` location. We count
the number of these that is a mine `is_mine == True` and store.

[TIP]
.Pre-calculation
====
Pre-calculating the adjacent counts in this way helps simplify the
reveal logic later.
====

[source,python]
----
include::code/app/minesweeper.py[tags=resetMap3]
----

A starting marker is used to ensure that the first move is _always_
valid. This is implemented as a _brute force_ search through
the grid space, effectively trying random positions until we
find a position which is not a mine. Since we don't know how
many attempts this will take, we need to wrap it in an
continuous loop.

Once that location is found, we mark it as the start location
and then trigger the exploration of all surrounding positions.
We break out of the loop, and reset the ready status.

[source,python]
----
include::code/app/minesweeper.py[tags=resetMap4]
----

.Initial exploration around rocket.
image::app/minesweeper-start.png[scaledwidth=50%,align="center"]

==== Position Tiles

As previously described, we've structured the game so that individual
tile positions hold their own state information. This means that
`Pos` objects are ideally positioned to handle game logic which
reacts to to interactions that relate to their own state — in other
words, this is where the magic is.

Since the `Pos` class is relatively complex, it is broken down here
in to main themes, which are discussed in turn. The initial
setup `__init__` block is simple, accepting an `x` and `y` position
and storing it on the object. `Pos` positions never change once created.

To complete setup the `.reset()` function is called which resets all
object attributes back to default, zero values. This flags the mine as
_not the start position_, _not a mine_, _not revealed_ and _not flagged_.
We also reset the adjacent count.

[source,python]
----
include::code/app/minesweeper.py[tags=positions]
----

Gameplay is centered around mouse interactions with
the tiles in the playfield, so detecting and reacting
to mouse clicks is central. In Qt we catch mouse
clicks by detecting the `mouseReleaseEvent`. To do this for
our custom `Pos` widget we define a handler on the class.
This receives `QMouseEvent` with the information containing
what happened. In this case we are only interested in whether
the mouse release occurred from the left or the right mouse
button.

For a left mouse click we check whether the tile is flagged
or already revealed.
If it is either, we ignore the click — making flagged tiles 'safe',
unable to be click by accident. If the tile is not flagged
we simply initiation the `.click()` method (see later).

For a right mouse click, on tiles which are _not_ revealed, we
call our `.toggle_flag()` method to toggle a flag on and off.

[source,python]
----
include::code/app/minesweeper.py[tags=positionsEvent]
----

The methods called by the `mouseReleaseEvent` handler
are defined below.

The `.toggle_flag` handler simply sets `.is_flagged` to
the inverse of itself (`True` becomes `False`, `False` becomes
`True`) having the effect of toggling it on and off. Note
that we have to call `.update()` to force a redraw having
changed the state. We also emit our custom `.clicked` signal,
which is used to start the timer — because placing a flag should also
count as starting, not just revealing a square.

The `.click()` method handles a left mouse click, and in turn
triggers the reveal of the square. If the number of adjacent
mines to this `Pos` is zero, we trigger the `.expandable` signal
to begin the process of auto-expanding the region explored
(see later).
Finally, we again emit `.clicked` to signal the start of the game.

Finally, the `.reveal()` method checks whether the tile is
already revealed, and if not sets `.is_revealed` to `True`. Again we
call `.update()` to trigger a repaint of the widget.

The optional emit of the `.revealed` signal is used only for the
endgame full-map reveal. Because each reveal triggers a further
lookup to find what tiles are also revealable, revealing the
entire map would create a large number of redundant callbacks.
By suppressing the signal here we avoid that.

[source,python]
----
include::code/app/minesweeper.py[tags=positionsAction]
----

Finally, we define a custom `paintEvent` method for our
`Pos` widget to handle the display of the current position
state. As described in [chapter] to perform custom paint over
a widget canvas we take a `QPainter` and the `event.rect()`
which provides the boundaries in which we are to draw — in
this case the outer border of the `Pos` widget.


Revealed tiles are drawn differently depending on whether the
tile is a _start position_, _bomb_ or _empty space_. The first
two are represented by icons of a rocket and bomb respectively.
These are drawn into the tile `QRect` using `.drawPixmap`. Note
we need to convert the `QImage` constants to pixmaps, by
passing through `QPixmap` by passing.

[TIP]
.QPixmap vs. QImages
====
You might think "why not just store these as `QPixmap` objects
since that's what we're using? We can't do this and store them
in constants because you can't create `QPixmap`
objects before your `QApplication` is up and running.
====

For empty positions (not rockets, not bombs) we optionally show
the adjacency number if it is larger than zero. To draw text onto
our `QPainter` we use `.drawText()` passing in the `QRect`, alignment
flags and the number to draw as a string. We've defined a standard
color for each number (stored in `NUM_COLORS`) for usability.

For tiles that are _not_ revealed we draw a tile,
by filling  a rectangle with light gray and draw a 1 pixel border
of darker grey. If `.is_flagged` is set, we also draw a flag icon
over the top of the tile using `drawPixmap` and the tile `QRect`.

[source,python]
----
include::code/app/minesweeper.py[tags=positionsPaint]
----

==== Mechanics

We commonly need to get all tiles surrounding a given point, so we have a custom
function for that purpose. It simple iterates across a 3x3 grid around the point,
with a check to ensure we do not go out of bounds on the grid edges
(`0 ≥ x ≤ self.b_size`). The returned list contains a `Pos` widget from each
surrounding location.

[source,python]
----
include::code/app/minesweeper.py[tags=surrounding]
----

The `expand_reveal` method is triggered in response to a click on a tile
with zero adjacent mines. In this case we want to expand the area around the
click to any spaces which also have zero adjacent mines, and also reveal
any squares around the border of that expanded area (which aren't mines).

This _can_ be achieved by looking at all squares around the clicked square,
and triggering a `.click()` on any that do not have `.n_adjacent == 0`. The
normal game logic takes over and expands the area automatically. However, this
is a bit inefficient, resulting in a large number of redundant signals
(each square triggers up to 9 signals for each surrounding square).

Instead we use a self-contained method to determine the area to be revealed,
and then trigger the reveal (using `.reveal()` to avoid the `.clicked` signals.

We start with a list `to_expand` containing the positions to check on the
next iteration, a list `to_reveal` containing the tile widgets to reveal,
and a flag `any_added` to determine when to exit the loop. The loop
stops the first time no new widgets are added to `to_reveal`.

Inside the loop we reset `any_added` to `False`, and empty the `to_expand`
list, keeping a temporary store in `l` for iterating over.

For each `x` and `y` location we get the 8 surrounding widgets. If any of
these widgets is not a mine, and is not already in the `to_reveal` list
we add it. This ensures that the edges of the expanded area are all revealed.
If the position has no adjacent mines, we append the coordinates onto `to_expand`
to be checked on the next iteration.

By adding any non-mine tiles to `to_reveal`, and only expanding
tiles that are not already in `to_reveal`, we ensure that we won't
visit a tile more than once.

[source,python]
----
include::code/app/minesweeper.py[tags=expandReveal]
----

==== Endgames

Endgame states are detected during the reveal process following
a click on a title. There are two possible outcomes — 

1. Tile is a mine, game over.
2. Tile is not a mine, decrement the `self.end_game_n`.

This continues until `self.end_game_n` reaches zero, which
triggers the win game process by calling either `game_over`
or `game_won`. Success/failure is triggered
by revealing the map and setting the relevant status, in
both cases.

[source,python]
----
include::code/app/minesweeper.py[tags=endGame]
----

.Oh no. Eaten by a B'ug.
image::app/minesweeper-lose.png[scaledwidth=50%,align="center"]


==== Status

The user interface for Moonsweeper is pretty simple: one display
showing the number of mines, one showing the amount of time elapsed,
and a button to start/restart the game.

Both the labels are defined as `QLabel` objects with the
with the same `QFont` size and color. These are defined on the `QMainWindow`
object so we can access and update them at a later time. Two additional
icons (a clock and a mine) are also defined as `QLabel` objects.

The button is a `QPushButton` with a defined icon, which is updated in
`set_status` in response to status changes. The `.pressed` signal is
connected to a custom slot method `button_pressed` which handles
the signal differently depending on the game state.

[source,python]
----
include::code/app/minesweeper.py[tags=status]
----

If the game is currently in progress `self.status == STATUS_PLAYING`
a button press is interpreted as "I give up" and the the game_over
state is triggered.

If the game is currently won `self.status == STATUS_SUCCESS`
or lost `self.status == STATUS_FAILED` the press is taken to mean
 "Try again" and the game map is reset.

[source,python]
----
include::code/app/minesweeper.py[tags=statusButton]
----

==== Menus

There is only a single menu for Moonsweeper which holds the
game controls. We create a `QMenu` by calling `.addMenu()` on
the `QMainWindow.menuBar()` as normal.

The first menu item is a standard `QAction` for "New game"
wit the `.triggered` action connected to the `.reset_map` function,
which performs the entire map setup process. For new games we
keep the existing board size & layout so do not need to re-init the map.

In addition we add a submenu "Levels" which contains a `QAction` for
each level defined in `LEVELS`. The level name is taken from the same
constant, and custom status message is built from the stored dimensions.
We connect the action `.triggered` signal to `.set_level`, using the
`lambda` method to discard the default signal data and instead pass
along the level number.

[source,python]
----
include::code/app/minesweeper.py[tags=menuGame]
----

==== Going further

Take a look through the rest of the source code we've not covered.

[TIP]
.Challenges
====
You might like to try make the following changes —

* Try changing the graphics to make you're own themed version of Minesweeper.
* Add support for non-square playing fields. Rectangular? Try a circle!
* Change the timer to count down — explore the Moon against the clock!
* Add power-ups: squares give bonuses, extra time, invincibility.
====
