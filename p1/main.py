import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies
import gettext,locale
import api

current_locale, encoding = locale.getdefaultlocale()

locale_path = 'locale/'

try:
    language = gettext.translation('main', locale_path, languages=[current_locale])
    language.install()
except:
    _ = lambda s: s


class WEntry(Gtk.Window):

    def __init__(self,funct,title):

        self.funct = funct

        Gtk.Window.__init__(self, title=_("title"))
        self.set_size_request(200,50)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text(title)
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

    def __init__(self,add,delete,seen,rec):

        self.ask_movie = add
        self.delete_movie = delete
        self.seen_movie = seen
        self.recommendations = rec
        self.buttons = Gtk.VBox(spacing=10)
        self.create_buttons()

    def create_buttons(self):

        self.button = Gtk.Button.new_with_label(_("Add"))
        self.button.connect("clicked", self.on_add)
        self.buttons.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button.new_with_label(_("Delete"))
        self.button.connect("clicked", self.on_delete)
        self.buttons.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button.new_with_label(_("Edit"))
        self.button.connect("clicked", self.on_edit)
        self.buttons.pack_start(self.button, True, True, 0)

        self.button = Gtk.Button.new_with_label(_("Seen"))
        self.button.connect("clicked", self.on_seen)
        self.buttons.pack_start(self.button, True, True ,0)

        self.button = Gtk.Button.new_with_label(_("Recommendations"))
        self.button.connect("clicked", self.on_recommend)
        self.buttons.pack_start(self.button, True, True, 0)

    def on_add(self,button):
        self.ask_movie(1)

    def on_delete(self,button):
        self.delete_movie()

    def on_edit(self,button):
        self.ask_movie(2)
    
    def on_seen(self,button):
        self.seen_movie()

    def on_recommend(self,button):
        self.recommendations()


class TreeList(object):

    def __init__(self):
        
        self.peliculas = movies.MyMovies()
        self.movieList = Gtk.ListStore(str,str)
        self.treeList = Gtk.TreeView(self.movieList)

        self.create_tree()
        
    #creates tree skeleton with "options" columns   
    def create_tree(self):

        options = [_("Title"),_("Seen")]
        for i, title in enumerate(options):
            render = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, render, text=i)
            self.treeList.append_column(column)

    #clears and adds all movie to treeList
    def refresh_tree(self,mode):

        def seen(movie):
            if movie.getStatus():
                return _('yes')
            return _('no')

        self.movieList.clear()

        for pelicula in self.peliculas.getList():
            if mode == 1:
                self.movieList.append([pelicula.getTitle(),seen(pelicula)])
            elif mode == 2 and pelicula.getStatus():
                self.movieList.append([pelicula.getTitle(),_('yes')])
            elif mode == 3 and not pelicula.getStatus():
                self.movieList.append([pelicula.getTitle(),_('no')])


class OptionsBox(object):

    def __init__(self,setMode):

        self.setMode = setMode
        self.box = Gtk.Box(spacing=6)
        select_tree = Gtk.ListStore(str)
        options = [ _("All"),_("Seen "),_("Watchlist")]

        for option in options:
            select_tree.append([option])

        movies_combo = Gtk.ComboBox.new_with_model(select_tree)
        movies_combo.connect("changed",self.on_combo_changed)
        renderer = Gtk.CellRendererText()
        movies_combo.pack_start(renderer,True)
        movies_combo.add_attribute(renderer, "text", 0)
        self.box.pack_start(movies_combo, False, False, True)

    
    #defines what the Engine will do on each mode
    def on_combo_changed(self,combo):
        tree_iter = combo.get_active_iter()

        if tree_iter != None:
            model = combo.get_model()
            option = model[tree_iter][0]
            if option == _("All"):
                self.setMode(1)
            elif option == _("Seen "):
                self.setMode(2)
            elif option == _("Watchlist"):
                self.setMode(3)

class Files(object):

    def __init__(self,tree):

        self.tree = tree 
        self.buttons = Gtk.Box(spacing=10)
        
        button1 = Gtk.Button(_("Import"))
        button1.connect("clicked",self.on_import)
        self.buttons.pack_start(button1,True,True,0)

        button2 = Gtk.Button(_("Export"))
        button2.connect("clicked",self.on_export)
        self.buttons.pack_start(button2,True,True,0)


    def on_import(self,button):
        
        try:
            f = open(".movies")
            films = f.readlines()
            for item in films:
                movie = movies.Movie(item[:-1])
                movie.setStatus(True)
                self.tree.peliculas.addMovie(movie)

        except:
            return

        self.tree.refresh_tree(1)


    def on_export(self,button):
        try:
            f = open(".movies",'w')
            for movie in self.tree.peliculas.getList():
                f.write(movie.getTitle())
        except:
            return


