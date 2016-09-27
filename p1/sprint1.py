import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies

options = ["Title","Time", "Year"]

class MyWindow(Gtk.Window): #create a new class

    def __init__(self): #creates the button
        
        #creates main window
        Gtk.Window.__init__(self, title="Hello World")
        self.set_border_width(10)

        #creates a grid
        grid = Gtk.Grid()
        #and adds the grid to the window
        self.add(grid)

        #initializes the movies list
        self.peliculas = movies.MyMovies()
        self.movieList = Gtk.ListStore(str,int,int)
        self.tree = Gtk.TreeView(self.movieList)

        #creates the tree
        self.create_tree()
        
        #adds a tree to the grid
        grid.add(self.tree)
        
        #creates the box for the buttons
        self.buttons = Gtk.VBox(spacing=20)
        
        grid.attach_next_to(self.buttons, self.tree, Gtk.PositionType.RIGHT, 1,1)
        self.create_buttons()


    def create_buttons(self):     

        self.button = Gtk.Button.new_with_label("Anadir")
        self.button.connect("clicked", self.on_anadir)		
        self.buttons.pack_start(self.button, True, True, 0)
        
        self.button = Gtk.Button.new_with_mnemonic("Borrar")
        self.button.connect("clicked", self.on_borrar)
        self.buttons.pack_start(self.button, True, True, 0)
        
        self.button = Gtk.Button.new_with_mnemonic("Editar")
        self.button.connect("clicked", self.on_editar)
        self.buttons.pack_start(self.button, True, True, 0)
    


    def create_tree(self):

        for i, column_title in enumerate(options):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, render,text=i)
            self.tree.append_column(column)
            
    def refresh_tree(self):

        self.movieList.clear()

        for pelicula in self.peliculas.getList():
            print pelicula.getData()
            self.movieList.append(list(pelicula.getData()))

    def add_to_tree(self,pelicula):
        self.movieList.append(list(pelicula.getData()))

    def on_anadir(self, button):
        print("Anadir")
        title = raw_input("title?:")
        time = input("minutes?:")
        year = input("year?:")
        pelicula = movies.Movie(title,time,year)
        for p1 in self.peliculas.getList():
            if p1.getData() == pelicula.getData():
                print "Movie Already Exists"
                return

        self.peliculas.addMovie(pelicula)
        #self.refresh_tree()
        self.add_to_tree(pelicula)

    def on_borrar(self, button):
        print("Borrar")

    def on_editar(self,button):
        print("Editar")

win = MyWindow() #creates an empty window
win.connect("delete-event", Gtk.main_quit) #se asegura de que cierre
win.show_all() #displays window
Gtk.main()

