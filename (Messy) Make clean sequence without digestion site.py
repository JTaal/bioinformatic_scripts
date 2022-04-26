from genericpath import isfile
from os import listdir
from os.path import isfile, join
from Bio import SeqIO

"""_______________Input_____________________________________________________________________________________________________________________________________________
"""

#inputpath = input("Give folder:")
amplicon_filepath = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Amplicon sequences"
#digest_enzyme_filepath = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Digestion sites\Alator Bioscience"
output_path = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Final sequence"

"""_______________Code______________________________________________________________________________________________________________________________________________
"""

#setting up all directory variables
output_file = ""
output_filename = "Insertion sequence (clean).fasta"
output_fileID = ">Insertion sequence\n"
output_filepath = output_path + "\\" + output_filename

amplicon_list = []
amplicon_listname = "List of amplicon order (clean).txt"
amplicon_list_outputpath = output_path + "\\" + amplicon_listname

#extract digest enzyme sequence
#digest_enzyme = open(digest_enzyme_filepath + "\\" + enzyme_name + ".fasta").read().split()
#print("Digest enzyme used: " + (digest_enzyme[0])[1:] ,digest_enzyme[1])

#create list of all amplicon files in the folder
filesInFolder = [f for f in listdir(amplicon_filepath) if isfile(join(amplicon_filepath, f))]

#sort the list of amplicons in reverse order if you want to
#filesInFolder.sort(reverse=True)
orderingsnumber = 0

#print info and create final sequence file
for file in filesInFolder:
    if ".fasta" in file:
        file_path = amplicon_filepath + "\\" + file
        for record in SeqIO.parse(file_path, "fasta"):
            orderingsnumber += 1
            fileName = file.replace(".fasta", "")
            amplicon_list.append(str(orderingsnumber) + ". " + fileName + ": " + str(len(record.seq)) + "bp" + ": " + record.description + ": " + record.seq)
            output_file += str(record.seq.upper())
            #print(fileName, len(record.seq))
    else:
        print(file,"is not a .fasta file.")
        continue

#Writing the files    
text_file = open(output_filepath, "w")
text_file.write(output_fileID + output_file)
text_file.close()

print("Final sequence written to", output_filepath)

with open(amplicon_list_outputpath, "w") as order_file:
    order_file.write("Ordernumber|QTRACE|Amplicon Size|ID|Sequence\n\n" + "Digest enzyme used: " + "\n"*2 )
    for item in amplicon_list:
        order_file.write("%s\n" % item)
    #order_file.write("%s\n"*2 % output_file)
order_file.close()

print("Amplicon list written to", amplicon_list_outputpath)

"""_______________FASTA format using BioPython______________________________________________________________________________________________________________________________________________
"""

#SeqIO.write(output_file, output_filename, "fasta")

#>>> record.id
#'gi|45478711|ref|NC_005816.1|'
#>>> record.name
#'gi|45478711|ref|NC_005816.1|'
#>>> record.description
#'gi|45478711|ref|NC_005816.1| Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1,
#complete sequence'