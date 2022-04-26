from genericpath import isfile
from os import listdir
from os.path import isfile, join
from Bio import SeqIO

#inputpath = input("Give folder:")
inputpath = r"C:\Users\Jasper\Desktop\Amplicon FASTAS"

#setting up all directory variables
output_file = ""
output_filename = "Insertion sequence.fasta"
output_fileID = ">Insertion sequence\n"
output_filepath = inputpath + "\\" + output_filename

amplicon_list = []
amplicon_listname = "List of amplicon order.txt"
amplicon_listpath = inputpath + "\\" + amplicon_listname

#create list of all files in the folder
filesInFolder = [f for f in listdir(inputpath) if isfile(join(inputpath, f))]

#print info and create final file
for file in filesInFolder:
    if ".fasta" in file:
        file_path = inputpath + "\\" + file
        for record in SeqIO.parse(file_path, "fasta"):
            fileName = file.replace(".fasta", "")
            amplicon_list.append(fileName)
            output_file += str(record.seq)
            
            
            print(fileName, len(record.seq))
            
            
    else:
        print(file,"is not a .fasta file.")
        continue

#open text file

#if output_filename in filesInFolder:
#    print("File already exist in directory")
#    print("")
#    answer = input("Do you want to continue and overwrite the file? (y/n) :")
#    if answer == "y":
#        skip
#    elif answer == "n":
#        "Exiting..."
#        exit()
#    else:
#        print("invalid answer. Exiting...")
#        exit()

#Writing the files    
text_file = open(output_filepath, "w")
text_file.write(output_fileID + output_file)
text_file.close()

with open(amplicon_listpath, "w") as order_file:
    for item in amplicon_list:
        order_file.write("%s " % item)
        
    order_file.write("%s\n" % "%s\n" % output_file)
order_file.close()

#SeqIO.write(output_file, output_filename, "fasta")

#>>> record.id
#'gi|45478711|ref|NC_005816.1|'
#>>> record.name
#'gi|45478711|ref|NC_005816.1|'
#>>> record.description
#'gi|45478711|ref|NC_005816.1| Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1,
#complete sequence'