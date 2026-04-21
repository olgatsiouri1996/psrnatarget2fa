
##################################
# Author: Olga Tsiouri
# Website: https://linktr.ee/otsiouri
##################################

"""
MIT License

Copyright (c) 2026 Olga Tsiouri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_merge(input_file, progress_bar):
    try:

        # Start the progress bar
        progress_bar.start()

        # Import the psRNATarget output txt as list in python
        with open(input_file, "r") as fin:
            lines = [line.strip() for line in fin]

        # Retrieve the 1st column with the miRNA names
        # lines[2:] is used to remove the 1st 2 lines: 
        # line 1: "#Please import the downloaded file into Microsoft Excel or other speadsheet software"
        # line 2: "miRNA_Acc.	Target_Acc.	Expectation	UPE$	miRNA_start	miRNA_end	Target_start	Target_end	miRNA_aligned_fragment	alignment	Target_aligned_fragment	Inhibition	Target_Desc.	Multiplicity"
        miRNA_names = [str(line.split("\t")[0]).strip() for line in lines[2:]]

        # Do the same for the mRNA targets & replace urakil to thymine
        mrna_targets = [str(line.split("\t")[10]).strip().replace("U","T") for line in lines[2:]]

        # Retrieve the mRNA sequence name and add .mRNA.aln.fasta as the output file extension
        output_file = str(lines[2].split("\t")[1]).strip() + ".mRNA.aln.fasta"

        # Create path to save the output fasta in the same folder as the input txt
        # ".replace("/","\\")" converts the folder slashes 
        output_filepath = str(os.path.join(os.path.dirname(input_file),output_file)).replace("/","\\")

        # Export to file
        with open(output_filepath,"w") as fout:
            fout.writelines(f">{name}\n{target}\n" for name, target in zip(miRNA_names, mrna_targets))

        progress_bar.stop()
        messagebox.showinfo("Success",f"FASTA file created at:\n{output_filepath}")

    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error",f"Error: {e}")
        
def start_thread():
    input_file = input_file_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input txt file.")
        return
    
    if not input_file.endswith(".txt"):
        messagebox.showwarning("Input Error", "The input file should be in txt format.")
        return

    # Start command in a new thread
    thread = threading.Thread(target=run_merge, args=(input_file, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("psRNATarget txt2fasta  Converter")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input txt file:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Convert to FASTA", command=start_thread).grid(row=2, column=1, padx=10, pady=20)

# Trademark label
trademark_label = tk.Label(app,  text="Copyright (c) Olga Tsiouri, 2026 <olgatsiouri@outlook.com>", font=("Arial", 10), fg="black")
trademark_label.grid(row=3, column=0, columnspan=3, pady=(20, 10), sticky="s")

app.mainloop()
