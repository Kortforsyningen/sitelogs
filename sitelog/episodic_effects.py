import re

from sitelog.sections import (
    SubSection,
    SectionList,
    Section,
)


class Effect(Section):
    def __init__(self):
        self._data = self._template_dict()

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
        if not re.match(r"^\d{4}\-\d\d\-\d\d", value):
            raise ValueError("Date must be of the format CCYY-MM-DD")
        self._data["Date"] = value

    @property
    def event(self):
        return self._data["Event"]

    @event.setter
    def event(self, value):
        self._data["Event"] = value

    def string(self):
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
