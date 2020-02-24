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

    @property
    def up(self):
        return self._data['Marker->ARP Up Ecc. (m)']

    @up.setter
    def up(self, value):
        self._data['Marker->ARP Up Ecc. (m)'] = value

    @property
    def north(self):
        return self._data['Marker->ARP North Ecc(m)']

    @north.setter
    def north(self, value):
        self._data['Marker->ARP North Ecc(m)'] = value

    @property
    def east(self):
        return self._data['Marker->ARP East Ecc(m)']

    @east.setter
    def east(self, value):
        self._data['Marker->ARP East Ecc(m)'] = value

    @property
    def north_alignment(self):
        return self._data['Alignment from True N']

    @north_alignment.setter
    def north_alignment(self, value):
        self._data['Alignment from True N'] = value

    @property
    def radome_type(self):
        return self._data['Antenna Radome Type']

    @radome_type.setter
    def radome_type(self, value):
        if len(value) > 4:
            raise ValueError("Antenna Radome Type must be 4 characters long")
        self._data['Antenna Radome Type'] = value

    @property
    def radome_serial(self):
        return self._data['Radome Serial Number']

    @radome_serial.setter
    def radome_serial(self, value):
        self._data['Radome Serial Number'] = value

    @property
    def cable_type(self):
        return self._data['Antenna Cable Type']

    @cable_type.setter
    def cable_type(self, value):
        self._data['Antenna Cable Type'] = value

    @property
    def cable_length(self):
        return self._data['Antenna Cable Length']

    @cable_length.setter
    def cable_length(self, value):
        self._data['Antenna Cable Length'] = value


    @property
    def date_installed(self):
        return self._data['Date Installed']

    @date_installed.setter
    def date_installed(self, value):
        if not re.match(r'^\d{4}\-\d\d\-\d\d', value):
            raise ValueError("Date Installed must be of the format (CCYY-MM-DDThh:mmZ)")
        self._data['Date Installed'] = value

    @property
    def date_removed(self):
        return self._data['Date Removed']

    @date_removed.setter
    def date_removed(self, value):
        if not re.match(r'^\d{4}\-\d\d\-\d\d', value):
            raise ValueError("Date Removed must be of the format (CCYY-MM-DDThh:mmZ)")
        self._data['Date Removed'] = value

    @property
    def additional(self):
        return self._data['Additional Information']

    @additional.setter
    def additional(self, value):
        self._data['Additional Information'] = value


    def string(self):

        section_text = f"""
4.{self.subtitle}  Antenna Type             : {self.antenna_type}
     Serial Number            : {self.serial_number}
     Antenna Reference Point  : {self.antenna_reference}
     Marker->ARP Up Ecc. (m)  : {self.up}
     Marker->ARP North Ecc(m) : {self.north}
     Marker->ARP East Ecc(m)  : {self.east}
     Alignment from True N    : {self.north_alignment}
     Antenna Radome Type      : {self.radome_type}
     Radome Serial Number     : {self.radome_serial}
     Antenna Cable Type       : {self.cable_type}
     Antenna Cable Length     : {self.cable_length}
     Date Installed           : {self.date_installed}
     Date Removed             : {self.date_removed}
     Additional Information   : {self.additional}
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
