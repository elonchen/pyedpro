#!/usr/bin/env python

# ------------------------------------------------------------------------
# This is open source text editor. Written on python. The motivation for 
# this project was to create a modern multi-platform editor. 
# Simple, powerful, configurable, extendable.
#
# This project was derived from pydepro.py
# 
# pyedpro functions near flawless on Linux / Windows / Mac / Raspberry PI

#
# Pyedpro has:
#
#    o  macro recording/play, 
#    o  search/replace, 
#    o  functional navigation,
#    o  comment/string spell check, 
#    o  auto backup, 
#    o  persistent undo/redo,  (undo beyond last save) 
#    o  auto complete, auto correct, 
#    o  ... and a lot more. 
#
# It is fast, it is extendable. The editor has a table driven key mapping. 
# One can easily edit the key map in keyhand.py, and the key actions 
# in acthand.py The default key map resembles gedit / wed / etp / brief

# History:  (recent first, incomplete list)
#
# jul/19/2018   Coloring for spell check, Trigger by scroll, more dominant color
# Jul/xx/2018   Update README, KEYS.TXT
# Jun/xx/2018   Log Files for time accounting.
# Jun/xx/2018   Log Files for time accounting.
 

# ASCII test editor, requires pyGtk. See pygtk-dependencied for 
# eazy access to depencdencies.

import os, sys, getopt, signal

#import gobject
#import warnings
#warnings.simplefilter("ignore")
#import gtk
#warnings.simplefilter("default")

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#import pyedlib.keyhand, pyedlib.acthand

import pyedlib.pedutil, pyedlib.pedwin
import pyedlib.log, pyedlib.pedsql
import pyedlib.pedconfig

#from pyedlib.pedutil import *

mainwin = None
show_timing = 0
show_config = 0
clear_config = 0
use_stdout = 0
  
# ------------------------------------------------------------------------

def main(strarr):

    if(pyedlib.pedconfig.conf.verbose):
        print "pydepro running on", "'" + os.name + "'", \
            "GTK", Gtk._version, "PyGtk", \
               "%d.%d.%d" % (Gtk.get_major_version(), \
                    Gtk.get_minor_version(), \
                        Gtk.get_micro_version())

    signal.signal(signal.SIGTERM, terminate)
    mainwin = pyedlib.pedwin.EdMainWindow(None, None, strarr)
    pyedlib.pedconfig.conf.pedwin = mainwin 
    
    Gtk.main()
              
def help():

    print 
    print "pydepro version: ", pyedlib.pedconfig.conf.version
    print "Usage: " + os.path.basename(sys.argv[0]) + " [options] [[filename] ... [filenameN]]"
    print "Options:"
    print "            -d level  - Debug level 1-10. (Limited implementation)"
    print "            -v        - Verbose (to stdout and log)"
    print "            -f        - Start Full screen"
    print "            -c        - Dump Config"
    print "            -V        - Show version"
    print "            -x        - Clear (eXtinguish) config (will prompt)"
    print "            -h        - Help"
    print

# ------------------------------------------------------------------------

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
       
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
       
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
       
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

def terminate(arg1, arg2):

    if(pyedlib.pedconfig.conf.verbose):
        print "Terminating pydepro.py, saving files to ~/pydepro"
        
    # Save all     
    pyedlib.pedconfig.conf.pedwin.activate_quit(None)    
    #return signal.SIG_IGN

# Start of program:

if __name__ == '__main__':

    # Redirect stdout to a fork to real stdout and log. This way messages can 
    # be seen even if pydepro is started without a terminal (from the GUI)
    
    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h?fvxctVo")
    except getopt.GetoptError, err:
        print "Invalid option(s) on command line:", err
        sys.exit(1)

    #print "opts", opts, "args", args
    
    pyedlib.pedconfig.conf.version = 0.44

    for aa in opts:
        if aa[0] == "-d":
            try:
                pgdebug = int(aa[1])
            except:
                pgdebug = 0

        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-?": help();  exit(1)
        if aa[0] == "-V": print "Version", pyedlib.pedconfig.conf.version; \
            exit(1)
        if aa[0] == "-f": pyedlib.pedconfig.conf.full_screen = True
        if aa[0] == "-v": pyedlib.pedconfig.conf.verbose = True            
        if aa[0] == "-x": clear_config = True            
        if aa[0] == "-c": show_config = True            
        if aa[0] == "-t": show_timing = True
        if aa[0] == "-o": use_stdout = True
    
    try:
        if not os.path.isdir(pyedlib.pedconfig.conf.config_dir):
            if(pyedlib.pedconfig.conf.verbose):
                print "making", pyedlib.pedconfig.con.config_dir
            os.mkdir(pyedlib.pedconfig.conf.config_dir)
    except: pass
    
    # Let the user know it needs fixin'
    if not os.path.isdir(pyedlib.pedconfig.conf.config_dir):
        print "Cannot access config dir:", pyedlib.pedconfig.conf.config_dir
        sys.exit(1)

    if not os.path.isdir(pyedlib.pedconfig.conf.data_dir):
        if(pyedlib.pedconfig.conf.verbose):
            print "making", pyedlib.pedconfig.con.data_dir
        os.mkdir(pyedlib.pedconfig.conf.data_dir)
         
    if not os.path.isdir(pyedlib.pedconfig.conf.log_dir):
        if(pyedlib.pedconfig.conf.verbose):
            print "making", pyedlib.pedconfig.conf.log_dir
        os.mkdir(pyedlib.pedconfig.conf.log_dir)
    
    if not os.path.isdir(pyedlib.pedconfig.conf.macro_dir):
        if(pyedlib.pedconfig.conf.verbose):
            print "making", pyedlib.pedconfig.conf.macro_dir
        os.mkdir(pyedlib.pedconfig.conf.macro_dir)

    if(pyedlib.pedconfig.conf.verbose):
        print "Data stored in ", pyedlib.pedconfig.conf.config_dir
        
    # Initialize sqlite to load / save preferences & other info    
    sql = pyedlib.pedsql.pedsql(pyedlib.pedconfig.conf.sql_data)
        
    # Initialize pedconfig for use  
    pyedlib.pedconfig.conf.sql = sql
    pyedlib.pedconfig.conf.keyh = pyedlib.keyhand.KeyHand()
    pyedlib.pedconfig.conf.mydir = os.path.abspath(__file__)

    # To clear all config vars
    if clear_config:    
        print "Are you sure you want to clear config ? (y/n)"
        sys.stdout.flush()
        aa = sys.stdin.readline()
        if aa[0] == "y":
            print "Removing configuration ... ",
            sql.rmall()        
            print "OK"
        sys.exit(0)

    # To check all config vars
    if show_config:    
        print "Dumping configuration:"
        ss = sql.getall(); 
        for aa in ss: 
            print aa
        sys.exit(0)

    #Uncomment this for silent stdout
    if use_stdout:
        print "Using stdout"
        sys.stdout = Unbuffered(sys.stdout)
        sys.stderr = Unbuffered(sys.stderr)
    else:
        sys.stdout = pyedlib.log.fake_stdout()
        sys.stderr = pyedlib.log.fake_stdout()
        
    # Uncomment this for buffered output
    if pyedlib.pedconfig.conf.verbose:
        print "Started pydepro"
        #pyedlib.log.print("Started pydepro")
     
    main(args[0:])

# EOF


