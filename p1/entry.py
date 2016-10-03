import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GObject

class EWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Title")
        self.set_size_request(200,100)
        
        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text("Titulo")
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing = 6)
        vbox.pack_start(hbox,True,True, 0)

        bbox = Gtk.Box(spacing=0)
        vbox.add(bbox)

        self.button = Gtk.Button.new_with_label("Ok")
        self.button.connect("clicked", self.on_ok)
        bbox.pack_start(self.button, True, True, 0)

    def on_ok(self,button):
        return self.entry.get_text()
        


def get_entry():
    win = EWindow()
    win.connect("delete-event",Gtk.main_quit)
    win.show_all()
    Gtk.main()
    
