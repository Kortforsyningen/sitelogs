import re

from sitelog.sections import (
    SubSection,
    SectionList,
)

class CollocationInstrument(SubSection):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.number = None

    def _template_dict(self):
        data = {
            "Instrumentation Type": "(GPS/GLONASS/DORIS/PRARE/SLR/VLBI/TIME/etc)",
            "Status": "(PERMANENT/MOBILE)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    def string(self):

        section_text = f"""
7.{self.title}  Instrumentation Type     : (GPS/GLONASS/DORIS/PRARE/SLR/VLBI/TIME/etc)
       Status                 : (PERMANENT/MOBILE)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
"""
        return section_text

class Collocation(SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = CollocationInstrument
        self.section_type = 'subsectionheader'

    def _template_dict(self):
        data = {
            "Instrumentation Type": "(GPS/GLONASS/DORIS/PRARE/SLR/VLBI/TIME/etc)",
            "Status": "(PERMANENT/MOBILE)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data



    def string(self):

        section_text = f"""
7.   Collocation Information
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string()
        else:
            s = CollocationInstrument()
            s.title = 'x'
            section_text += s.string()
        return section_text

