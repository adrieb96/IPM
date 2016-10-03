import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies

class WEntry(Gtk.Window):

    def __init__(self,add):

        self.add_movie = add

        Gtk.Window.__init__(self, title="title")
        self.set_size_request(200,50)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text("title...")
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)

        bbox = Gtk.Box(spacing=0)
        vbox.add(bbox)

        self.button = Gtk.Button.new_with_label("Ok")
        self.button.connect("clicked", self.on_ok)
        bbox.pack_start(self.button, True, True, 0)

    def on_ok(self, button):
        new = self.entry.get_text()
        self.add_movie(new)
        

class Buttons(object):

    def __init__(self,add,delete,edit):

        self.ask_movie = add
        self.delete_movie = delete
        self.edit_movie = edit
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
        self.ask_movie()

    def on_delete(self,button):
        self.delete_movie()

    def on_edit(self,button):
        self.edit_movie()


class TreeList(object):

    def __init__(self):
        
        self.peliculas = movies.MyMovies()
        self.movieList = Gtk.ListStore(str)
        self.treeList = Gtk.TreeView(self.movieList)

        self.create_tree()
        
    def create_tree(self):

        options = ["Title"]
        for i, title in enumerate(options):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, render, text=i)
            self.treeList.append_column(column)

    def refresh_tree(self):

        self.movieList.clear()

        for pelicula in self.peliculas.getList():
            self.movieList.append([pelicula.getTitle()])


        
class Engine(Gtk.Window):
    
    def __init__(self):
        
        self.wentry = None

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
        self.actions = Buttons(self.ask_movie,self.delete_movie,self.edit_movie)
        grid.attach_next_to(self.actions.buttons, self.tree.treeList, Gtk.PositionType.RIGHT,1,1)

    def ask_movie(self):

        self.wentry = WEntry(self.add_movie) 
        self.wentry.connect("delete-event", Gtk.main_quit)
        self.wentry.show_all()
        
    
    def add_movie(self,title):

        self.wentry.destroy()
        movie = movies.Movie(title)
        self.tree.peliculas.addMovie(movie)
        self.tree.refresh_tree()

    def delete_movie(self):

        selection = self.tree.treeList.get_selection()
        (model,path) = selection.get_selected()

        title = model.get_value(path,0)
        movie = self.tree.peliculas.getMovie(title)
        self.tree.peliculas.deleteMovie(movie)
        model.remove(path)
        

    def edit_movie(self):

        self.delete_movie()
        self.ask_movie()



    
        


window = Engine()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
