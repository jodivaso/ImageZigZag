from tkinter import ttk
import tkinter


class TreeviewFrame(ttk.Frame):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vscrollbar = ttk.Scrollbar(content, orient=tkinter.VERTICAL)
        self.treeview = ttk.Treeview(
            content,
            yscrollcommand=self.vscrollbar.set,
            height=3
        )
        self.vscrollbar.config(command=self.treeview.yview)
        self.vscrollbar.grid(row=0, column=1, sticky="ns")
        self.treeview.grid(row=0, column=0)
