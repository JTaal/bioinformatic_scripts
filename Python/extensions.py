import os
from os import listdir
from os.path import isfile, join

def changeExtensions(inputPath, new_extension, old_extension):
    if os.path.isdir(inputPath):
        inputPath += "\\"
        filesInFolder = [f for f in listdir(inputPath) if isfile(join(inputPath, f))]
        for file in filesInFolder:
            if new_extension in file:
                print(file," skipped")
                continue
            elif old_extension in file:
                old_name = inputPath+file
                new_name = os.path.splitext(inputPath+file)[0]+ new_extension
                os.rename(old_name, new_name)
    else:
        print("")
        print("Directory not found")
        print("")
        return False
    
#changeExtensions(r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\01 pJETA101\Amplicon FASTAS\Amplicon sequences", ".fasta", ".txt")