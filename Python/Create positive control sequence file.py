from genericpath import isfile
from os import listdir
from os.path import isfile, join
from Bio import SeqIO
#from Bio.Seq import MutableSeq, Seq

"""_______________Input_____________________________________________________________________________________________________________________________________________
"""
#paths
#inputpath = input("Give folder:")
amplicon_filepath = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Amplicon sequences"
controls_filepath = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Control sequences"
digest_enzyme_filepath = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Digestion sites\Fermentas"
output_path = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Final sequence"

#enzyme names
enzyme_name_main = "XhoI" 
enzyme_name_5_prime = "ApaI"
enzyme_name_3_prime = "SmaI"
primer_sequence_5_prime = "CACCATTGGCAATGAGCGGTTC"
primer_sequence_3_prime = "ACGTGGACATCCGCAAAGACCT"
"""_______________Code______________________________________________________________________________________________________________________________________________
"""

#setting up all directory variables
output_file = ""
output_filename = "Insertion sequence " + enzyme_name_main +".fasta"
output_fileID = ">Insertion sequence "+ enzyme_name_main + "\n"
output_filepath = output_path + "\\" + output_filename

amplicon_list = []
amplicon_listname = "List of amplicon order " + enzyme_name_main + ".txt"
amplicon_list_outputpath = output_path + "\\" + amplicon_listname

#extract digest enzyme sequences
dictionary_enzymes = {"enzyme_main": enzyme_name_main , "enzyme_5_prime": enzyme_name_5_prime, "enzyme_3_prime": enzyme_name_3_prime}
list_enzymes = list(dictionary_enzymes.keys())

for key in dictionary_enzymes:
    temp_enzymeholder = open(digest_enzyme_filepath + "\\" + dictionary_enzymes.get(key) + ".fasta").read().split()
    dictionary_enzymes[key] = [dictionary_enzymes.get(key), temp_enzymeholder[1]]
    print("Digest enzyme used: " + str(dictionary_enzymes.get(key)))
    
    
#digestions site sequences added into easy to read variables
enzyme_main_sequence = dictionary_enzymes.get("enzyme_main")[1]
enzyme_5_prime_sequence = dictionary_enzymes.get("enzyme_5_prime")[1]
enzyme_3_prime_sequence = dictionary_enzymes.get("enzyme_3_prime")[1]

#create list of all amplicon files in the folder
filesInFolder = [f for f in listdir(amplicon_filepath) if isfile(join(amplicon_filepath, f))]

#sort the list of amplicons in reverse order if you want to
#filesInFolder.sort(reverse=True)
control_ACE = SeqIO.read(controls_filepath + "\\ACE.fasta", "fasta").upper()
control_RNaseP = SeqIO.read(controls_filepath + "\\RNaseP Celera & KDX.fasta", "fasta").upper()

#add 5' tail as unique digestion site/ACE/RNase
head_5_prime_insert = enzyme_5_prime_sequence + primer_sequence_5_prime + enzyme_main_sequence + control_ACE.seq + control_RNaseP.seq 
output_file += head_5_prime_insert

#create orderingsnumber variable
orderingsnumber = 0

#print info and create final sequence file and fill amplicon_list
for filename in filesInFolder:
    if ".fasta" in filename:
        file_path = amplicon_filepath + "\\" + filename
        for record in SeqIO.parse(file_path, "fasta"):
            orderingsnumber += 1
            filename_only = filename.replace(".fasta", "")
            amplicon_list.append(str(orderingsnumber) + ". " + filename_only + ": " + str(len(record.seq)) + "bp" + ": " + record.description + ": " + record.seq)
            output_file += enzyme_main_sequence.upper()
            output_file += str(record.seq.upper())
    else:
        print(filename,"is not a .fasta file.")
        continue

print(output_file)

#The loop doesn't insert a digestionsite after an amplicon so the main digest has to be added at the tail
#add 3' tail as RNase/ACE/unique digestion site
tail_3_prime_insert = enzyme_main_sequence + control_RNaseP.seq + control_ACE.seq + enzyme_main_sequence + primer_sequence_3_prime + enzyme_3_prime_sequence 
output_file += tail_3_prime_insert
#mutable_fasta_sequence = MutableSeq(output_file)
#fasta_sequence = Seq(output_file)

#Writing the files    
text_file = open(output_filepath, "w")
text_file.write(output_fileID + str(output_file))
text_file.close()

print("Final sequence written to", output_filepath)

with open(amplicon_list_outputpath, "w") as order_file:
    order_file.write("Ordernumber|QTRACE|Amplicon Size|ID|Sequence\n\n")
    order_file.write("Main digest enzyme used: " + dictionary_enzymes.get("enzyme_main")[0] + " Sequence: " + dictionary_enzymes.get("enzyme_main")[1] + "\n")
    order_file.write("5' digest enzyme used: " + dictionary_enzymes.get("enzyme_5_prime")[0] + " Sequence: " + dictionary_enzymes.get("enzyme_5_prime")[1] + "\n")
    order_file.write("3' digest enzyme used: " + dictionary_enzymes.get("enzyme_3_prime")[0] + " Sequence: " + dictionary_enzymes.get("enzyme_3_prime")[1] + "\n\n")    
    for item in amplicon_list:
        order_file.write("%s\n" % item)
order_file.close()

print("Amplicon list written to", amplicon_list_outputpath)

"""_______________FASTA format using BioPython______________________________________________________________________________________________________________________________________________
"""

#Website
#http://biopython.org/DIST/docs/tutorial/Tutorial.pdf

#SeqIO.write(output_file, output_filename, "fasta")

#>>> record.id
#'gi|45478711|ref|NC_005816.1|'
#>>> record.name
#'gi|45478711|ref|NC_005816.1|'
#>>> record.description
#'gi|45478711|ref|NC_005816.1| Yersinia pestis biovar Microtus str. 91001 plasmid pPCP1,
#complete sequence'