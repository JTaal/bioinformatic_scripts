from os import makedirs
from pathlib import Path
from barcode import EAN13
from docxtpl import DocxTemplate, InlineImage
from barcode.writer import ImageWriter
from docx.shared import Mm
import pandas as pd

def create_barcode(number_string):
    base_dir = Path(__file__).parent / "barcodes"
    makedirs(base_dir, exist_ok=True)
    barcode = EAN13(number_string, writer=ImageWriter())
    barcode.save(base_dir/number_string)
    number_filename = number_string + ".png"
    return str(base_dir/number_filename)

word_path = r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\Jasper\Programming\JETA-Molecular-scripts\Python\required files\Test.docx"
word = DocxTemplate(word_path)

def create_table(Pathway, customername):   
    row = {}
    tbl_contents = []
    
    order_df = pd.read_excel(Pathway, sheet_name="order")
    order_list = order_df.to_dict(orient="records")
    
    if customername.lower() == "turku":
        turku = "Build in turkus requirements here"    
    else:
        for record in order_list:
            row["cols"] = [InlineImage(word, create_barcode(str(record["Barcode"])), 
                            width=Mm(30), height=Mm(13.2)), record["REF"], 
                            record["Name"], 
                            record["Description"], 
                            record["Category"], 
                            record["LOT"], 
                            record["Expiration date"], 
                            record["Qty"].split("[")[0], 
                            record["Qty"].split("[")[0], 
                            "0"
                            ]
            tbl_contents.append(row.copy())
        col_labels = ["Barcode", "REF", "Name", "Description", "Unit", "Lot No.", "Expiry date", "Quantity Ordered", "Quantity Shipped", "Back-order"]
        
    context = {"col_labels" : col_labels, "tbl_contents": tbl_contents}
    return context

word.render(context)
word.save(r"D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\Jasper\Programming\JETA-Molecular-scripts\Python\required files\blablabla.docx")