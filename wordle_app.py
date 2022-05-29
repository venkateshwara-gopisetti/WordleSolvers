# -*- coding: utf-8 -*-
"""
Created on Sat May 14 00:19:35 2022

@author: Venkat
"""

# =============================================================================
# Importing Libraries
# =============================================================================

import tkinter as tk
import tkinter.scrolledtext as st

from src.wordle_objects import WordleBot, WordleServer

# pylint: disable=too-many-ancestors
class MYGUI(tk.Frame):
    """_summary_

    Args:
        tk (_type_): _description_
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.root.title('TEST')
        self.root.option_add('*tearOff', 'FALSE')
        options = {'padx': 5, 'pady': 5}
        # temperature label
        self.task_label = tk.Label(self, text='Task')
        self.task_label.grid(column=0, row=0, sticky=tk.W, **options)

        # temperature entry
        self.task = tk.StringVar()
        self.task_entry = tk.Entry(self, textvariable=self.task)
        self.task_entry.grid(column=1, row=0, **options)
        self.task_entry.focus()

        self.solve_button = tk.Button(self, text='Solve')
        self.solve_button['command'] = self.solve
        self.solve_button.grid(column=2, row=0, sticky=tk.W, **options)

        # result label
        self.result_label = tk.Label(self)
        self.result_label.grid(row=1, columnspan=3, **options)

        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)
        self.grid(column=0, row=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1, uniform='a')
        self.grid_columnconfigure(1, weight=1, uniform='a')
        self.grid_columnconfigure(2, weight=1, uniform='a')
        self.grid_columnconfigure(3, weight=1, uniform='a')

        self.text_area = st.ScrolledText(self.root,
                                width = 30,
                                height = 8,
                                font = ("Times New Roman",
                                        15))

        self.text_area.grid(column = 0, pady = 10, padx = 10)

    def solve(self):
        """_summary_
        """
        self.text_area.delete("1.0",tk.END)
        task = self.task.get()
        wordleserver = WordleServer(task)
        bot = WordleBot()
        total_iterations, answer, used_words  = bot.solver1(server=wordleserver)
        for wrd in used_words:
            self.text_area.insert(tk.END, wrd)
            self.text_area.insert(tk.END, '\n')
        self.text_area.insert(tk.END, answer)
        self.text_area.insert(tk.END, '\n')
        self.text_area.insert(tk.END, f"Total Iterations - {total_iterations}")
        self.text_area.insert(tk.END, '\n')
        # self.root.update()
        # Making the text read only

if __name__=="__main__":
    root = tk.Tk()
    MYGUI(root)
    root.mainloop()
