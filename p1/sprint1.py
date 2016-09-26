import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies


class MyWindow(Gtk.Window): #create a new class

    def __init__(self): #creates the button

        Gtk.Window.__init__(self, title="Hello World")
        self.set_border_width(10)

        grid = Gtk.Grid()
        self.add(grid)

        self.peliculas = movies.MyMovies()
        movieList = Gtk.ListStore(str,int,int)
        for movie in self.peliculas.getList():
            movieList.append(list(movie))                    

        tree = Gtk.TreeView(movieList)
        
        for i, column_title in enumerate(["Titulo", "Duracion", "Ano"]):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, render,text=i)
            tree.append_column(column)
        
        #scrollable_treelist = Gtk.ScrolledWindow()
        #scrollable_treelist.set_vexpand(True)
        #grid.attach(scrollable_treelist, 0, 0, 8, 10)


        grid.add(tree)
        
        buttons = Gtk.VBox(spacing=20)
        
        grid.attach_next_to(buttons, tree, Gtk.PositionType.RIGHT, 1,1)
        
        button = Gtk.Button.new_with_label("Anadir")
        button.connect("clicked", self.on_anadir)		
        buttons.pack_start(button, True, True, 0)
        
        button = Gtk.Button.new_with_mnemonic("Borrar")
        button.connect("clicked", self.on_borrar)
        buttons.pack_start(button, True, True, 0)
        
        button = Gtk.Button.new_with_mnemonic("Editar")
        button.connect("clicked", self.on_editar)
        buttons.pack_start(button, True, True, 0)

    def on_anadir(self, button):
        print("Anadir")
        title = raw_input("title?:")
        time = raw_input("minutes?:")
        year = raw_input("year?:")
        pelicula = movies.Movie(title,time,year)
        self.peliculas.addMovie(pelicula)

    def on_borrar(self, button):
        print("Borrar")

    def on_editar(self,button):
        print("Editar")

win = MyWindow() #creates an empty window
win.connect("delete-event", Gtk.main_quit) #se asegura de que cierre
win.show_all() #displays window
Gtk.main()

