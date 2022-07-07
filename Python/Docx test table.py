from docxtpl import DocxTemplate

tpl=DocxTemplate(r'D:\Dropbox(JETA)\JETA Team Folder\JETA\02 Research & Development\Jasper\Test\test table.docx')

context = {
    'col_labels' : ['fruit', 'vegetable', 'stone', 'thing'],
    'tbl_contents': [
        {'label': 'yellow', 'cols': ['banana', 'capsicum', 'pyrite', 'taxi']},
        {'label': 'red', 'cols': ['apple', 'tomato', 'cinnabar', 'doubledecker']},
        {'label': 'green', 'cols': ['guava', 'cucumber', 'aventurine', 'card']},
        ]
}

tpl.render(context)
tpl.save(r'D:\Dropbox (JETA)\JETA Team Folder\JETA\02 Research & Development\Jasper\Test\test table 1.docx')