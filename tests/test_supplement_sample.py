"""Source-value checks for supplementary spreadsheet export."""
import csv
from datetime import datetime
import importlib.util
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

spec = importlib.util.spec_from_file_location('supplement_sample', Path(__file__).resolve().parents[1] / 'scripts/extract_supplement_sample.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SupplementChecks(unittest.TestCase):
    def test_sequences_small_numbers_formulas_merges_and_original_row_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            source = directory / 'source.xlsx'
            book = Workbook()
            sheet = book.active
            sheet.title = 'Actual measurements'
            sheet.append(['Sequence', 'P value', 'Group'])
            sheet.append(['ACGTACGT', 1.2e-10, 'shared'])
            sheet.append(['00123', 0, None])
            sheet.merge_cells('C2:C3')
            sheet['B5'] = '=SUM(B2:B3)'
            sheet['A6'] = datetime(2025, 9, 15)
            book.save(source)
            original = source.read_bytes()
            result = module.parse_workbook(source, directory)[0]
            with (directory / result['complete_tsv']).open(newline='') as handle:
                rows = list(csv.reader(handle, delimiter='\t'))
            self.assertEqual(rows[0], ['source_row', 'A', 'B', 'C'])
            self.assertEqual(rows[2], ['2', 'ACGTACGT', '1.2e-10', 'shared'])
            self.assertEqual(rows[3], ['3', '00123', '0', ''])
            self.assertEqual(rows[4], ['5', '', '=SUM(B2:B3)', ''])
            self.assertEqual(rows[5], ['6', '2025-09-15T00:00:00', '', ''])
            self.assertEqual(result['merged_ranges'], ['C2:C3'])
            self.assertEqual(result['formula_cells'], 1)
            self.assertEqual(result['nonempty_rows'], 5)
            self.assertEqual(result['date_typed_cells'], 1)
            self.assertEqual(result['first_date_cells'][0]['coordinate'], 'A6')
            self.assertEqual(source.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
