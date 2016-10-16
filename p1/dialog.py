import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies
import gettext,locale

class WRecommendations(Gtk.Window):

    def __init__(self,tree,films):
        
        self.tree = tree
        self.films = films

        Gtk.Window.__init__(self,title=_("title"))
        self.set_border_width(5)

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(4)
        grid.set_column_spacing(5)
        self.add(grid)
        self.movies = []

        title = Gtk.Label()
        title.set_markup("<b>"+_("Reommendations")+":</b>\n"+_("Select movies to add"))
        title.set_justify(Gtk.Justification.LEFT)
        grid.attach(title,0,0,2,2)

        i=2
        for film in self.films:
            button = Gtk.CheckButton(film)
            grid.attach(button,0,i,3,1)
            button.connect("toggled",self.on_toggled,film)
            i+=1

        button1 = Gtk.Button.new_with_label(_("Add"))
        button2 = Gtk.Button.new_with_label(_("Exit"))
        button3 = Gtk.Button.new_with_label(_("Add All"))

        button1.connect("clicked", self.on_add)
        button2.connect("clicked", self.on_exit)
        button3.connect("clicked", self.on_add_all)

        grid.attach(button1,0,i,1,1)
        grid.attach(button3,1,i,1,1)
        grid.attach(button2,2,i,1,1)

        self.connect("key-press-event", self.on_pressed_key)

    def on_pressed_key(self,widget,event): 
        if event.keyval == 65293:
            self.add_movies(self.movies)

        elif event.keyval == 65307:
            self.destroy()

                
    def on_toggled(self,widget,movie=None):
        if widget.get_active():
            self.movies.append(movie)
        else:
            self.movies.remove(movie)

    def on_add(self,button):
        self.add_movies(self.movies)


    def on_add_all(self,button):
        self.add_movies(self.films)


    def add_movies(self,movies):
        for item in movies:
            movie = movies.Movie(item)
            self.tree.peliculas.addMovie(movie)
        self.tree.refresh_tree(1)
        self.destroy()


    def on_exit(self,button):
        self.destroy()


class Dialog(object):

    def __init__(self, father):
        
        self.father = father

    def error(self):
        #Creates a dialog widget showing the erro
        #(Only movie repeated error)
        dialog = Gtk.MessageDialog(self.father, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, _("Error with Movie"))
        dialog.format_secondary_text(_("Movie already exists"))
        dialog.run()
        dialog.destroy()
        

    def no_connection(self,err):

        dialog = Gtk.MessageDialog(self.father, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, _("Connection Error"))
        if err == -1:
            dialog.format_secondary_text(_("Timeout Exceeded"))
        if err == 0:
            dialog.format_secondary_text(_("Couldn't connect to the DataBase"))

        dialog.run()
        dialog.destroy()

    def no_films(self):

        def getDefault():
            return open(".default").readlines()

        dialog = Gtk.MessageDialog(self.father, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, _("You have no Movies"))
        text = _("We have some recommendations to get you started:")+'\n'

        recommended = getDefault()
        
        for film in recommended:
            if film is None:
                break
            text += "-"+film

        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

    
    def no_seen_movies(self):

        dialog = Gtk.MessageDialog(self.father, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, _("You have seen no Movies"))
        
        dialog.format_secondary_text(_("Mark your movies as seen to get recommendations"))
        dialog.run()
        dialog.destroy()
    
    def recommendations(self,films):

        if len(films)<1:
            dialog = Gtk.MessageDialog(self.father, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, _("No Recomendations Found"))
            dialog.format_secondary_text(_("Couldnt found recommendations for your movies"))
            dialog.run()
            dialog.destroy()
            return

        window = WRecommendations(self.father.tree,films)
        window.show_all()

        """
        dialog = Gtk.MessageDialog(self.father,0,Gtk.MessageType.INFO, Gtk.ButtonsType.OK,_("Recommendations based on your movies"))
        text=""
        for film in msg:
            text += film+"\n"

        if len(text)<1:
            text = _("No recommendations found")
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()
        """

    """
    def validated(self,title,mode):

        msg = {1:_("Movie Exists"), 2:_("Movie doesnt Exist")}
        dialog = Gtk.MessageDialog(self.father,0,Gtk.MessageType.INFO, Gtk.ButtonsType.OK, msg[mode])
        dialog.format_secondary_text(title[0])
        dialog.run()
        dialog.destroy()

    def validation(self,films):

        dialog = Gtk.MessageDialog(self.father,0,Gtk.MessageType.INFO, Gtk.ButtonsType.OK, _("Your movie was not found"))
        text="We have some similar titles\n"

        for film in films:
            text += film[0]+'\n'

        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

    """
