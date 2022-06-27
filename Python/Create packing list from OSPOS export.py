import datetime
import pandas as pd
import sys
from docxtpl import DocxTemplate

#Setting up directories
base_dir = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\Jasper\Auto packing lists"
word_template_path = base_dir + "\\" + "Mother-packing-list.docx"
excel_path = base_dir + "\\" + "Packing list creator.xlsx"
inventory_path = base_dir + "\\" +"Physical inventory"
output_dir = base_dir + "\\" + "Output"

#Manual input information
customer_name = "bionobis"

today_text = str(datetime.datetime.today()) 
# output = 2022-06-20 11:02:26.384404
today_text = f"{datetime.datetime.now():%Y-%m-%d}"
# output = 2022-06-20
today = today_text[2:4] + today_text[5:7] + today_text[8:10]


doc = DocxTemplate(word_template_path)

order_items = pd.read_excel(excel_path, sheet_name="Sheet1")
customer_info = pd.read_excel(excel_path, sheet_name="Customer info")


item_dic = order_items.to_dict(orient="records")
customer_dic = customer_info.to_dict(orient="records",)
customer_dic_names = customer_info.to_dict(orient="list")
#customer_dic = customer_dic[0]

#checks whether the given customer name is in the excel sheet
if customer_name in customer_dic_names.get("name"):
    print("\nCustomer name found!\n")
else:
    print("\nThe customer name you've given is not in the database.")
    print("Exiting script.......\n")
    sys.exit()

    
doc.render(customer_dic)
doc.save(base_dir + "\\" + today + " Packing list"  + ".docx")   

#for record in order_items.to_dict(orient="records"):
#    print(record)