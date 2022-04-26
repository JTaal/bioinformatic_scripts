import sys
import glob
import fasta

for i in glob.glob(input("give pathway") + ".fasta"):
  print(i)

filepattern = ".fasta"
output = open(sys.argv[2], 'w')

#initialize lists
names = []
seqs = []

#glob.glob returns a list of files that match the pattern
for file in glob.glob(filepattern):
    #we read the contents and an instance of the class is returned
    contents = fasta.read_fasta(open(file).readlines())
    #a file can contain more than one sequence so we read them in a loop
    for item in contents:
        names.append(item.name)
        seqs.append(item.sequence)

#we print the output
for i in range(len(names)):
    output.write(names[i] + '\n' + seqs[i] + '\n\n')

output.close()

fasta.FASTA.read(file)