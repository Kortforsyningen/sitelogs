import re
from datetime import datetime as dt

from sitelog.sections import (
    SubSection,
    SectionList,
    Section,
)
from sitelog import _format_string


class Effect(Section):
    def __init__(self, date="", event=""):
        self._data = self._template_dict()
        self.date = date
        self.event = event

    def _template_dict(self):
        data = {
            "Date": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Event": "(TREE CLEARING/CONSTRUCTION/etc)",
        }
        return data

    @property
    def date(self):
        return self._data["Date"]

    @date.setter
    def date(self, value):
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
        self._data["Date"] = value

    @property
    def event(self):
        return self._data["Event"]

    @event.setter
    def event(self, value):
        self._data["Event"] = value

    def string(self):
        self.subsectionheader = _format_string("Date", "subsectitle")
        section_text = f"""
10.{self.subtitle} Date                     : {self.date}
     Event                    : {self.event}
"""

        return section_text


class EpisodicEffects(SectionList):
    def __init__(self):
        super().__init__()
        self.subsection_type = Effect
        self.section_type = "subsectionheader"

    def string(self):

        section_text = f"""
10.  Local Episodic Effects Possibly Affecting Data Quality
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string()
        else:
            s = self.subsection_type()
            s.subtitle = "x"
            section_text += s.string()

        return section_text
