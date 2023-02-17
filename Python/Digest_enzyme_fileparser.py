from fileinput import close
from genericpath import isfile
from os import listdir
from os.path import isfile, join

#NO SPACES ALLOWED INSIDE THE NAMES! 
#THE PROGRAM SEPERATES THE DOCUMENTS BASED ON SPACES



#inputpath = input("Give folder:")
inputpath = input("give folder:")

#inputname of the document
inputname = input("give file name:") + ".txt"

#setting up all directory variables
extension = ".fasta"


def DigestSplitter(inputpath, inputname, extension):
    #create list of all files in the folder
    filesInFolder = [f for f in listdir(inputpath) if isfile(join(inputpath, f))]

    #split join and write enzyme into new fasta file
    for file in filesInFolder:
        if file == inputname:
            enzymes = open(inputpath + "\\"+ file).read().split()
            print(enzymes)
            while len(enzymes) >= 2:
                print(enzymes[0], "name")
                filename = ">" + enzymes.pop(0)
                print(enzymes[0], "sequence")
                sequence = enzymes.pop(0)
                new_file = open(inputpath + "\\" + filename[1:] + extension, "w")
                new_file.write(filename + "\n" + sequence)
                close()

DigestSplitter(inputpath, inputname, extension)


#for file in filesInFolder:
#    if file == inputname:
#        enzymes = open(inputpath + "\\"+ file).read().split()
#        for item in enzymes:
#            print(item[1:])
#            if ">" in item:
#                filename = ">" + item
#                new_file = inputpath + "\\" + item[1:] + extension
#                continue
#            else:
#                sequence = item
#                new_file = open(new_file, "w")
#                new_file.write(filename + "\n" + sequence)
#                close()