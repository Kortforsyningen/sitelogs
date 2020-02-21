import re

from sitelog.sections import (
    SubSection,
    SectionList,
)

class AntennaType(SubSection):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()

    def _template_dict(self):
        data = {
            "Antenna Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Serial Number": "(A*, but note the first A5 is used in SINEX)",
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
        return data

    @property
    def antenna_type(self):
        return self._data['Antenna Type']

    @antenna_type.setter
    def antenna_type(self, value):
        self._data['Antenna Type'] = value

    @property
    def serial_number(self):
        return self._data['Serial Number']

    @serial_number.setter
    def serial_number(self, value):
        self._data['Serial Number'] = value

    @property
    def antenna_reference(self):
        return self._data['Antenna Reference Point']

    @antenna_reference.setter
    def antenna_reference(self, value):
        self._data['Serial Number'] = value

    def string(self):

        section_text = f"""
4.{self.subtitle}  Antenna Type             : {self.antenna_type}
     Serial Number            : {self.serial_number}
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
        return section_text

class Antenna(SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = AntennaType
        self.section_type = 'subsectionheader'


    def _template_dict(self):
        data = {
            "Antenna Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Serial Number": "(A*, but note the first A5 is used in SINEX)",
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
        return data

    def string(self):

        section_text = f"""
4.   GNSS Antenna Information
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string()
        else:
            s = AntennaType()
            s.subtitle = 'x'
            section_text += s.string()
        return section_text
