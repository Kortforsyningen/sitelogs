import re

from sitelog.sections import (
    SubSection,
    SectionList,
)
from sitelog import _format_string
from datetime import datetime as dt


class Frequency(SubSection):
    def __init__(self, standard_type="", input_freq="", effective_dates="", notes=""):
        super().__init__()
        self._data = self._template_dict()
        self.number = None
        self.standard_type = standard_type
        self.input_freq = input_freq
        self.effective_dates = effective_dates
        self.notes = notes

    def _template_dict(self):
        data = {
            "Standard Type": "(INTERNAL or EXTERNAL H-MASER/CESIUM/etc)",
            "Input Frequency": "(if external)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    @property
    def standard_type(self):
        return self._data["Standard Type"]

    @standard_type.setter
    def standard_type(self, value):
        self._data["Standard Type"] = value

    @property
    def input_freq(self):
        return self._data["Input Frequency"]

    @input_freq.setter
    def input_freq(self, value):
        self._data["Input Frequency"] = value

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
                    datetime_object = dt.strptime(date, "%Y-%m-%d")
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
        self.notes = _format_string(self.notes, "multilinevalue")
        self.subsectionheader = _format_string(
            "Standard Type", "subsectitle", len(str(self.subtitle))
        )
        section_text = f"""
6.{self.subtitle}{self.subsectionheader}{self.standard_type}
       Input Frequency        : {self.input_freq}
       Effective Dates        : {self.effective_dates}
       Notes                  : {self.notes}
"""
        return section_text


class FrequencyStandard(SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = Frequency
        self.section_type = "subsectionheader"

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
            s.subtitle = "x"
            section_text += s.string()

        return section_text
