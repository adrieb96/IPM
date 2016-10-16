"""""""""""""""""""""""""""""""""""""""
    
    ------IPM------ 

 Python + GTK
 
 Adrian Estevez Barreiro
 Diego Corton de Blas


"""""""""""""""""""""""""""""""""""""""
import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject
import movies
import gettext,locale
import api
import dialog

import time
import threading
GObject.threads_init()


current_locale, encoding = locale.getdefaultlocale()

locale_path = 'locale/'

try:
    language = gettext.translation('main', locale_path, languages=[current_locale])
    language.install()
except:
    _ = lambda s: s

class API_Thread(threading.Thread):

    def __init__(self,callback,job,arg):

        threading.Thread.__init__(self)
        self.callback = callback
        self.API = api.TMDB(current_locale)
        self.arg = arg
        self.job = job
        self.exit = False


    def recommendations(self):

        def get_iterations(i):
            if i<3:
                return (5,False)
            if i<4:
                return (3,False)
            if i<6: 
                return (2,False)
            else:
                return (1,i>10)
        #----------------------------------

        def approve(recs,seen):
            
            for film in seen:
                try:
                    recs.remove(film.getTitle())
                except:
                    pass
            return recs
        #----------------------------------

        rec_list = []
        
        seen = self.arg

        i = len(seen)

        if i > 0:

            (i,repeat) = get_iterations(i)
            for movie in seen:
                #If exit is activated, thread kills himself without crying
                if self.exit:
                    return None

                id_movie = self.API.get_movie_id(movie.getTitle())

                if id_movie is None:
                    pass
                else:
                    j=0
                    recs = self.API.get_recommendation(id_movie,2*i)
                    if self.exit:
                        return None

                    for movie in recs:
                        if j > i:
                            break
                        if movie in rec_list:
                            if repeat:  
                                break
                        else:    
                            rec_list.append(movie)
                            j+=1

            msg = approve(rec_list,seen)

        else:
            msg=[_("You have seen no movies")]

        return msg

    
    def run(self):

        #First it tries to connect to the db
        if not self.API.try_connection():
            answer = False
            self.job = 0
        else:
            #if the api losses connection to the db it returns an error
            if self.exit:
                answer = None
            else:    
                try:
                    if self.job == 1:
                        answer = self.recommendations()
                    elif self.job == 2:
                        pass
                except:
                    answer = []
                    self.job = -1

        #Calls the callback function and dies
        GObject.idle_add(self.callback,self.job,answer)

    #?
    def exit_thread(self):
        self.exit = True

class WEntry(Gtk.Window):

    def __init__(self,funct,title):

        self.funct = funct
    
        if title != _("Add"):
            WTitle = _("Edit")
        else:
            WTitle = title
        
        Gtk.Window.__init__(self, title=_(WTitle))
        self.set_size_request(200,50)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text(title)
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)

        self.button = Gtk.Button.new_with_label("Ok")
        self.button.connect("clicked", self.on_ok)
        hbox.pack_start(self.button, True, True, 0)

        self.button2 = Gtk.Button.new_with_label(_("Cancel"))
        self.button2.connect("clicked", self.on_cancel)
        hbox.pack_start(self.button2, True, True, 0)
        
        self.connect("key-press-event",self.on_pressed_key)
        
    def on_cancel(self, button):
        self.destroy()

    def on_pressed_key(self,widget,event):
        if event.keyval == 65293:
            self.return_value()

    def on_ok(self, button):
        self.return_value()

    def return_value(self):
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

    def __init__(self,tree,thread):

        self.tree = tree 
        self.thread = thread
        self.buttons = Gtk.Box(spacing=10)
        
        button1 = Gtk.Button(_("Import"))
        button1.connect("clicked",self.on_import)
        self.buttons.pack_start(button1,True,True,0)

        button2 = Gtk.Button(_("Export"))
        button2.connect("clicked",self.on_export)
        self.buttons.pack_start(button2,True,True,0)


    #if the files exists imports the movies inside
    def on_import(self,button):
        
        if not(self.thread is None):
            return
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

    #exports current seen movies to the file
    def on_export(self,button):
        try:
            seen = self.tree.peliculas.getSeen()
            if len(seen)<1:
                return

            f = open(".movies",'w')
            for movie in seen:
                f.write(movie.getTitle()+'\n')

        except:
            return

"""
class Validate(object):

    def __init__(self,val):

        self.validate = val
        self.button = Gtk.Box(spacing=10)

        button = Gtk.Button(_("Check Movie"))
        button.connect("clicked", self.on_validate)
        self.button.pack_start(button,True,True,0)

    def on_validate(self,button):
        self.validate()


class WValidate(Gtk.Window):

    def __init__(self,films):

        self.films = films
        Gtk.Window.__init__(self, title="Validate")
        self.set_border_width(10)
        
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)


        self.add(grid)

        txt = self.getTxt()
        label = Gtk.Label()
        label.set_markup("<b>Movies</b>")
        grid.attach(label,0,0,1,1)

        button1 = Gtk.Button("year")
        button1.connect("clicked", self.kill_box)
        grid.attach(button1,4,1,1,1)

        button2 = Gtk.Button("title")
        button2.connect("clicked", self.kill_box)
        grid.attach(button2,4,0,1,1)

        button3 = Gtk.Button("Votes")
        button3.connect("clicked", self.kill_box)
        grid.attach(button3,4,2,1,1)


    def getTxt(self):
        
        txt = ""
        for movie in self.films:
            txt += movie[0]+'\n'

        return txt

    def order_by(self,button):
        
        shorted = []
        end = 0

        for item in lista:

            pos = 0
    
    def kill_box(self,button):
        self.destroy()
"""

