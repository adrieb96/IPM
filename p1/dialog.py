import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies
import gettext,locale

class WHelp(Gtk.Window):

    def __init__(self):

        self.help_list = {_("Add"):_("Add your movies to the list"),
                      _("Delete"):_("Delete the movies you don't want in your list"),
                      _("Edit"):_("Change the title of your movies as many times as you want"),
                      _("Seen"):_("Mark your movie as Seen or Not Seen"),
                      _("Recommendations"):_("Get Recommendations based on your seen movies"),
                      _("Import"):_("If you have a saved list of seen movies you can import it"),
                      _("Export"):_("Export your seen movies"),
                      _("All"):_("See the full list of saved Movies"),
                      _("Seen"):_("Just see the list of seen Movies"),
                      _("Watchlist"):_("Here you can check your no seen Movies")
                     }
        
        Gtk.Window.__init__(self,title=_("User Help"))
        self.set_border_width(5)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        self.add(grid)

        title = Gtk.Label()
        title.set_markup("<big><b>"+_("User Help")+"</b></big>")

        txt = ""
        for item in self.help_list:
            txt += "<b>"+ item + "</b>: " + self.help_list[item] + '\n'

        content = Gtk.Label()
        content.set_markup(txt)

        grid.attach(title,0,0,1,1)
        grid.attach(content,0,1,3,2)

        button = Gtk.Button.new_with_label("Ok")
        button.connect("clicked", self.on_clicked)
        grid.attach(button,0,3,3,1)

    def on_clicked(self,button):
        self.destroy()


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


    def add_movies(self,films):
        for item in films:
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
            dialog.format_secondary_text(_("Couldnt find recommendations for your movies"))
            dialog.run()
            dialog.destroy()
            return

        window = WRecommendations(self.father.tree,films)
        window.show_all()


    def get_help(self):
       
        whelp = WHelp()
        whelp.show_all()

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
