from genericpath import isfile
from os import listdir
from os.path import isfile, join
from Bio import SeqIO
import pandas as pd

input_variables = "------------------------------------------------------------------------------------------------------------------------------------------------------"

folder_filepath = r"C:\Users\jaspe\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\03 MCRI\Full length CNV sequences\CNVS"
outputname = "MCRI amplicons"

non_input = "------------------------------------------------------------------------------------------------------------------------------------------------------------"

filesInFolder = [f for f in listdir(folder_filepath) if isfile(join(folder_filepath, f))]

orderingsnumber = 0
amplicon_list = []

for filename in filesInFolder:
    if ".fasta" in filename:
        file_path = folder_filepath + "\\" + filename
        for record in SeqIO.parse(file_path, "fasta"):
            orderingsnumber += 1
            filename_only = filename.replace(".fasta", "")
            amplicon_list.append(str(orderingsnumber) + ". " + filename_only + ": " + str(len(record.seq)) + "bp" + ": " + record.description + ": " + record.seq)
    else:
        print(filename,"is not a .fasta file.")
        continue

print(amplicon_list)

df = pd.DataFrame(amplicon_list)
df.to_csv(outputname + ".csv")