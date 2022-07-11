from os import makedirs
from pathlib import Path
from barcode import EAN13
from barcode.writer import ImageWriter
import pandas as pd




def create_barcode(number_string):   
    base_dir = Path(__file__).parent / "barcodes"
    makedirs(base_dir, exist_ok=True)
    barcode = EAN13(number_string, writer=ImageWriter(format="PNG"))
    return barcode.save(base_dir/number_string)


create_barcode("5454354354353254")