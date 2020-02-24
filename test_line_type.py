import unittest

from sitelog import (
    _determine_line_type,
    SiteIdentification,
    Section,
    SectionList,
    AntennaType,
    Antenna,
)

class TestLineType(unittest.TestCase):

    def test_line_type(self):
        line = '4.x  Antenna Type             : (A20, from rcvr_ant.tab; see instructions)'
        line_type = 'subsectionheader'
        self.assertEqual(_determine_line_type(line), line_type)

    def test_site_code(self):
        code = 'AB346'
        code2 = 'AB'
        site = SiteIdentification()
        with self.assertRaises(ValueError):
            site.site_code = code
            site.site_code = code2

    def test_IERS(self):
        code = 'AB346'
        site = SiteIdentification()
        with self.assertRaises(ValueError):
            site.IERS_number = code

    def test_bedrock(self):
        site = SiteIdentification()
        with self.assertRaises(ValueError):
            site.bedrock_type = 'ROCK'

    def test_read_lines_subsec(self):
        sec = Section()
        lines = ['4.x  Antenna Type             : Leica', '     Serial Number            : 1111122']
        _data = {
            'Antenna Type': 'Leica',
            'Serial Number': '1111122'
        }
        subtitle = '4.x'
        sec.read_lines(lines)
        self.assertEqual(sec._data, _data)
        self.assertEqual(subtitle, sec.subtitle)

    def test_read_lines_subsubsec(self):
        sec = Section()
        lines = ['4.3.x  Antenna Type             : Leica', '     Serial Number            : 1111122']
        _data = {
            'Antenna Type': 'Leica',
            'Serial Number': '1111122'
        }
        subtitle = '3.'
        title = '  Antenna Type             :'
        sec.read_lines(lines)
        self.assertEqual(sec._data, _data)
        self.assertEqual(subtitle, sec.subtitle)
        self.assertEqual(title, sec.title)

    def test_read_lines_list(self): #
        list_sec = SectionList()

        lines = ['4.3  Antenna Type             : Leica', '     Serial Number            : 1111122']
        _data = {
            "Antenna Type": "Leica",
            "Serial Number": "1111122",
            "Antenna Reference Point": "(BPA/BCR/XXX from \"antenna.gra\"; see instr.)",
            "Marker->ARP Up Ecc. (m)": "(F8.4)",
            "Marker->ARP North Ecc(m)": "(F8.4)",
            "Marker->ARP East Ecc(m)": "(F8.4)",
            "Alignment from True N": "(deg; + is clockwise/east)",
            "Antenna Radome Type": "(A4 from rcvr_ant.tab; see instructions)",
            "Radome Serial Number": "",
            "Antenna Cable Type": "(vendor & type number)",
            "Antenna Cable Length": "(m)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Date Removed": "(CCYY-MM-DDThh:mmZ)",
            "Additional Information": "(multiple lines)",
        }
        subtitle = '4.3'
        list_sec.subsection_type = AntennaType
        list_sec.section_type = 'subsectionheader'
        list_sec.read_lines(lines)
        list_sub_sec =  list_sec._subsections[0]
        self.assertEqual( _data, list_sub_sec._data)
        self.assertEqual(subtitle, list_sub_sec.subtitle)

    def test_antenna(self): #
        antenna_sec = Antenna()

        lines = ['4.3  Antenna Type             : Leica', '     Serial Number            : 1111122']
        antenna_text = """\n4.   GNSS Antenna Information\n\n4.1  Antenna Type             : Leica\n     Serial Number            : 1111122\n     Antenna Reference Point  : (BPA/BCR/XXX from "antenna.gra"; see instr.)\n     Marker->ARP Up Ecc. (m)  : (F8.4)\n     Marker->ARP North Ecc(m) : (F8.4)\n     Marker->ARP East Ecc(m)  : (F8.4)\n     Alignment from True N    : (deg; + is clockwise/east)\n     Antenna Radome Type      : (A4 from rcvr_ant.tab; see instructions)\n     Radome Serial Number     :\n     Antenna Cable Type       : (vendor & type number)\n     Antenna Cable Length     : (m)\n     Date Installed           : (CCYY-MM-DDThh:mmZ)\n     Date Removed             : (CCYY-MM-DDThh:mmZ)\n     Additional Information   : (multiple lines)\n"""

        antenna_sec.read_lines(lines)

        self.assertEqual(antenna_text, antenna_sec.string())

    



if __name__ == '__main__':
    unittest.main()