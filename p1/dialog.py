import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import movies
import gettext,locale


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
            dialog.format_secondary_text(_("Timeout exceeded"))
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


    def recommendations(self,msg):

        dialog = Gtk.MessageDialog(self.father,0,Gtk.MessageType.INFO, Gtk.ButtonsType.OK,_("Recommendations based on your movies"))
        text=""
        for film in msg:
            text += film+"\n"

        if len(text)<1:
            text = _("No recommendations found")
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

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


