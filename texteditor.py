import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox
import os
import pyperclip


class TextEditor:
    def __init__(self):
        # create main window and frames
        self.main_window = tk.Tk()
        self.main_window.title("Python GUI based TextEditor / New File")
        self.main_window.geometry("{}x{}".format(800, 600))
        self.main_window.grid_rowconfigure(1, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)
        self.main_window.protocol('WM_DELETE_WINDOW', self.on_quit)

        self.menu_frame = tk.Frame(self.main_window)
        self.text_frame = tk.Frame(self.main_window)
        self.footer_frame = tk.Frame(self.main_window)

        self.menu_frame.grid(row=0, sticky="nwes")
        self.text_frame.grid(row=1, sticky="nsew")
        self.footer_frame.grid(row=2, sticky="sew")
        self.text_frame.propagate(False)
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)

        # create top menu and adding options
        self.top_menu = tk.Menu(self.menu_frame)
        self.main_window.config(menu=self.top_menu)
        self.file_menu = tk.Menu(self.top_menu, tearoff=0)
        self.edit_menu = tk.Menu(self.top_menu, tearoff=0)
        self.view_menu = tk.Menu(self.top_menu, tearoff=0)

        self.top_menu.add_cascade(label="File", menu=self.file_menu)
        self.top_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.top_menu.add_cascade(label="View", menu=self.view_menu)

        self.file_menu.add_cascade(label="New file", command=self.new_file)
        self.file_menu.add_cascade(label="Open file", command=self.open_file)
        self.file_menu.add_cascade(label="Save...", command=self.save)
        self.file_menu.add_cascade(label="Save as", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_cascade(label="Exit", command=self.on_quit)

        self.edit_menu.add_cascade(label="Copy", command=self.copy)
        self.edit_menu.add_cascade(label="Cut", command=self.cut)
        self.edit_menu.add_cascade(label="Paste", command=self.paste)
        self.edit_menu.add_cascade(label="Select all", command=self.sall)
        self.wrap_ckd = tk.IntVar()  # int variables for checkbuttons
        self.wrap_ckd.set(0)  # this one is set to 0, because, in default, there is no wraping
        self.foot_ckd = tk.IntVar()
        self.foot_ckd.set(1)  # this one is set to 1, because, in default, footer is shown
        self.view_menu.add_checkbutton(label="Wrap lines", command=self.wrap, variable=self.wrap_ckd,
                                       onvalue=1, offvalue=0)
        self.view_menu.add_checkbutton(label="Show footer", command=self.footer, variable=self.foot_ckd,
                                       onvalue=1, offvalue=0)

        # setting text widget
        self.editor_field = tk.Text(self.text_frame, wrap=tk.NONE)
        self.editor_field.grid(row=0, column=0, sticky="nsew")

        # setting vertical scrollbar
        self.scrollbar_vert = tk.Scrollbar(self.text_frame, command=self.editor_field.yview, orient=tk.VERTICAL)
        self.scrollbar_vert.grid(row=0, column=1, sticky="nsew")
        self.editor_field['yscrollcommand'] = self.scrollbar_vert.set
        # setting vertical scrollbar, which can be hidden when wrapping is on
        self.scrollbar_horiz = tk.Scrollbar(self.text_frame, command=self.editor_field.xview, orient=tk.HORIZONTAL)
        self.scrollbar_horiz.grid(row=1, column=0, sticky="nsew")
        self.editor_field['xscrollcommand'] = self.scrollbar_horiz.set

        # binding events for modifying text field or releasing a key
        self.editor_field.bind('<<Modified>>', self.modified)
        self.editor_field.bind('<KeyRelease>', self.update_footer)

        # setting footer
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.footer_frame.grid_columnconfigure(1, weight=1)

        # on the left side it will be displayed current state of file (opened, saved, name)
        # and it will disappear after 5 seconds
        self.file_info = tk.Label(self.footer_frame, text="New text file", anchor=tk.W)
        self.file_info_updater()

        # on the right side it will be displayed current position of cursor
        # it's set to Line1 Col1 for now, but it will change after <KeyRelease>
        self.coordinates = tk.Label(self.footer_frame, text="Line: 1, Col: 1", anchor=tk.W)
        self.coordinates.grid(column=1, row=0, sticky=tk.W)

        self.file_name = ""  # variable for file name
        self.flag = False
        self.main_window.mainloop()

    def file_info_updater(self):
        self.file_info.grid(column=0, row=0, sticky=tk.W)
        self.file_info.after(5000, self.clear_label)

    def modified(self, _):  # method binded to <KeyRelease>, returns TRUE after releasing key
        self.flag = True
        return self.flag

    def new_file(self):  # basically clears text widget and changes window title
        self.editor_field.delete("0.0", 'end')
        self.main_window.title("Python GUI based TextEditor / New File")
        self.file_info = tk.Label(self.footer_frame, text="New text file", anchor=tk.W)
        self.file_info_updater()

    """
    Opens new file.
    Variable self_name stores file names taken from askopenfilename function
    If user clicked 'X' or Cancel and file_name is empty string function returns nothing
    If opposide it opens file and insert in text widget all lines one by one
    """
    def open_file(self):
        self.file_name = fd.askopenfilename(initialdir="C:\\Users\\" + os.getlogin() + "\\Documents",
                                            filetypes=[("Text files", "txt")])
        try:
            if self.file_name == "":
                return
            else:
                with open(self.file_name) as f:
                    for line in f:
                        self.editor_field.insert(tk.END, line)
                current_file = self.file_name[self.file_name.rfind("/", 0, len(self.file_name))+1:]
                self.main_window.title("Python GUI based TextEditor / "
                                       + current_file)
                self.file_info.config(text="Opened file " + current_file)
                self.file_info_updater()

        except Exception as e:
            tkinter.messagebox.askretrycancel(title="Error", message="Something went wrong....")
            print(e)

    def save_as(self):  # basically same as open_file but instead of opening it saves
        self.file_name = fd.asksaveasfilename(initialdir="C:\\Users\\" + os.getlogin() + "\\Documents",
                                              filetypes=[("Text files", "txt")])
        print(self.file_name)
        try:
            if self.file_name == "":
                return
            else:
                f = open(self.file_name + ".txt", "a")
                f.write(self.editor_field.get("0.0", 'end-1c'))
                current_file = self.file_name[self.file_name.rfind("/", 0, len(self.file_name)) + 1:]
                self.main_window.title("Python GUI based TextEditor / "
                                       + current_file)
                self.file_info.config(text="Saved as " + current_file)
                self.file_info_updater()
        except Exception as e:
            tkinter.messagebox.askretrycancel(title="Error", message="Something went wrong....")
            print(e)

    """
    This function checks if file_name is set. If yes it means that we working on file which exist on hard drive,
    so there' no need for asking a name. So it opens that file, clears it and rewrites it
    If no it means we working on new file, so save_as() function is called
    """
    def save(self):
        if self.file_name != "":
            try:
                f = open(self.file_name, "w")
                f.write(self.editor_field.get("0.0", 'end-1c'))
                self.file_info.config(text="File saved")
                self.file_info_updater()
            except Exception as e:
                tkinter.messagebox.askretrycancel(title="Error", message="Something went wrong....")
                print(e)
        else:
            self.save_as()

    """
    Function checks if text widget was modified (ergo file was modified).
    If it was, save_as() function is calles
    If it wasn't, program quits with os.quit() method
    """
    def on_quit(self):
        if self.flag is True:
            save_or_not = tkinter.messagebox.askyesno("Save", "Save changes?")
            if save_or_not is True:
                self.save_as()
            else:
                self.main_window.quit()
        else:
            self.main_window.quit()

    """
    Functions copy, cut, paste
    There was no cut method in pyperclip library, so, when CUT is pressed
    it copies selected text and deletes it
    """
    def copy(self):
        pyperclip.copy(self.editor_field.selection_get())

    def paste(self):
        self.editor_field.insert(tk.INSERT, pyperclip.paste())

    def cut(self):
        pyperclip.copy(self.editor_field.selection_get())
        self.editor_field.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def sall(self):  # function select all text
        self.editor_field.tag_add('sel', '1.0', tk.END)

    """
    Function sets wrapping in text widget. If wrapping is on - horizontal scrollbar is removes
    If wrapping is off - horizontal scrollbar is set again
    """
    def wrap(self):
        if self.wrap_ckd.get() == 1:
            self.editor_field.config(wrap=tk.WORD)
            self.scrollbar_horiz.grid_remove()
        else:
            self.editor_field.config(wrap=tk.NONE)
            self.scrollbar_horiz.grid()

    def update_footer(self, _):  # after key release function gets current cursor position and updates footer
        cor = self.editor_field.index(tk.INSERT).split(".")

        self.coordinates.config(text="Line: " + cor[0] + ", Col: " + str(int(cor[1]) + 1))

    def clear_label(self):  # removes file status label after 5 seconds (method after)
        self.file_info.grid_remove()

    def footer(self):
        if self.foot_ckd.get() == 0:
            self.footer_frame.grid_remove()
        else:
            self.footer_frame.grid()

if __name__ == "__main__":
    new_window = TextEditor()
