import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window): #create a new class

	def __init__(self): #creates the button
		Gtk.Window.__init__(self, title="Hello World")
		self.set_border_width(10)

		hbox = Gtk.Box(spacing=2)
		self.add(hbox)

                hboxList = Gtk.Box(spacing=6)
                hbox.add(hboxList)
	
                hboxButton = Gtk.VBox(spacing=20)
                hbox.add(hboxButton)

		button = Gtk.Button.new_with_label("Anadir")
		button.connect("clicked", self.on_anadir)		
		hboxButton.pack_start(button, True, True, 0)

		button = Gtk.Button.new_with_mnemonic("Borrar")
		button.connect("clicked", self.on_borrar)
		hboxButton.pack_start(button, True, True, 0)

                button = Gtk.Button.new_with_mnemonic("Editar")
                button.connect("clicked", self.on_editar)
                hboxButton.pack_start(button, True, True, 0)

	def on_anadir(self, button): #define what do when clicked
		print("Anadir")
	
	def on_borrar(self, button):
		print("Borrar")
        
        def on_editar(self,button):
                print("Editar")

win = MyWindow() #creates an empty window
win.connect("delete-event", Gtk.main_quit) #se asegura de que cierre
win.show_all() #displays window
Gtk.main()

