#! /usr/bin/python
def create_tmp_folder(foldername):
 import os
 os.system("mkdir -p %s"%(foldername))
 os.system("mkdir -p %s/data"%(foldername))
def clean_up(foldername , path):
 import os
 os.system("cp -u %s/data/swffile.swf %s"%(foldername , path))
 os.system("rm -rf %s"%(foldername))
def check_path(path_got):
 import os
 import os.path
 if os.path.isfile(path_got):
    return path_got
 else:
    quit("File is missing or is not readable.")
def filename_get(data):
    split_data = data.split("/")
    filename = split_data[-1]
    return filename
def filelocation_get(filename,file_path):
 location = file_path.replace(filename,"")
 return location
def terminal():
 def gui():
   import pygtk
   import gtk
   dialog = gtk.FileChooserDialog("select swf file to open..",None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))
   dialog.set_default_response(gtk.RESPONSE_OK)
   filter = gtk.FileFilter()
   filter.set_name("swf files")
   filter.add_pattern("*.swf")
   dialog.add_filter(filter)
   response = dialog.run()
   if response == gtk.RESPONSE_OK:
       data = dialog.get_filename()
       dialog.destroy()
       return data
   elif response == gtk.RESPONSE_CANCEL:
       return False
       dialog.destroy()
 from optparse import OptionParser
 parser = OptionParser(usage="usage: %prog  filename",version="%prog 1.0")
 parser.add_option("-g", "--gui",action="store_true", dest="gui",help="start gui mode")
 parser.add_option("-c", "--cli",action="store_true", dest="cli",help="start comand line mode")
 (options, args) = parser.parse_args()
 if options.gui == True:
  mode = 1
 if options.cli == True:
  mode = 2
 if mode == 2:
  if len(args) != 1:
   parser.error("wrong number of arguments")
  terminal_data = args[0]
  return terminal_data
 if mode == 1:
  terminal_data = gui()
  if terminal_data == False:
   quit("no files selected.")
  else:
   return terminal_data
def html_gen(location):
 html_data= """<html>\n<body>\n<object type="application/x-shockwave-flash" data="./data/swffile.swf"\n width="801" height="450">\n<param name="movie" value="swffile.swf">\n<param name="quality" value="high">\n<param name="bgcolor" value="#ffffff">\n<param name="play" value="true">\n<param name="loop" value="true">\n<param name="wmode" value="window">\n<param name="scale" value="showall">\n<param name="menu" value="true">\n<param name="devicefont" value="false">\n<param name="salign" value="">\n<param name="allowScriptAccess" value="sameDomain">\n</object>\n</body>\n</html>\n"""
 file = open("%s/runner.html"%(location), "w")
 file.write(html_data)
 file.close()
def cp_data(location1,location2):
 import os
 os.system("cp %s %s/data/swffile.swf"%(location1,location2))
def swf_player(data_location):
 import webkit
 import gobject
 import gtk
 global got_data
 got_data = data_location
 class Browser:
    data = got_data
    
    def delete_event(self, widget, event, data=None):
        return False
    def destroy(self, widget, data=None):
        gtk.main_quit()
    def __init__(self):
        gobject.threads_init()
        import gtk
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.set_title("Swf Player")
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.web_view = webkit.WebView()
        self.web_view.open(self.data)      
        scroll_window = gtk.ScrolledWindow(None, None)
        scroll_window.set_size_request(801, 450)
        scroll_window.add(self.web_view)     
        vbox = gtk.VBox(False, 0)
        vbox.add(scroll_window)
        self.window.add(vbox)
        self.window.show_all()
    def main(self):
        gtk.main()
 if __name__ == "__main__":
    browser = Browser()
    browser.main()

terminal_data = terminal()

filepath = check_path(terminal_data)
filename = filename_get(filepath)
filelocation = filelocation_get(filename,filepath)
tmp_location = ("/tmp/swfplayer/%s"%(filename))
create_tmp_folder(tmp_location)
html_gen(tmp_location)
cp_data(filepath , tmp_location)
browser_data = ("file:///tmp/swfplayer/%s/runner.html"%(filename))
swf_player(browser_data)
clean_up(tmp_location  , filepath)
