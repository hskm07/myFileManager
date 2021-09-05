#!/usr/bin/python3
import glob
import os
import subprocess

import tkinter as tk
import tkinter.ttk as ttk


def searchfiles(path):

    search = {}
    if os.path.isdir(path):
        for f in glob.glob(path + '/**', recursive=True):
            print('base : ' + os.path.basename(f))
            print('Abs : ' + os.path.abspath(f))


class treeviewHeading(tk.Frame):
    def __init__(self, main):
        super().__init__(main)
        #self.columnconfigure(0, weight=1)

        self.csv = self.searchcsv(os.getcwd())
        self.create_treeview_headings()
        
    def create_treeview_headings(self):
        
        self.label = tk.Label(self, text = "CSV File Manager")
        self.label.grid(row=0, column=0, pady=1)
        self.htree = ttk.Treeview(self, height=15, selectmode="extended")
        
        # set content
        self.htree["columns"] = (1,2)
        self.htree["show"] = "headings"
        self.htree.column(1, width=250)
        self.htree.column(2, width=250)

        # set header name
        self.htree.heading(1, text='FILE NAME')
        self.htree.heading(2, text='EXTENSION')

        # make recode
        for key, value in sorted(self.csv.items(), key=lambda x: x[1]):
            self.htree.insert("", "end", values=(str(key), str(value)))
                    
        self.htree.grid(row=1, column=0, padx=5, pady=5)

        # set scrollbar
        hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.htree.xview)
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.htree.yview)
        self.htree.configure(xscrollcommand=hscrollbar.set)
        self.htree.configure(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NS)
        hscrollbar.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
        
        self.create_Button(self.htree)

    def create_Button(self, tree):
        button = tk.Button(text='select', command=lambda: self.clk_event(tree))
        button.grid(row=1, column=0, padx=5, pady=5)
        #button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        #close_btn = tk.Button(text = 'close')
        #close_btn.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

    def clk_event(self, tree):
        try:
            selected = tree.selection()
            # debug
            # print(tree.item(selected[0]))
            select_path = tree.item(selected[0])['values'][0]
            print(select_path)
        except Exception as e:
            print("Error : ", e)
        
    
    def searchcsv(self, path):
        csvfiles = {}
        if os.path.isdir(path):
            for f in glob.glob(path + '/*.csv', recursive=True):
                root, base = os.path.split(f)
                csvfiles[base] = root
        return csvfiles



class treeviewFrame(tk.Frame):
    def __init__(self, main):
        super().__init__(main)

        self.search = self.searchfiles(os.getcwd())
        self.create_treeview()


    def create_treeview(self):
       
        self.label = tk.Label(self, text="TreeView")
        self.label.grid(row=0, column=0,pady=0)

        self.ttree = ttk.Treeview(self, height=15, selectmode="browse")
        self.ttree['show'] = "tree"
        # set scrollbar
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.ttree.yview)
        self.ttree.configure(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NS)
         
        self.ttree.grid(row=1, column=0, padx=5, pady=5)


        for key, value in sorted(self.search.items()):
            if len(value) == 0:
                continue

            sort_val = sorted(value)
            if key == '.':
                for v in sort_val:
                    self.ttree.insert("", "end", text=v)
            else:
                parent = self.ttree.insert("", "end", text=os.path.basename(key))
                for v in sort_val:
                    self.ttree.insert(parent, "end", text=v)


    def searchfiles(self, path):    
        search = {}
        for f in glob.glob(path + '/**', recursive=True):
            if os.path.isdir(f):
                search.setdefault(f, [])
            else:
                parent_path, base_name = os.path.split(f)
                if parent_path == path:
                    parent_path = '.'
                search.setdefault(parent_path, []).append(base_name)

        return search

def main():
    root = tk.Tk()
    root.geometry('800x500')
    root.title('Show Direcotry Application')
    frame1 = treeviewHeading(main=root)
    frame2 = treeviewFrame(main=root)
    frame1.grid(column=0, row=0)
    frame2.grid(column=1, row=0)
    root.mainloop()
        



if __name__ == '__main__':

    #PATH = r'/home/atmark/Document/myFTPapp'
    #searchfiles(PATH)
    main()
