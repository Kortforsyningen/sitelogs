import re
from enum import Enum
from datetime import datetime as dt


class ConditionTypes(Enum):
    RADIO = "Radio Interferences"
    MULTIPATH = "Multipath Sources"
    OBSTRUCTION = "Signal Obstructions"
    UNKNOWN = ""


from sitelog.sections import (
    SubSection,
    SectionList,
    Section,
)
from sitelog import _format_string

gen_title = "Local Condition"


class LocalCondition(Section):
    def __init__(
        self, condition =ConditionTypes.UNKNOWN, source="", observed_degradation="", dates="", additional=""
        ):
        super().__init__()
        self._data = self._template_dict()
        self.title = gen_title
        self.subsubtitle = ""
        self.number = ""
        self.condition = condition
        self.source = source
        self.obs_degradation = observed_degradation
        self.dates = dates
        self.additional = additional

    def _template_dict(self):
        data = {
            "Model": "",
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
                self.subsubtitle = "1."
            elif value.name == "MULTIPATH":
                self.subsubtitle = "2."
            elif value.name == "OBSTRUCTION":
                self.subsubtitle = "3."
            else:
                self.subsubtitle = "x."

    @property
    def source(self):
        return self._data["Model"]

    @source.setter
    def source(self, value):
        self._data["Model"] = value

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
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        self.number = _format_string(self.number, "subsubsecnr")
        self.title = _format_string(self.title, "subsubsectitle")
        self.additional = _format_string(self.additional, "multilinevalue")
        if self.subsubtitle == "1." or self.subsubtitle == "x.":
            section_text = f"""
{self.number}{self.title}{self.source}
       Observed Degradations  : {self.obs_degradation}
       Effective Dates        : {self.dates}
       Additional Information : {self.additional}
"""
        else:
            section_text = f"""
{self.number}{self.title}{self.source}
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
            self._subsections = sorted(self._subsections, key=lambda x: x.subsubtitle)
            for subsection in self._subsections:
                self.list_subtitles.append(subsection.subsubtitle)
                if subsection.title == gen_title:
                    subsection.subtitle = "x."
                if subsection.subsubtitle == "x.":
                    subsection.subsubtitle = "x"
                else:
                    subsection.subtitle = str(
                        self.list_subtitles.count(subsection.subsubtitle)
                    )
                subsection.number = (
                    "9." + subsection.subsubtitle + subsection.subtitle
                )
                section_text += subsection.string()
        else:
            s = self.subsection_type()
            s.title = gen_title
            s.subtitle = "x."
            s.subsubtitle = "9." + s.subtitle + "x"
            section_text += s.string()
        
        return section_text
