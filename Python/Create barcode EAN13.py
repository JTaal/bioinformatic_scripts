import os
import datetime
from random import random
import PySimpleGUI as sg
import pandas as pd
from time import time
from os import makedirs
from pathlib import Path
from barcode import EAN13
from barcode.writer import ImageWriter
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


def create_barcode(number_string):   
    base_dir = Path(__file__).parent / "barcodes"
    makedirs(base_dir, exist_ok=True)
    barcode = EAN13(number_string, writer=ImageWriter())
    return barcode.save(base_dir/number_string)



create_barcode("")