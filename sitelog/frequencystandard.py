import sitelog.sitelogger as sitelogger
import re

class Frequency(sitelogger.SubSection):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.number = None

    def _template_dict(self):
        data = {
            "Standard Type": "(INTERNAL or EXTERNAL H-MASER/CESIUM/etc)",
            "Input Frequency": "(if external)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    def string(self):

        section_text = f"""
6.{self.title}  Standard Type            : (INTERNAL or EXTERNAL H-MASER/CESIUM/etc)
       Input Frequency        : (if external)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
"""
        return section_text

class FrequencyStandard(sitelogger.SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = Frequency
        self.section_type = 'subsectionheader'


    def _template_dict(self):
        data = {
            "Standard Type": "(INTERNAL or EXTERNAL H-MASER/CESIUM/etc)",
            "Input Frequency": "(if external)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data


    def string(self):

        section_text = f"""
6.   Frequency Standard
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string() 
        else:
            s = Frequency()
            s.title = '6.x'
            section_text += s.string()
        return section_text
