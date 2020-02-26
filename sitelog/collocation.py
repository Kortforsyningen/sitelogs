import re

from sitelog.sections import (
    SubSection,
    SectionList,
)
from sitelog import _format_string


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

    @property
    def instrumentation_type(self):
        return self._data["Instrumentation Type"]

    @instrumentation_type.setter
    def instrumentation_type(self, value):
        self._data["Instrumentation Type"] = value

    @property
    def status(self):
        return self._data["Status"]

    @status.setter
    def status(self, value):
        self._data["Status"] = value

    @property
    def effective_dates(self):
        return self._data["Effective Dates"]

    @effective_dates.setter
    def effective_dates(self, value):
        self._data["Effective Dates"] = value

    @property
    def notes(self):
        return self._data["Notes"]

    @notes.setter
    def notes(self, value):
        self._data["Notes"] = value

    def string(self):
        self.notes = _format_string(self.notes, "multilinevalue")
        section_text = f"""
7.{self.subtitle}  Instrumentation Type     : {self.instrumentation_type}
       Status                 : {self.status}
       Effective Dates        : {self.effective_dates}
       Notes                  : {self.notes}
"""
        return section_text


class Collocation(SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = CollocationInstrument
        self.section_type = "subsectionheader"

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
            s.subtitle = "x"
            section_text += s.string()
        return section_text
