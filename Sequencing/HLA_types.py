import os
import pandas as pd

# For user input uncomment below and comment the hardcoded lines below
path = input("give folder: ")
filename = input("give filename: ")
path = os.path.realpath(os.path.join(path, filename))

# Read in the excel file into a pandas dataframe
file = pd.read_excel(path)

# Print all the column headers so the user can copy them from the terminal
print("\nHeaders: \n")
for header in file.columns.sort_values():
    print(header)
    # print(header, sep="")
    file[header] = file[header].dropna()
print()

# initialise variables
user_input = "never"
selection_list = []

# Get the desired markers from the user
while (user_input.lower() in ["yes", "y"]) == False:
    user_input = input("Select one of the headers above or type yes/y to start: ")
    # Break on user input
    if (user_input in selection_list):
        print("\nAlready selected. Want to stop? Then input yes/y\n")
        continue
    if (user_input.lower() in ["yes", "y"]) != False:
        break
    # Check user input for a valid option
    if user_input not in file.columns.values or user_input == "":
        print("\ninvalid option\n")
        continue
    selection_list.append(user_input)

# Stop if nothing was selected (sorta redudant)
if len(selection_list) < 1:
    print("Nothing was selected. exiting...")
    exit()

# return the list if only a single column was selected
if len(selection_list) == 1:
    print("Only a single header was selected")
    print("Concesus: \n", file[selection_list[0]].dropna(), sep="")
    exit()

header_list = selection_list.copy()
filter_list = []

# extract out all the values using the selected headers
for header in selection_list:
    filter_list.append(set(file[header].dropna()))

# Sort based on columns length
filter_list.sort(key=len)

# Get the smalles number which is always the first
smallest_set = filter_list.pop(0)

# Setup variables
consensus = [] 
filter_floats = True

# Find concensus among all the filter sets
for set in filter_list:
    smallest_set = smallest_set.intersection(set)

# Change consensus to list and setup to filter floats
consensus = list(smallest_set)
consensus.sort()
filtered_consensus = []

# filter any floats and cast them to int
if filter_floats:
    for dna in consensus:
        if type(dna) == float:
            dna = int(dna)
        filtered_consensus.append(dna)

# output the consensus to the user
print("\nselected markers = ", header_list)
print("consensus = ", filtered_consensus)
input("\n press any key to quit\n")
