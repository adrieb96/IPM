import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies


class WEntry(Gtk.Window):

    def __init__(self,funct):

        self.funct = funct

        Gtk.Window.__init__(self, title="title")
        self.set_size_request(200,50)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text(" ")
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)

        bbox = Gtk.Box(spacing=0)
        vbox.add(bbox)

        self.button = Gtk.Button.new_with_label("Ok")
        self.button.connect("clicked", self.on_ok)
        bbox.pack_start(self.button, True, True, 0)

        
    def on_ok(self, button):
        #gets the user input and calls the given function
        title = self.entry.get_text()
        self.funct(title)
        self.destroy()
        

class Buttons(object):

    def __init__(self,add,delete):

        self.ask_movie = add
        self.delete_movie = delete
        self.buttons = Gtk.VBox(spacing=20)
        self.create_buttons()

    def create_buttons(self):

        self.button = Gtk.Button.new_with_label("Add")
        self.button.connect("clicked", self.on_add)
        self.buttons.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button.new_with_label("Delete")
        self.button.connect("clicked", self.on_delete)
        self.buttons.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button.new_with_label("Edit")
        self.button.connect("clicked", self.on_edit)
        self.buttons.pack_start(self.button, True, True, 0)

    def on_add(self,button):
        self.ask_movie(1)

    def on_delete(self,button):
        self.delete_movie()

    def on_edit(self,button):
        self.ask_movie(2)


class TreeList(object):

    def __init__(self):
        
        self.peliculas = movies.MyMovies()
        self.movieList = Gtk.ListStore(str)
        self.treeList = Gtk.TreeView(self.movieList)

        self.create_tree()
        
    #creates tree skeleton with "options" columns   
    def create_tree(self):

        options = ["Title"]
        for i, title in enumerate(options):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, render, text=i)
            self.treeList.append_column(column)

    #clears and adds all movie to treeList
    def refresh_tree(self):

        self.movieList.clear()

        for pelicula in self.peliculas.getList():
            self.movieList.append([pelicula.getTitle()])


#The HEART of the GUI
class Engine(Gtk.Window):
    
    def __init__(self):
        
        self.wentry = None
        self.path = None
        self.model = None

        #creates main window
        Gtk.Window.__init__(self, title="Er Videoclu")
        self.set_border_width(10)

        #creates grid
        grid = Gtk.Grid()
        self.add(grid)

        #creates the tree and adds it to the grid
        self.tree = TreeList()
        grid.add(self.tree.treeList)

        #creates the buttons and add them to the grid
        self.actions = Buttons(self.ask_movie,self.delete_movie)
        grid.attach_next_to(self.actions.buttons, self.tree.treeList, Gtk.PositionType.RIGHT,1,1)

    def ask_movie(self,mode):

        #add movie
        if mode == 1:
            self.wentry = WEntry(self.add_movie) 
        else: #edit movie
            self.select()
        
            if self.path is None:
                return

        #calls an entry window to get user input
            self.wentry = WEntry(self.edit_movie)

        self.wentry.show_all()

    def add_movie(self,title):
        
        #destroys entry window, checks if title is empty and adds it to the list
        self.wentry.destroy()
        if title.isspace():
            return
        movie = movies.Movie(title)
        if self.tree.peliculas.addMovie(movie):
            self.tree.refresh_tree()
        else:
            self.dialog_error()

    def delete_movie(self):

        self.select()
        
        if self.path is None:
            return

        #deletes the selected movie
        title = self.model.get_value(self.path,0)
        movie = self.tree.peliculas.getMovie(title)
        self.tree.peliculas.deleteMovie(movie)
        self.model.remove(self.path)
        

    def edit_movie(self, new):
        self.wentry.destroy()

        title = self.model.get_value(self.path,0)

        #checks if new title is valid
        if new.isspace() or new == title:
            return
        
        newMovie = movies.Movie(new)        
        movie = self.tree.peliculas.getMovie(title)

        #if title already exists throws an error and exits without doing anything
        if self.tree.peliculas.updateMovie(movie,newMovie):
            self.tree.refresh_tree()
        else:
            self.dialog_error()

    def select(self):
        #gets the "selected" item
        (self.model, self.path) = self.tree.treeList.get_selection().get_selected()
           
    def dialog_error(self):
        #Creates a dialog widget showing the erro
        #(Only movie repeated error)
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error with Movie")
        dialog.format_secondary_text("Movie already exists")
        dialog.run()
        dialog.destroy()

    
        

#MAIN creates Engine
window = Engine()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
