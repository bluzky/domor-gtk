__author__ = 'bluzky'

try:
    from gi.repository import Gtk, Gdk, GObject
except ImportError:
    import gtk as Gtk
    import gtk.gdk as Gdk
    import gobject as GObject

css = """
#fullscreen-window
{
    background-color: rgba(0,0,0,0.7);
}

#bg GtkButton
{
    background-color: white;
}

.bg-white
{
    background-color: #fff;
}
"""


def setStyle():
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
