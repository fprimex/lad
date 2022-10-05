## Lines And Dots - LAD

An Application for Explorations in Graph Theory and Networking.

## License

This program is licensed under the CC0, which is a license developed by
Creative Commons to express that this material is explicitly dedicated to the
public domain. It may be used in any way without seeking permission or
attribution.

> Creative Commons is a global nonprofit organization that enables sharing and
> reuse of creativity and knowledge through the provision of free legal tools.

Please see the
[CC0](https://creativecommons.org/share-your-work/public-domain/cc0/) page for
more information.

## Program Requirements

* Python 3.x - http://python.org
* wxPython 4.x - http://wxpython.org
* NetworkX 2.x - https://networkx.github.io/
* numpy 1.x - http://numpy.scipy.org

## Running LAD

Launch with 'python lad.py'

The main window contains menus for loading, saving, and exporting graphs
(File), manipulating the program view (View), changing the way the mouse
interacts with the canvas (Mouse Mode), and manipulating the graph
itself (Graph). Hopefully the help text for each menu item displayed in
the status bar is descriptive enough.

In Creation Mouse Mode, click the canvas to create and select vertices.
Edges can be added by selecting multiple vertices (hold down Ctrl while
clicking, Command on Mac) and using the Graph menu to either add all
possible edges or a path. Drag multiple selections around by keeping the
Ctrl (or Command) key held down.

When selecting and creating vertices the notebook (tabbed window) will
update with information. The Info page displays information about the
current selection. The Vars page (tab showing "G.vars['var']=val")
displays a Python dictionary of variables. Data in both the Vars page
and Info page can be edited by double clicking on the item.

Lastly, there is an interacitive Python shell at the bottom of the main
window. All aspects of the program can be manipulated from this shell,
including the addition of new menus and windows as well as programatic
interatction with the Graph. I don't recommend reassigning the graph,
G, or other variables right now.

Several variables have been made available at the shell by default:

```
G        - The program's central data structure, a networkx graph
canvas   - The graph drawing window
notebook - The tabbed window containing the Info and Vars pages
shell    - The shell window itself
```

The graph G has several interesting properties and methods. I recommend
visiting the networkx
[tutorial](https://networkx.org/documentation/stable/tutorial.html).

In addition to the standard attributes and methods provided by networkx,
LAD graphs come standard with the following Python dictionary attributes:

```
G.vlabel[v]  - dictionary of vertex labels
G.vpos[v]    - dictionary of vertex positions
G.vweight[v] - dictionary of vertex weights
G.vcolor[v]  - dictionary of vertex colors
G.vars       - dictionary of user defined variables
G.var_exps   - dictionary of expressions used to calculate G.var values
```

A standard 'session' I have been using to show off multiple features:

* Launch LAD
* Click to make several vertices (hold Ctrl to select while creating)
* Add a path (Ctrl+P)
* Drag things around, edit attributes using Info page
* Switch to Vars page and create more vertices and edges
* Add complete edges (Ctrl+A Ctrl+P)
* Create a new Var - right click in Vars page, select Insert Row
* Give the variable the name degree0, press tab, type G.degree(0)
* Create a new vertex / edge that connects to v0 (vertex number 0)
* In the shell:

```
>>> import networkx as nx
>>> G.vpos = nx.circular_layout(G)
>>> canvas.Refresh()
>>> for v in G.nodes():
        G.vpos[v] = 5*G.vpos[v]

>>> canvas.Refresh()
```

* Back in the main window, save the graph, export it as an image, etc
* Select all, delete (Ctrl+A, Ctrl+Backspace)

## Extending LAD

LAD has been designed from the ground up to be ultimately hackable. Python
language constructs such as method reassignment are used and encouraged.

In particular, see the GraphArtist and NotebookPage directories in the
source distribution to see how to get started either drawing graphs or
creating notebook UI elements.

For example, open a new graph and enter at the shell:

```
>>> import GraphArtist
>>> blank_artist = GraphArtist.BlankArtist()
>>> canvas.artist.DrawAxes = blank_artist.DrawAxes
>>> canvas.Refresh()
```

I would love to see people create modules to import that created new
menu entries for their own graph analysis purposes.

Future Plans
============
* Need nice application features - saving window size and position,
  creating a way to set program defaults, etc
* LAD currently only implements NetworkX Graph. It needs support for
  DiGraph, XGraph, and XDiGraph
* More Graph artists
* There are no zooming options or scrolling options on the canvas - this
  is especially a problem when loading graphs
* There are no docstrings
* Should either inherit from NetworkX graphs to provide extended
  attributes or provide a 'dectorate' method to look for attributes,
  creating defaults when needed
* There need to be menu entries that wrap NetworkX functionality like
  creating named graphs, doing layouts, and most importantly:
* NEED ALGORITHMS! shortest path, etc
