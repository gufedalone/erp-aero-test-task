from controls import parser
from erp_aero_test_task import pdf_page
from utils.paths import resource


def test_pdf_comparison():
    # GIVEN
    path = resource('test_task.pdf')

    # WHEN
    data = parser.pdf_to_dict(path)

    # THEN
    pdf_page.check_keys(data)
    pdf_page.verify_barcodes(path, data)
    pdf_page.pdf_structure_is_valid(path)

