import re
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator


def check_keys(dictionary):
    keys_list = dictionary.keys()
    for key in keys_list:
        assert key in keys_list, f'Error: Key "{key}" not found'
    return keys_list


def create_dict(org_name):
    value = extract_org_name
    dictionary = {org_name: value}
    dictionary.pop(org_name)
    return dictionary


def decode_barcodes(path):
    images_from_pdf = convert_from_path(path)
    for image in images_from_pdf:
        decoded = decode(image)
        barcodes = []
        for d in decoded:
            barcode = d.data.decode('utf-8')
            barcodes.append(barcode)
        return barcodes


def extract_matches(text, regex):
    pattern = re.compile(regex)
    matches = pattern.findall(text)
    for i in range(len(matches)):
        if 'REMARK' in matches[i]:
            matches[i:i + 1] = matches[i].split('\n\n')
    return matches


def extract_org_name(text):
    name = text.split('\n')[0]
    return name


def fill_dict(matches, dictionary):
    for e in matches:
        split_element = e.split(':')
        key = split_element[0].strip()
        value = split_element[1].strip()
        dictionary[key] = value


def pdf_structure_is_valid(path):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(path, 'rb') as f:
        pages = list(PDFPage.get_pages(f))
        for i, page in enumerate(pages):
            interpreter.process_page(page)
            layout = device.get_result()

            element_coordinates = {}
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    x, y = element.x0, element.y1
                    text = element.get_text().strip()
                    element_coordinates[text] = (x, y)

            for key, expected_coord in element_coordinates.items():
                if key in element_coordinates:
                    x, y = element_coordinates[key]
                    if abs(x - expected_coord[0]) > 1 or abs(y - expected_coord[1]) > 1:
                        return False
                else:
                    return False


def verify_barcodes(path, dictionary):
    values_list = dictionary.values()
    barcode_values = decode_barcodes(path)
    for value in barcode_values:
        assert value in values_list, f'Error: Barcode {value} is not found'