#The HEART of the GUI
class Engine(Gtk.Window):
    
    def __init__(self):
        
        self.wentry = None
        self.path = None
        self.model = None
        self.thread = None
        self.mode = 1 #It starts on mode 1, so you can see all movies
        self.connection = True
        self.API = api.TMDB(current_locale)
        self.dialog = dialog.Dialog(self)

        #creates main window
        Gtk.Window.__init__(self, title="Er Videoclu")
        self.set_border_width(10)

        #creates grid
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(6)
        self.grid.set_column_spacing(10)
        self.add(self.grid)

        #creates the tree and adds it to the grid
        self.tree = TreeList()
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 3, 8)
        self.scrollable_treelist.add(self.tree.treeList)

        #creates the buttons and add them to the grid
        self.actions = Buttons(self.ask_movie,self.delete_movie,self.seen_movie,self.recommendations)
        self.grid.attach(self.actions.buttons,3,0,2,5)
        
        #creates the combo box
        self.combo = OptionsBox(self.setMode)
        self.grid.attach(self.combo.box,0,8,1,1)

        #creates the Files buttons
        self.files = Files(self.tree,self.thread)
        self.grid.attach(self.files.buttons,3,8,2,1)

        #creates the validate button
        #self.validate = Validate(self.validate_movie)
        #grid.attach(self.validate.button,1,8,2,1)
    
        self.spinner = Gtk.Spinner()
        self.grid.attach(self.spinner,3,5,1,1)

        self.cancel_button = Gtk.Button.new_with_label(_("Cancel"))
        self.cancel_button.connect("clicked", self.on_cancel)
        #creates a label on the bottom right corner
        #label = Gtk.Label("\n  Adrian & Corton")
        #grid.attach(label,4,8,1,1)
        
    
    def exit(self,widget,event):

        #Exits the main program, killing all living threads
        if self.thread is None:
            Gtk.main_quit()
        else:
            self.thread.exit_thread() 
            Gtk.main_quit()


    def setMode(self,mode):
        self.mode=mode
        self.tree.refresh_tree(self.mode)


    #Starts the spinner and calls the api thread
    def start_spinner(self,mode,arg):

        self.spinner.start()
        self.grid.attach(self.cancel_button,4,5,1,1)
        self.cancel_button.show()
        self.thread = API_Thread(self.stop_spinner,mode,arg)
        self.thread.start()
 
    def on_cancel(self,button):
        if self.thread is None:
            return
        self.thread.exit_thread()

    #Stops the spinner and handles the answer 
    def stop_spinner(self,mode,answer):

        self.spinner.stop()
        self.grid.remove(self.cancel_button)
        self.thread = None

        if answer is None:
            return

        if mode < 1:
            self.dialog.no_connection(mode)

        elif mode == 1:
            self.dialog.recommendations(answer)


    def ask_movie(self,mode):

        if mode == 1: #add movie
            self.wentry = WEntry(self.add_movie,_("Add")) 

        else: #edit movie
            if not (self.thread is None):
                return

            self.select()
        
            if self.path is None:
                return

            title = self.model.get_value(self.path,0)
            self.wentry = WEntry(self.edit_movie,title)

        self.wentry.show_all()


    def add_movie(self,title):
 
        #destroys entry window, checks if title is empty and adds it to the list
        self.wentry.destroy()
        if title.isspace() or len(title) < 1 or title == _("Add"):
            return

        movie = movies.Movie(title)

        if self.tree.peliculas.addMovie(movie):
            self.tree.refresh_tree(self.mode)
        else:
            self.dialog.error()


    def delete_movie(self):

        if not (self.thread is None):
            return

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
            self.dialog.error()


    def seen_movie(self):

        if not (self.thread is None):
            return

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
           

    def recommendations(self):

        if not (self.thread is None):
            return

        if self.tree.peliculas.getLength() < 1:
            self.dialog.no_films()
        else:
            seen = self.tree.peliculas.getSeen()
            if len(seen)<1:
                self.dialog.no_seen_movies()
                return

            self.start_spinner(1,seen)

    """
    def validate_movie(self):

        if not (self.thread is None):
            return

        self.select()

        if self.path is None:
            return

        if not self.API.try_connection():
            self.dialog.no_connection()
            return
            

        title = self.model.get_value(self.path,0)
        titles = self.API.get_similar_title(title)
        if title in titles:
            self.dialog.validated(title)
        else:
            self.wvalidate = WValidate(titles)
            self.wvalidate.show_all()
            self.dialog.validation(titles)
    """
            
def on_pressed_key(widget,event):
    if event.keyval == 65470:
        print "DISPLAY HELP!!"

#------------------------------------MAIN------------------------------------ 
#Creates Engine and start the application

window = Engine()
window.connect("delete-event", window.exit)
window.connect("key-press-event", on_pressed_key)
window.show_all()
Gtk.main()
