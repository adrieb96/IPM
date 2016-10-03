#import PyGtk
import gtk

class Dialog:

    def rundialog(self,widget,data=None):
        self.dia.show_all()
        result = self.dia.run()
        self.dia.hide()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)

        self.dia = gtk.Dialog('Test Dialog', self.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.dia.vbox.pack_start(gtk.Label('test'))

        self.button = gtk.button("Run dialog")
        self.button.connect("clicked",self.rundialog, None)
        self.window.add(self.button)
        self.button.show()
        self.window.show()

win = Dialog()
gtk.main
