import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies

options = ["Title"]

def askTitle():
    while True:
        title = entry.get_entry()
        if len(title)<1:
            print "No valid name"
        else:
            return title

class MyWindow(Gtk.Window): #create a new class

    def __init__(self): #creates the button
        
        #creates main window
        Gtk.Window.__init__(self, title="Er Videoclu")
        self.set_border_width(10)

        #creates a grid
        grid = Gtk.Grid()
        #and adds the grid to the window
        self.add(grid)

        #initializes the movies list
        self.peliculas = movies.MyMovies()
        self.movieList = Gtk.ListStore(str)
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
   
    #Empty tree
    def create_tree(self):

        for i, column_title in enumerate(options):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, render,text=i)
            self.tree.append_column(column)
            
    #Refresh the tree with the movies list
    def refresh_tree(self):

        self.movieList.clear()

        for pelicula in self.peliculas.getList():
            self.movieList.append([pelicula.getTitle()])


    #Adds the given movie to the movies list and tree
    def on_anadir(self, button):

        pelicula = movies.Movie(askTitle())
        if self.peliculas.addMovie(pelicula):
            self.refresh_tree()
            print "Movie added"
        else:
            print "Movie already exists"

    #Deletes the selected movie from both the tree and the movies list
    def on_borrar(self, button):
        print("Borrar")
        selection = self.tree.get_selection()
        (model, path) = selection.get_selected()
        if path is None:
                print "No item selected"
        else:           
            titulo = model.get_value(path,0) 
            pelicula = self.peliculas.getMovie(titulo)
            self.peliculas.deleteMovie(pelicula)
            model.remove(path)


    #Edits everything from a movie
    def on_editar(self,button):
        print("Editar")
        selection = self.tree.get_selection()
        (model,path) = selection.get_selected()
        if path is None:
            print "No item selected"
        else:
            titulo = model.get_value(path,0)
            pelicula = self.peliculas.getMovie(titulo)
            pelicula2 = movies.Movie(askTitle())
            self.peliculas.updateMovie(pelicula,pelicula2)
            self.refresh_tree()