#The HEART of the GUI
class Engine(Gtk.Window):
    
    def __init__(self):
        
        self.wentry = None
        self.path = None
        self.model = None
        self.mode = 1
        self.API = api.TMDB(current_locale)

        #creates main window
        Gtk.Window.__init__(self, title="Er Videoclu")
        self.set_border_width(10)

        #creates grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        self.add(grid)

        #creates the tree and adds it to the grid
        self.tree = TreeList()
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        grid.attach(self.scrollable_treelist, 0, 0, 3, 8)
        self.scrollable_treelist.add(self.tree.treeList)

        #creates the buttons and add them to the grid
        self.actions = Buttons(self.ask_movie,self.delete_movie,self.seen_movie,self.recommendations)
        grid.attach(self.actions.buttons,3,0,2,5)
        
        self.combo = OptionsBox(self.setMode)
        grid.attach(self.combo.box,0,8,2,1)

        """
        #creates a spinner that appears when loading info
        self.spinner = Gtk.Spinner()
        grid.attach_next_to(self.spinner, self.combo.box, Gtk.PositionType.RIGHT,1,1)
        self.spinner.start()
        """

        self.files = Files(self.tree)
        grid.attach(self.files.buttons,3,7,2,1)
        
    def setMode(self,mode):
        self.mode=mode
        self.tree.refresh_tree(self.mode)


    def ask_movie(self,mode):

        #add movie
        if mode == 1:
            self.wentry = WEntry(self.add_movie,"") 
        else: #edit movie
            self.select()
        
            if self.path is None:
                return

            title = self.model.get_value(self.path,0)
            self.wentry = WEntry(self.edit_movie,title)

        self.wentry.show_all()


    def add_movie(self,title):
        
        #destroys entry window, checks if title is empty and adds it to the list
        self.wentry.destroy()
        if title.isspace():
            return

        movie = movies.Movie(title)

        if self.tree.peliculas.addMovie(movie):
            self.tree.refresh_tree(self.mode)
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
            self.tree.refresh_tree(self.mode)
        else:
            self.dialog_error()


    def seen_movie(self):
        
        self.select()

        if self.path is None:
            return

        title = self.model.get_value(self.path,0)
        movie = self.tree.peliculas.getMovie(title)
        self.tree.peliculas.seenMovie(movie)
        self.tree.refresh_tree(self.mode)


    def select(self):
        #gets the "selected" item
        (self.model, self.path) = self.tree.treeList.get_selection().get_selected()
           

    def getDefault(self):
        return open("default").readlines()


    def recommendations(self):

        if self.tree.peliculas.getLength() < 1:
            self.dialog_no_films()
        else:

            if not self.API.try_connection():
                self.dialog_no_connection()
                return
            
            rec_list = []
            not_found = []

            seen = self.tree.peliculas.getSeen()
            if len(seen) > 0:
                for movie in seen:
                    id_movie = self.API.get_movie_id(movie.getTitle())
                    if id_movie is None:
                        not_found.append(movie.getTitle())
                    else: 
                        rec_list.append(id_movie)

                msg=self.API.get_recommendations(rec_list)
            else:
                msg=[_("You have seen no movies")]
            self.dialog_recommendations(msg)


    def dialog_error(self):
        #Creates a dialog widget showing the erro
        #(Only movie repeated error)
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, _("Error with Movie"))
        dialog.format_secondary_text(_("Movie already exists"))
        dialog.run()
        dialog.destroy()
        

    def dialog_no_connection(self):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, _("Connection Error"))
        dialog.format_secondary_text(_("Couldn't connect to the DataBase"))
        dialog.run()
        dialog.destroy()


    def dialog_no_films(self):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, _("You have no Movies"))
        text = _("We have some recommendations to get you started:")+'\n'
        recommended = self.getDefault()
        for film in recommended:
            if film is None:
                break
            text += "-"+film

        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

    def dialog_recommendations(self,msg):

        dialog = Gtk.MessageDialog(self,0,Gtk.MessageType.INFO, Gtk.ButtonsType.OK,_("Recommendations based on your movies"))
        text=""
        for film in msg:
            text += film+"\n"

        if len(text)<1:
            text = _("No recommendations found")
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()
        
def on_pressed_key(widget,event):
    if event.keyval == 65470:
        print "DISPLAY HELP!!"

#MAIN creates Engine
window = Engine()
window.connect("delete-event", Gtk.main_quit)
window.connect("key-press-event", on_pressed_key)
window.show_all()
Gtk.main()
