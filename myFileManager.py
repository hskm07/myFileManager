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


class ShowDirApp(tk.Frame):
    def __init__(self, main):
        super().__init__(main)
        self.pack()

        self.grid()
        self.columnconfigure(0, weight=1)

        self.search = self.searchfiles(os.getcwd())
        self.csv = self.searchcsv(os.getcwd())
        self.create_treeview_headings()
        self.create_treeview()
        

    
    def create_treeview_headings(self):
        self.htree = ttk.Treeview(self, height=15, selectmode="extended")
        
        # set content
        self.htree["columns"] = (1,2)
        self.htree["show"] = "headings"
        self.htree.column(1, width=250)
        self.htree.column(2, width=200)

        # set header name
        self.htree.heading(1, text='FILE NAME')
        self.htree.heading(2, text='EXTENSION')

        # make recode
        for key, value in sorted(self.csv.items(), key=lambda x: x[1]):
            self.htree.insert("", "end", values=(str(key), str(value)))
                    
        self.htree.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


        # set scrollbar
        hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.htree.xview)
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.htree.yview)
        self.htree.configure(xscrollcommand=hscrollbar.set)
        self.htree.configure(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky=tk.NS)
        hscrollbar.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=tk.EW)
        
        self.create_Button(self.htree)


    def create_treeview(self):
        self.ttree = ttk.Treeview(self, height=15, selectmode="browse")
        self.ttree['show'] = "tree"
         
        self.ttree.grid(row=0, column=2, padx=5, pady=5)
        for key, value in self.search.items():
            #print('key: {0}, value : {1}'.format(key, value))
            parent = self.ttree.insert("", "end", text=os.path.basename(key))
            for v in value:
                self.ttree.insert(parent, "end", text=v)




    def create_Button(self, tree):
        button = tk.Button(text='select', command=lambda: self.clk_event(tree))
        button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
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
        
    
    def searchfiles(self, path):    
        search = {}
        for f in glob.glob(path + '/**', recursive=True):
            if os.path.isdir(f):
                search.setdefault(f, [])
            else:
                path, base = os.path.split(f)
                search.setdefault(path, []).append(base)

        return search

    def searchcsv(self, path):
        csvfiles = {}
        if os.path.isdir(path):
            for f in glob.glob(path + '/*.csv', recursive=True):
                root, base = os.path.split(f)
                csvfiles[base] = root
        return csvfiles


def main():
    root = tk.Tk()
    root.geometry('1000x500')
    root.title('Show Direcotry Application')
    app = ShowDirApp(main=root)
    app.mainloop()
        



if __name__ == '__main__':

    #PATH = r'/home/atmark/Document/myFTPapp'
    #searchfiles(PATH)
    main()


