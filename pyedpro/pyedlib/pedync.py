#!/usr/bin/env python

# Prompt Handler for PyEdPro

import os, sys, string

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import GdkPixbuf

import pyedlib.pedconfig

# ------------------------------------------------------------------------

def yes_no_cancel(title, message, cancel = True):

    dialog = Gtk.Dialog(title,
                   None,
                   Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)

    dialog.set_default_response(Gtk.ResponseType.YES)
    dialog.set_position(Gtk.WindowPosition.CENTER)

    dialog.set_transient_for(pyedlib.pedconfig.conf.pedwin.mywin);
    
    sp = "     "
    label = Gtk.Label(message); 
    label2 = Gtk.Label(sp);      label3 = Gtk.Label(sp)
    label2a = Gtk.Label(sp);     label3a = Gtk.Label(sp)
    
    hbox = Gtk.HBox() ;     
    
    hbox.pack_start(label2, 0, 0, 0);  
    hbox.pack_start(label, 1, 1, 0);     
    hbox.pack_start(label3, 0, 0, 0)
    
    dialog.vbox.pack_start(label2a, 0, 0, 0);  
    dialog.vbox.pack_start(hbox, 0, 0, 0)
    dialog.vbox.pack_start(label3a, 0, 0, 0);  
    
    dialog.add_button("_Yes", Gtk.ResponseType.YES)
    dialog.add_button("_No", Gtk.ResponseType.NO)
    
    if cancel:
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)

    dialog.connect("key-press-event", yn_key, cancel)
    #dialog.connect("key-release-event", yn_key, cancel)
    dialog.show_all()
    response = dialog.run()       
    # Convert all responses to cancel
    if  response == Gtk.ResponseType.CANCEL or \
        response == Gtk.ResponseType.REJECT or \
        response == Gtk.ResponseType.CLOSE  or \
        response == Gtk.ResponseType.DELETE_EVENT:
        response = Gtk.ResponseType.CANCEL        
    dialog.destroy()
    return  response 

def yn_key(win, event, cancel):
    #print event
    if event.keyval == Gdk.KEY_y or \
        event.keyval == Gdk.KEY_Y:
        win.response(Gtk.ResponseType.YES)
        
    if event.keyval == Gdk.KEY_n or \
        event.keyval == Gdk.KEY_N:
        win.response(Gtk.ResponseType.NO)

    if cancel:
        if event.keyval == Gdk.KEY_c or \
            event.keyval == Gdk.KEY_C:
            win.response(Gtk.ResponseType.CANCEL)

# ------------------------------------------------------------------------
# Show About dialog:

import platform

def  about(self2):
    dialog = Gtk.AboutDialog()
    #dialog.set_parent(None)
    dialog.set_name(" PyEdPro - Python Editor ")
    dialog.set_version(str(pyedlib.pedconfig.conf.version));
    gver = (Gtk.get_major_version(), \
                        Gtk.get_minor_version(), \
                            Gtk.get_micro_version())
    
    dialog.set_position(Gtk.WindowPosition.CENTER)
    
    dialog.set_transient_for(self2.mywin)
    
    #"\nRunning PyGObject %d.%d.%d" % GObject.pygobject_version +\
     
    comm = "\nPython based easily configurable editor\n"\
        "with time accounting module.\n"\
        "\nRunning PyGtk %d.%d.%d" % GLib.pyglib_version +\
        "\nRunning GTK %d.%d.%d\n" % gver +\
        "\nRunning Python %s\n" % platform.python_version()
    dialog.set_comments(comm);
    dialog.set_copyright("Portions \302\251 Copyright Peter Glen\n"
                          "Project placed in the Public Domain.")
    dialog.set_program_name("PyEdPro")
    img_dir = os.path.join(os.path.dirname(__file__), 'images')
    img_path = os.path.join(img_dir, 'gtk-logo-rgb.gif')

    try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
        #print "loaded pixbuf"
        dialog.set_logo(pixbuf)

    except:
        print "Cannot load logo for about dialog", img_path;
        print sys.exc_info()
                    
    #dialog.set_website("")

    ## Close dialog on user response
    dialog.connect ("response", lambda d, r: d.destroy())
    dialog.connect("key-press-event", about_key)

    dialog.show()

def about_key(win, event):
    #print "about_key", event
    if  event.type == Gdk.EventType.KEY_PRESS:
        if event.keyval == Gdk.KEY_x or event.keyval == Gdk.KEY_X:
            if event.state & Gtk.gdk.MOD1_MASK:
                win.destroy()
    
# Show a regular message:

def message(strx, title = None):

    icon = Gtk.STOCK_INFO
    dialog = Gtk.MessageDialog(None, None,
                   Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, strx)
    
    dialog.set_transient_for(pyedlib.pedconfig.conf.pedwin.mywin);
    #dialog.parent =  
       
    if title:
        dialog.set_title(title)
    else:
        dialog.set_title("PyEdPro")

    dialog.set_position(Gtk.WindowPosition.CENTER)
        
    # Close dialog on user response
    dialog.connect("response", lambda d, r: d.destroy())
    dialog.show()

#EOF






