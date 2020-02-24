import re

from sitelog.sections import (
    SubSection,
    SectionList,
)

class Frequency(SubSection):
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

    @property
    def standard_type(self):
        return self._data['Standard Type']

    @standard_type.setter
    def standard_type(self, value):
        self._data['Standard Type'] = value

    @property
    def input_freq(self):
        return self._data['Input Frequency']

    @input_freq.setter
    def input_freq(self, value):
        self._data['Input Frequency'] = value

    @property
    def effective_dates(self):
        return self._data['Effective Dates']

    @effective_dates.setter
    def effective_dates(self, value):
        self._data['Effective Dates'] = value

    @property
    def notes(self):
        return self._data['Notes']

    @notes.setter
    def notes(self, value):
        self._data['Notes'] = value

    def string(self):

        section_text = f"""
6.{self.subtitle}  Standard Type            : {self.standard_type}
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
            s.subtitle = 'x'
            section_text += s.string()
        return section_text
