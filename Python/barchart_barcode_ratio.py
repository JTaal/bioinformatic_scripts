import matplotlib.pyplot as plt
import pandas as pd

# Set path and read file into a pandas dataframe
path = r"D:\NanoTYPE\220923_4_samples_Omixon\no_sample\20220923_1652_MN21782_FAT58898_bbcc535b\sequencing_summary_FAT58898_6bd5d597.txt"

class summary_parser:
    def __init__(self, path, sep='\t', low_memory=False):
        self.path=path
        self.data=pd.read_table(path, sep=sep, low_memory=low_memory)
    
    def print_headers(self):
        """
        Prints all the headers in the terminal
        """
        print("\nAll the headers:\n")
        for line in self.data:
            print(line)
        print("\n")

    def barcode_ratio_parser(self, MINRATIO = 0.00000001, MINREADS = 5000):
        """
        This parser uses self.data to a sequencing_summary and exports the x, y data
        """
        # fetch the data
        data = self.data
        
        # Setup variables
        barcode_counts = {}
        barcode_ratios = {}
        barcode_status = data[["barcode_arrangement", "filename_fastq"]].values
        barcode_names = data["barcode_arrangement"].unique()

        # initialise the dict with appropriate structure
        for barcode in barcode_names:
            barcode_counts.update({barcode:[{"pass":0},{"fail":0}]})

        # populate dict with counts of failures and passes
        for line in barcode_status:
            barcode = line[0]

            if "fail" in line[1]:
                barcode_counts[barcode][1]["fail"] += 1

            else:
                barcode_counts[barcode][0]["pass"] += 1

        # calculate the ratio and filter based on reads
        for barcode in barcode_counts:
            passed = barcode_counts[barcode][0]["pass"]
            failed = barcode_counts[barcode][1]["fail"]

            total = passed + failed
            passed_ratio = passed/total
            # passed_percentage = passed_ratio * 100

            if total < MINREADS:
                continue

            # barcode_ratios.update({barcode:passed_percentage})
            barcode_ratios.update({barcode:passed_ratio})

        # filter values based on their ratio
        for barcode in barcode_ratios.copy():
            if barcode_ratios[barcode] > MINRATIO:
                continue
            del barcode_ratios[barcode]

        # remove unwanted data
        del barcode_ratios['-']

        # Format dict to useable data
        data_list = sorted(barcode_ratios.items())
        x, y = zip(*data_list)

        return x, y

parser = summary_parser(path, sep='\t')

# Print headers
# parser.print_headers()

x, y = parser.barcode_ratio_parser()

# Create plot
plt.xticks(rotation=45, ha="right")
plt.bar(x, y)
plt.ylabel("Percentage usable reads")
plt.show()