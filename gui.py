"""
TODO:
file name on title

"""

import tkinter as tk
from tkinter import filedialog as fd
import tkinter.messagebox
import os
import pyperclip

class Gui:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Python GUI based TextEditor / New File")
        self.main_window.geometry("{}x{}".format(800, 600))
        self.main_window.grid_rowconfigure(1, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)
        self.menu_frame = tk.Frame(self.main_window)
        self.text_frame = tk.Frame(self.main_window)
        self.footer_frame = tk.Frame(self.main_window)
        self.menu_frame.grid(row=0, sticky="nwes")
        self.text_frame.grid(row=1, sticky="nsew")
        self.footer_frame.grid(row=2, sticky="sew")
        self.text_frame.propagate(False)
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.top_menu = tk.Menu(self.menu_frame)
        self.main_window.config(menu=self.top_menu)
        self.file_menu = tk.Menu(self.top_menu, tearoff=0)
        self.edit_menu = tk.Menu(self.top_menu, tearoff=0)
        self.view_menu = tk.Menu(self.top_menu, tearoff=0)

        self.top_menu.add_cascade(label="File", menu=self.file_menu)
        self.top_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.top_menu.add_cascade(label="View", menu=self.view_menu)

        self.file_menu.add_checkbutton(label="New file", command=self.new_file)
        self.file_menu.add_cascade(label="Open file", command=self.open_file)
        self.file_menu.add_cascade(label="Save...", command=self.save)
        self.file_menu.add_cascade(label="Save as", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_cascade(label="Exit", command=self.on_quit)

        self.edit_menu.add_cascade(label="Copy", command=self.copy)
        self.edit_menu.add_cascade(label="Cut", command=self.cut)
        self.edit_menu.add_cascade(label="Paste", command=self.paste)
        self.edit_menu.add_cascade(label="Select all", command=self.sall)
        self.wrap_ckd = tk.IntVar()
        self.wrap_ckd.set(0)
        self.foot_ckd = tk.IntVar()
        self.foot_ckd.set(0)
        self.view_menu.add_checkbutton(label="Wrap lines", command=self.wrap, variable=self.wrap_ckd, onvalue=1, offvalue=0)
        self.view_menu.add_checkbutton(label="Show footer", command=self.footer, variable=self.foot_ckd, onvalue=1, offvalue=0)

        self.editor_field = tk.Text(self.text_frame, wrap=tk.NONE)
        self.editor_field.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_vert = tk.Scrollbar(self.text_frame, command=self.editor_field.yview, orient=tk.VERTICAL)
        self.scrollbar_vert.grid(row=0, column=1, sticky="nsew")
        self.editor_field['yscrollcommand'] = self.scrollbar_vert.set
        self.scrollbar_horiz = tk.Scrollbar(self.text_frame, command=self.editor_field.xview, orient=tk.HORIZONTAL)
        self.scrollbar_horiz.grid(row=1, column=0, sticky="nsew")
        self.editor_field['xscrollcommand'] = self.scrollbar_horiz.set
        self.editor_field.bind('<<Modified>>', self.modified)
        lab = tk.Label(self.footer_frame, text="check check", anchor=tk.N)
        lab.pack()

        self.file_name = ""
        self.main_window.mainloop()
    def modified(self, event):
        return True
    def new_file(self):
        self.editor_field.delete("0.0", 'end')
        self.main_window.title("Python GUI based TextEditor / New File")

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
                self.main_window.title("Python GUI based TextEditor / " + self.file_name)
        except Exception as e:
            tkinter.messagebox.askretrycancel(title="Error", message="Something went wrong....")
            print(e)

    def save_as(self):
        self.file_name = fd.asksaveasfilename(initialdir="C:\\Users\\" + os.getlogin() + "\\Documents",
                                              filetypes=[("Text files", "txt")])
        try:
            if self.file_name == "":
                return
            else:
                f = open(self.file_name + ".txt", "a")
                f.write(self.editor_field.get("0.0", 'end-1c'))
                self.main_window.title("Python GUI based TextEditor / ")
        except Exception as e:
            tkinter.messagebox.askretrycancel(title="Error", message="Something went wrong....")
            print(e)

    def save(self):
        if self.file_name != "":
            try:
                f = open(self.file_name, "w")
                f.write(self.editor_field.get("0.0", 'end-1c'))
            except Exception as e:
                tkinter.messagebox.askretrycancel(title="Error", message="Something went wrong....")
                print(e)
        else:
            self.save_as()

    def on_quit(self):
        if self.editor_field.get('1.0', 'end') != '' or self.modified() is True:
            save_or_not = tkinter.messagebox.askyesno("Save", "Save changes?")
            if save_or_not is True:
                self.save_as()
            else:
                self.main_window.quit()
        else:
            self.main_window.quit()
    def copy(self):
        pyperclip.copy(self.editor_field.selection_get())

    def paste(self):
        self.editor_field.insert(tk.INSERT, pyperclip.paste())

    def cut(self):
        pyperclip.copy(self.editor_field.selection_get())
        self.editor_field.delete(tk.SEL_FIRST, tk.SEL_LAST)

    def sall(self):
        self.editor_field.tag_add('sel', '1.0', tk.END)
    def wrap(self):
        if self.wrap_ckd.get() == 1:
            self.editor_field.config(wrap=tk.WORD)
            self.scrollbar_horiz.grid_remove()
        else:
            self.editor_field.config(wrap=tk.NONE)
            self.scrollbar_horiz.grid()
    def footer(self):
        return