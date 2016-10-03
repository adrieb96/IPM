import gi #import gi and force it to acces gtk+3
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import mainWindow, entry

win = mainWindow.MyWindow() #creates an empty window
win.connect("delete-event", Gtk.main_quit) #se asegura de que cierre
win.show_all() #displays window
Gtk.main()

