from pdfminer.high_level import extract_text
from erp_aero_test_task.pdf_page import extract_matches, create_dict, fill_dict


def pdf_to_dict(path):
    text = extract_text(path)
    matches = extract_matches(text, r'.+:[\s]*.+')
    data_dict = create_dict('ORG')
    fill_dict(matches, data_dict)
    return data_dict
