import tkinter
import threading
import time
from googletrans import Translator


# Lots of tutorials have from tkinter import *, but that is pretty much always a bad idea
from tkinter import ttk
import abc

class Menubar(ttk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, *args, **kwargs):
        ''' Constructor'''
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_menubar()

    def on_exit(self):
        '''Exits program'''
        quit()

    def display_help(self):
        '''Displays help document'''
        pass

    def display_about(self):
        '''Displays info about program'''
        pass

    def init_menubar(self):
        self.menubar = tkinter.Menu(self.root)
        self.menu_file = tkinter.Menu(self.menubar) # Creates a "File" menu
        self.menu_file.add_command(label='Exit', command=self.on_exit) # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file, label='File') # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tkinter.Menu(self.menubar) #Creates a "Help" menu
        self.menu_help.add_command(label='Help', command=self.display_help)
        self.menu_help.add_command(label='About', command=self.display_about)
        self.menubar.add_cascade(menu=self.menu_help, label='Help')

        self.root.config(menu=self.menubar)

class Window(ttk.Frame):
    """Abstract base class for a popup window"""
    __metaclass__ = abc.ABCMeta
    def __init__(self, parent):
        ''' Constructor '''
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.resizable(width=False, height=False) # Disallows window resizing
        self.validate_notempty = (self.register(self.notEmpty), '%P') # Creates Tcl wrapper for python function. %P = new contents of field after the edit.
        self.init_gui()

    @abc.abstractmethod # Must be overwriten by subclasses
    def init_gui(self):
        '''Initiates GUI of any popup window'''
        pass

    @abc.abstractmethod
    def do_something(self):
        '''Does something that all popup windows need to do'''
        pass

    def notEmpty(self, P):
        '''Validates Entry fields to ensure they aren't empty'''
        if P.strip():
            valid = True
        else:
            print("Error: Field must not be empty.") # Prints to console
            valid = False
        return valid

    def close_win(self):
        '''Closes window'''
        self.parent.destroy()

class SomethingWindow(Window):
    """ New popup window """

    def init_gui(self):
        self.parent.title("New Window")
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(3, weight=1)

        # Create Widgets

        self.label_title = ttk.Label(self.parent, text="This sure is a new window!")
        self.contentframe = ttk.Frame(self.parent, relief="sunken")

        self.label_test = ttk.Label(self.contentframe, text='Enter some text:')
        self.input_test = ttk.Entry(self.contentframe, width=30, validate='focusout', validatecommand=(self.validate_notempty))

        self.btn_do = ttk.Button(self.parent, text='Action', command=self.do_something)
        self.btn_cancel = ttk.Button(self.parent, text='Cancel', command=self.close_win)

        # Layout
        self.label_title.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.contentframe.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.label_test.grid(row=0, column=0)
        self.input_test.grid(row=0, column=1, sticky='w')

        self.btn_do.grid(row=2, column=0, sticky='e')
        self.btn_cancel.grid(row=2, column=1, sticky='e')

        # Padding
        for child in self.parent.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.contentframe.winfo_children():
            child.grid_configure(padx=5, pady=2)

    def do_something(self):
        '''Does something'''
        text = self.input_test.get().strip()
        if text:
            # Do things with text
            self.close_win()
        else:
            print("Error: But for real though, field must not be empty.")

class GUI(ttk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def openwindow(self):
        self.new_win = tkinter.Toplevel(self.root) # Set parent
        SomethingWindow(self.new_win)

    def init_gui(self):
        self.root.title('Translate_Tool')
        
        self.grid(column=0, row=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1) # Allows column to stretch upon resizing
        self.grid_rowconfigure(0, weight=1) # Same with row
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        self.root.wm_attributes("-topmost", 1)
        
        w = 600 # width for the Tk root
        h = 200 # height for the Tk root
        self.root.geometry(str(w)+"x"+str(h))
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        print(ws,hs)
        x = (ws/4*3) - (w/2)
        y = (hs/8) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
 
        # Menu Bar
        # self.menubar = Menubar(self.root)
        
        # Create Widgets
        self.btn = ttk.Button(self, text='Open Window', command=self.openwindow)

        # Layout using grid
        self.btn.grid(row=0, column=0, sticky='ew')

        # Padding
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=5)
        
        
        import tkinter.font as tkFont
        self.font = tkFont.Font(family="helvetica", size=18)
        self.font.configure(size=20)
        
        self.text = tkinter.Text(self.root, font=self.font)
        self.text.insert(tkinter.INSERT, "Zaaaa")
        self.text.insert(tkinter.END, "Warudo")
        self.text.grid(row=0, column=0, sticky='ew')

        self.widget_contents = tkinter.StringVar()
        self.widget_contents.set('')
        self.some_entry = tkinter.Entry(self,textvariable=self.widget_contents,width=10)
        self.some_entry.grid(row=0, column=0, sticky='ew')
        def entry1_callback(*args):
            global count 
            self.widget_contents.set(count)
        self.widget_contents.trace('w',entry1_callback)
        
      


      
        def my_callback(var, indx, mode):
            global result
            print(result, "call")
            self.text.delete('1.0',tkinter.END)
            self.text.insert(tkinter.INSERT,result.text)     
        global my_var
        my_var = tkinter.StringVar()
        my_var.trace_add('write', my_callback)        


def clipboard_threading(arg):
    global clipboard_buffer
    global result
    translator = Translator()
    count = 0
    refresh_rate = 500 / 1000 # sec
    clipboard_buffer_old = tkinter.Tk().clipboard_get()
    while True:
        clipboard_buffer = tkinter.Tk().clipboard_get()
        if clipboard_buffer != clipboard_buffer_old :
            clipboard_buffer_old = clipboard_buffer
            ''' translate task '''

            print("copy detected:",clipboard_buffer)
            result = translator.translate(clipboard_buffer ,src='ja' ,dest='th')
            print(result.text)
            
            global my_var
            my_var.set(result)

            ''' translate task '''
        count += 1
        time.sleep(refresh_rate)
        print("Count: {}".format(count))
  
def tkinter_threading(arg):

    root = tkinter.Tk()
    GUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=clipboard_threading, args=("arg",))
    t2 = threading.Thread(target=tkinter_threading, args=("arg",))
  
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # both threads completely executed
    print("Done!")


    