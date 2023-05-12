from controls import parser
from erp_aero_test_task import pdf_page


def test_pdf_comparison(pdf_path):
    # WHEN
    data = parser.pdf_to_dict(pdf_path)

    # THEN
    pdf_page.check_keys(data)
    pdf_page.verify_barcodes(pdf_path, data)
    pdf_page.pdf_structure_is_valid(pdf_path)
