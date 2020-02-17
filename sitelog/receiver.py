import re

from sitelog.sections import (
        SubSection,
        SectionList,
)

class GnssReceiver(SubSection):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
#        self.subtitle = []
#        self.title = '' 
        self.number = None
 #       self._data['Receiver Type'] = receiver_type

    def _template_dict(self):
        data = {
            "Receiver Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Satellite System": "(GPS+GLO+GAL+BDS+QZSS+SBAS)",
            "Serial Number": "(A20, but note the first A5 is used in SINEX)",
            "Firmware Version": "(A11)",
            "Elevation Cutoff Setting": "(deg)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Date Removed": "(CCYY-MM-DDThh:mmZ)",
            "Temperature Stabiliz.": "(none or tolerance in degrees C)",
            "Additional Information": "(multiple lines)",
        }
        return data


    @property
    def receiver_type(self):
        return self._data['Receiver Type']

    @receiver_type.setter
    def receiver_type(self, value):
        self._data['Receiver Type'] = value

    @property
    def sat_sys(self):
        return self._data['Satellite System']

    @sat_sys.setter
    def sat_sys(self, value):
        self._data['Satellite System'] = value


    @property
    def firmware(self):
        return self._data['Firmware Version']

    @firmware.setter
    def firmware(self, value):
        self._data['Firmware Version'] = value

    @property
    def cutoff(self):
        return self._data['Elevation Cutoff Setting']

    @cutoff.setter
    def cutoff(self, value):
        self._data['Elevation Cutoff Settingn'] = value

    @property
    def additional(self):
        return self._data['Additional Information']

    @additional.setter
    def additional(self, value):
        self._data['Additional Information'] = value

    def string(self):

        section_text = f"""
3.{self.title}  Receiver Type            : {self.receiver_type}
     Satellite System         : {self.sat_sys}
     Serial Number            : (A20, but note the first A5 is used in SINEX)
     Firmware Version         : {self.firmware}
     Elevation Cutoff Setting : {self.cutoff}
     Date Installed           : (CCYY-MM-DDThh:mmZ)
     Date Removed             : (CCYY-MM-DDThh:mmZ)
     Temperature Stabiliz.    : (none or tolerance in degrees C)
     Additional Information   : {self.additional}

"""
        return section_text

class GNSS(SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict
        self.subsection_type = GnssReceiver
        self.section_type = 'subsectionheader' #subsection 

    def _template_dict(self):
        data = {
            "Receiver Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Satellite System": "(GPS+GLO+GAL+BDS+QZSS+SBAS)",
            "Serial Number": "(A20, but note the first A5 is used in SINEX)",
            "Firmware Version": "(A11)",
            "Elevation Cutoff Setting": "(deg)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Date Removed": "(CCYY-MM-DDThh:mmZ)",
            "Temperature Stabiliz.": "(none or tolerance in degrees C)",
            "Additional Information": "(multiple lines)",
        }
        return data


    def string(self):

        section_text = f"""
3.   GNSS Receiver Information
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string() 
        else:
            s = GnssReceiver()
            s.title = 'x'
            section_text += s.string()
        return section_text
