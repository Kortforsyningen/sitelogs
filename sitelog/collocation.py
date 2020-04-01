import re

from sitelog.sections import (
    SubSection,
    SectionList,
)
from sitelog import _format_string
from datetime import datetime as dt


class CollocationInstrument(SubSection):
    def __init__(
        self, instrumentation_type="", status="", effective_dates="", notes=""
        ):
        super().__init__()
        self._data = self._template_dict()
        self.number = None
        self.instrumentation_type = instrumentation_type
        self.status = status
        self.effective_dates = effective_dates
        self.notes = notes

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
        if value.upper() not in ("PERMANENT", "MOBILE", ""):
            raise ValueError("Status must either be PERMANENT or MOBILE")
        self._data["Status"] = value

    @property
    def effective_dates(self):
        return self._data["Effective Dates"]

    @effective_dates.setter
    def effective_dates(self, value):
        if isinstance(value, dt):
            value = value.strftime("%Y-%m-%d")
        elif isinstance(value, list):
            list_dates = []
            joint = "/"
            for date in value:
                list_dates.append(date.strftime("%Y-%m-%d"))
            value = joint.join(list_dates)
        elif value == "":
            pass
        else:
            list_dates = value.split("/")
            for date in list_dates:
                try:
                    datetime_object = dt.strptime(date, '%Y-%m-%d')
                except:
                    raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        self._data["Effective Dates"] = value

    @property
    def notes(self):
        return self._data["Notes"]

    @notes.setter
    def notes(self, value):
        self._data["Notes"] = value

    def string(self):
        self.subsectionheader = _format_string("Instrumentation Type", "subsectitle", len(str(self.subtitle)))
        self.notes = _format_string(self.notes, "multilinevalue")
        section_text = f"""
7.{self.subtitle}{self.subsectionheader}{self.instrumentation_type}
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
