bron = "12345"

print(bron[len(bron)-3:])

from os import listdir
from extensions import changeExtensions

changeExtensions(r"C:\Users\Jasper\Desktop\Amplicon FASTAS\Digestion sites\Alator Bioscience", ".fasta", ".txt")