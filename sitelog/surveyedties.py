import re

from sitelog.sections import (
    SubSection,
    SectionList,
)
from sitelog import _format_string
from datetime import datetime as dt


class Tie(SubSection):
    def __init__(
        self, marker_name="", marker_usage="", marker_cdp="", marker_domes="", dx="",
        dy="", dz="", accuracy="", method="", date_measured="", additional=""
        ):
        super().__init__()
        self._data = self._template_dict()
        self.number = None
        self.marker_name = marker_name
        self.marker_usage = marker_usage
        self.marker_cdp = marker_cdp
        self.marker_domes = marker_domes
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.accuracy = accuracy
        self.method = method
        self.date_measured = date_measured
        self.additional = additional

    def _template_dict(self):
        data = {
            "Tied Marker Name": "",
            "Tied Marker Usage": "(SLR/VLBI/LOCAL CONTROL/FOOTPRINT/etc)",
            "Tied Marker CDP Number": "(A4)",
            "Tied Marker DOMES Number": "(A9)",
            "Differential Components from GNSS Marker to the tied monument (ITRS)": "",
            "dx (m)": "(m)",
            "dy (m)": "(m)",
            "dz (m)": "(m)",
            "Accuracy (mm)": "(mm)",
            "Survey method": "(GPS CAMPAIGN/TRILATERATION/TRIANGULATION/etc)",
            "Date Measured": "(CCYY-MM-DDThh:mmZ)",
            "Additional Information": "(multiple lines)",
        }
        return data

    @property
    def marker_name(self):
        return self._data["Tied Marker Name"]

    @marker_name.setter
    def marker_name(self, value):
        self._data["Tied Marker Name"] = value

    @property
    def marker_usage(self):
        return self._data["Tied Marker Usage"]

    @marker_usage.setter
    def marker_usage(self, value):
        self._data["Tied Marker Usage"] = value

    @property
    def marker_cdp(self):
        return self._data["Tied Marker CDP Number"]

    @marker_cdp.setter
    def marker_cdp(self, value):
        if len(value) > 4:
            raise ValueError("Tied Marker CDP Number must be 4 characters long")
        self._data["Tied Marker CDP Number"] = value

    @property
    def marker_domes(self):
        return self._data["Tied Marker DOMES Number"]

    @marker_domes.setter
    def marker_domes(self, value):
        if len(value) > 9:
            raise ValueError(
                "Tied Marker DOMES Number must be no longer than 9 characters"
            )
        self._data["Tied Marker DOMES Number"] = value

    @property
    def dx(self):
        return self._data["dx (m)"]

    @dx.setter
    def dx(self, value):
        self._data["dx (m)"] = value

    @property
    def dy(self):
        return self._data["dy (m)"]

    @dy.setter
    def dy(self, value):
        self._data["dy (m)"] = value

    @property
    def dz(self):
        return self._data["dz (m)"]

    @dz.setter
    def dz(self, value):
        self._data["dz (m)"] = value

    @property
    def accuracy(self):
        return self._data["Accuracy (mm)"]

    @accuracy.setter
    def accuracy(self, value):
        self._data["Accuracy (mm)"] = value

    @property
    def method(self):
        return self._data["Survey method"]

    @method.setter
    def method(self, value):
        self._data["Survey method"] = value

    @property
    def date_measured(self):
        return self._data["Date Measured"]

    @date_measured.setter
    def date_measured(self, value):
        if isinstance(value, dt):
            try:
                value = value.strftime("%Y-%m-%dT%H:%M%Z")
            except:
                value = value.strftime("%Y-%m-%d")
        elif value == "":
            pass
        else:
            datetime_object = None
            time_formats = ['%Y-%m-%dT%H:%M%Z','%Y-%m-%dT%H:%MZ','%Y-%m-%d']

            for format in time_formats:
                try:
                    datetime_object = dt.strptime(value, format)
                    break
                except:
                    continue
            
            if datetime_object is None:
                raise ValueError("Incorrect date format, should be (CCYY-MM-DDThh:mmZ)")
        self._data["Date Measured"] = value

    @property
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        self.additional = _format_string(self.additional, "multilinevalue")
        self.subsectionheader = _format_string("Tied Marker Name", "subsectitle", len(str(self.subtitle)))
        section_text = f"""
5.{self.subtitle}{self.subsectionheader}{self.marker_name}
     Tied Marker Usage        : {self.marker_usage}
     Tied Marker CDP Number   : {self.marker_cdp}
     Tied Marker DOMES Number : {self.marker_domes}
     Differential Components from GNSS Marker to the tied monument (ITRS)
       dx (m)                 : {self.dx}
       dy (m)                 : {self.dy}
       dz (m)                 : {self.dz}
     Accuracy (mm)            : {self.accuracy}
     Survey method            : {self.method}
     Date Measured            : {self.date_measured}
     Additional Information   : {self.additional}
"""
        
        return section_text


class LocalTies(SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = Tie
        self.section_type = "subsectionheader"

    def _template_dict(self):
        data = {
            "Tied Marker Name": "",
            "Tied Marker Usage": "(SLR/VLBI/LOCAL CONTROL/FOOTPRINT/etc)",
            "Tied Marker CDP Number": "(A4)",
            "Tied Marker DOMES Number": "(A9)",
            "Differential Components from GNSS Marker to the tied monument (ITRS)": "",
            "dx (m)": "(m)",
            "dy (m)": "(m)",
            "dz (m)": "(m)",
            "Accuracy (mm)": "(mm)",
            "Survey method": "(GPS CAMPAIGN/TRILATERATION/TRIANGULATION/etc)",
            "Date Measured": "(CCYY-MM-DDThh:mmZ)",
            "Additional Information": "(multiple lines)",
        }
        return data

    def string(self):

        section_text = f"""
5.   Surveyed Local Ties
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string()
        else:
            s = Tie()
            s.subtitle = "x"
            section_text += s.string()
        
        return section_text
