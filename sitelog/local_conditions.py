import re
from enum import Enum


class ConditionTypes(Enum):
    RADIO = "Radio Interferences"
    MULTIPATH = "Multipath Sources"
    OBSTRUCTION = "Signal Obstructions"


from sitelog.sections import (
    SubSection,
    SectionList,
    Section,
)
from sitelog import _format_string

gen_title = "Local Condition"


class LocalCondition(Section):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.title = gen_title
        self.subsubtitle = ""

    def _template_dict(self):
        data = {
            "Source": "",
            "Observed Degradations": "(SN RATIO/DATA GAPS/etc)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Additional Information": "(multiple lines)",
        }
        return data

    @property
    def condition(self):
        return self.condition

    @condition.setter
    def condition(self, value):
        if not isinstance(value, ConditionTypes):
            raise ValueError("Input needs to be a ConditionTypes()")
        else:
            self.title = value.value
            if value.name == "RADIO":
                self.subtitle = "1."
            elif value.name == "MULTIPATH":
                self.subtitle = "2."
            elif value.name == "OBSTRUCTION":
                self.subtitle = "3."
            else:
                self.subtitle = "x."

    @property
    def source(self):
        return self._data["Source"]

    @source.setter
    def source(self, value):
        self._data["Source"] = value

    @property
    def obs_degradation(self):
        return self._data["Observed Degradations"]

    @obs_degradation.setter
    def obs_degradation(self, value):
        self._data["Observed Degradations"] = value

    @property
    def dates(self):
        return self._data["Effective Dates"]

    @dates.setter
    def dates(self, value):
        self._data["Effective Dates"] = value

    @property
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        self.subsubtitle = _format_string(self.subsubtitle, "subsubsecnr")
        self.title = _format_string(self.title, "subsubsectitle")
        self.additional = _format_string(self.additional, "multilinevalue")
        if self.subtitle == "1." or self.subtitle == "x.":
            section_text = f"""
{self.subsubtitle}{self.title}{self.source}
       Observed Degradations  : {self.obs_degradation}
       Effective Dates        : {self.dates}
       Additional Information : {self.additional}
"""
        else:
            section_text = f"""
{self.subsubtitle}{self.title}{self.source}
       Effective Dates        : {self.dates}
       Additional Information : {self.additional}
"""
        return section_text


class Conditions(SectionList):
    def __init__(self):
        super().__init__()
        self.list_subtitles = []
        self.subsection_type = LocalCondition
        self.section_type = "subsubsectionheader"

    def string(self):
        section_text = f"""
9.  Local Ongoing Conditions Possibly Affecting Computed Position
"""
        if self._subsections:
            self._subsections = sorted(self._subsections, key=lambda x: x.subtitle)
            for subsection in self._subsections:
                self.list_subtitles.append(subsection.subtitle)
                if subsection.title == gen_title:
                    subsection.subtitle = "x."
                if subsection.subtitle == "x.":
                    subsection.subsubtitle = "x"
                else:
                    subsection.subsubtitle = str(
                        self.list_subtitles.count(subsection.subtitle)
                    )
                subsection.subsubtitle = (
                    "9." + subsection.subtitle + subsection.subsubtitle
                )
                section_text += subsection.string()
        else:
            s = self.subsection_type()
            s.title = gen_title
            s.subtitle = "x."
            s.subsubtitle = "9." + s.subtitle + "x"
            section_text += s.string()
        return section_text
