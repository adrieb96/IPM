import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window): #create a new class

	def __init__(self): #creates the button
		Gtk.Window.__init__(self, title="Hello World")

		self.button = Gtk.Button(label="Click Here")
		self.button.connect("clicked", self.on_button_clicked)
		self.add(self.button)

	def on_button_clicked(self, widget): #define what do when clicked
		print("Hello World")

win = MyWindow() #creates an empty window
win.connect("delete-event", Gtk.main_quit) #se asegura de que cierre
win.show_all() #displays window
Gtk.main()

