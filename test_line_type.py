import unittest

from sitelog import (
    _determine_line_type,
    _format_string,
    SiteIdentification,
    Section,
    SectionList,
    AntennaType,
    Antenna,
    MetInstrument,
    Meteorological,
    SensorType,
)


class TestLineType(unittest.TestCase):
    def test_line_type(self):
        line = (
            "4.x  Antenna Type             : (A20, from rcvr_ant.tab; see instructions)"
        )
        line_type = "subsectionheader"
        self.assertEqual(_determine_line_type(line), line_type)

    def test_site_code(self):
        code = "AB346"
        code2 = "AB"
        site = SiteIdentification()
        with self.assertRaises(ValueError):
            site.site_code = code
            site.site_code = code2

    def test_IERS(self):
        code = "AB346"
        site = SiteIdentification()
        with self.assertRaises(ValueError):
            site.IERS_number = code

    def test_bedrock(self):
        site = SiteIdentification()
        with self.assertRaises(ValueError):
            site.bedrock_type = "ROCK"

    def test_read_lines_subsec(self):
        sec = Section()
        lines = [
            "4.x  Antenna Type             : Leica",
            "     Serial Number            : 1111122",
        ]
        _data = {"Antenna Type": "Leica", "Serial Number": "1111122"}
        subtitle = "4.x"
        sec.read_lines(lines)
        self.assertEqual(sec._data, _data)
        self.assertEqual(subtitle, sec.subtitle)

    def test_read_lines_subsubsec(self):
        sec = Section()
        lines = [
            "4.3.x  Antenna Type             : Leica",
            "     Serial Number            : 1111122",
        ]
        _data = {"Model": "Leica", "Serial Number": "1111122"}
        subtitle = "3."
        title = "Antenna Type"
        sec.read_lines(lines)
        self.assertEqual(sec._data, _data)
        self.assertEqual(subtitle, sec.subtitle)
        self.assertEqual(title, sec.title)

    def test_read_lines_list(self):  #
        list_sec = SectionList()

        lines = [
            "4.3  Antenna Type             : Leica",
            "     Serial Number            : 1111122",
        ]
        _data = {
            "Antenna Type": "Leica",
            "Serial Number": "1111122",
            "Antenna Reference Point": '(BPA/BCR/XXX from "antenna.gra"; see instr.)',
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
        subtitle = 1
        list_sec.subsection_type = AntennaType
        list_sec.section_type = "subsectionheader"
        list_sec.read_lines(lines)
        list_sub_sec = list_sec._subsections[0]
        self.assertEqual(_data, list_sub_sec._data)
        self.assertEqual(subtitle, list_sub_sec.subtitle)

    def test_antenna(self):  #
        antenna_sec = Antenna()

        lines = [
            "4.3  Antenna Type             : Leica",
            "     Serial Number            : 1111122",
        ]

        # Note the whitespace after "Radome Serial Number", can be a problem in
        # editors that automatically removes trailing whitespace
        antenna_text = """
4.   GNSS Antenna Information

4.1  Antenna Type             : Leica
     Serial Number            : 1111122
     Antenna Reference Point  : (BPA/BCR/XXX from "antenna.gra"; see instr.)
     Marker->ARP Up Ecc. (m)  : (F8.4)
     Marker->ARP North Ecc(m) : (F8.4)
     Marker->ARP East Ecc(m)  : (F8.4)
     Alignment from True N    : (deg; + is clockwise/east)
     Antenna Radome Type      : (A4 from rcvr_ant.tab; see instructions)
     Radome Serial Number     : 
     Antenna Cable Type       : (vendor & type number)
     Antenna Cable Length     : (m)
     Date Installed           : (CCYY-MM-DDThh:mmZ)
     Date Removed             : (CCYY-MM-DDThh:mmZ)
     Additional Information   : (multiple lines)
"""

        antenna_sec.read_lines(lines)
        self.assertEqual(antenna_text, antenna_sec.string())

    def test_format_string(self):
        line = "If an antenna has a cover which is integral and not ordinarily removable by the user, it is considered part of the antenna and NONE is to be used for the radome code."
        line_type = "multilinevalue"
        multiline = "If an antenna has a cover which is integral and\n                              : not ordinarily removable by the user, it is\n                              : considered part of the antenna and NONE is to be\n                              : used for the radome code."
        self.assertEqual(multiline, _format_string(line, line_type))

    def test_meteorological(self):
        """
        Writing a Meteorological Instrumentation from existing sitelog.
        Organising subsection
        """
        met_sec = Meteorological()

        lines = [
            "8.2.2  Pressure Sensor Model             : Pres. Sens.",
            "       Serial Number            : 1111122",
        ]

        met_text = """
8.   Meteorological Instrumentation

8.2.1 Pressure Sensor Model   : Pres. Sens.
       Manufacturer           : 
       Serial Number          : 1111122
       Data Sampling Interval : (sec)
       Accuracy               : 
       Height Diff to Ant     : (m)
       Calibration date       : (CCYY-MM-DD)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
"""

        met_sec.read_lines(lines)
        self.assertEqual(met_text, met_sec.string())

    def test_meteorological_new(self):
        meteorological = Meteorological()
        meteorological[0] = MetInstrument()
        meteorological[0].instrument = SensorType.PRESSURE
        meteorological[0].model = "Pres. Sens."
        meteorological[0].serial_number = "1111122"

        met_text = """
8.   Meteorological Instrumentation

8.2.1 Pressure Sensor Model   : Pres. Sens.
       Manufacturer           : 
       Serial Number          : 1111122
       Data Sampling Interval : (sec)
       Accuracy               : 
       Height Diff to Ant     : (m)
       Calibration date       : (CCYY-MM-DD)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
"""

        self.assertEqual(met_text, meteorological.string())


if __name__ == "__main__":
    unittest.main()
