#!/usr/bin/python3
##################################
# Author: Olga Tsiouri
# Website: https://linktr.ee/otsiouri
# Usage: psrnatarget2fa.py <psrnatarget_output.txt>
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

import sys

try:
    input_file = str(sys.argv[1])

except IndexError:
    print("ERROR: Input txt file missing")
    sys.exit(1)

if not input_file.endswith(".txt"):
    print("ERROR: Input file should be txt")
    sys.exit(1)    

try:
    # Import the psRNATarget output txt as list in python
    with open(input_file, "r") as fin:
        lines = [line.strip() for line in fin]

    # Retrieve the 1st column with the miRNA names
    # lines[2:] is used to remove the 1st 2 lines: 
    # line 1: "#Please import the downloaded file into Microsoft Excel or other speadsheet software"
    # line 2: "miRNA_Acc.	Target_Acc.	Expectation	UPE$	miRNA_start	miRNA_end	Target_start	Target_end	miRNA_aligned_fragment	alignment	Target_aligned_fragment	Inhibition	Target_Desc.	Multiplicity"
    miRNA_names = [str(line.split("\t")[0]).strip() for line in lines[2:]]

    # Do the same for the mRNA targets & replace urakil to thymine
    targets = [str(line.split("\t")[10]).strip().replace("U","T") for line in lines[2:]]

    # Retrieve the mRNA sequence name and add .mRNA.aln.fasta as the output file extension
    output_file = str(lines[2].split("\t")[1]).strip() + ".mRNA.aln.fasta"

    # Export to file
    with open(output_file,"w") as fout:
        fout.writelines(f">{name}\n{target}\n" for name, target in zip(miRNA_names, targets))
    
    # Notification that the program is finished
    print(f"Output file {output_file} created")

except Exception as e:
    print(f"ERROR:\n{e}")
