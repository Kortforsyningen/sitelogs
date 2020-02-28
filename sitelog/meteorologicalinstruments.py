import re
from enum import Enum


class SensorType(Enum):
    HUMIDITY = "Humidity Sensor Model"
    PRESSURE = "Pressure Sensor Model"
    TEMPERATURE = "Temp. Sensor Model"
    WATERVAPOR = "Water Vapor Radiometer"
    OTHER = "Other Instrumentation"


from sitelog.sections import (
    SubSection,
    SectionList,
    Section,
)
from sitelog import _format_string

gen_title = "Humidity/Pressure/Temp. Sensor Model, Water Vapor Radiometer or Other"


class MetInstrument(Section):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.number = None
        self.subsubtitle = ""
        self.title = gen_title

    def _template_dict(self):
        data = {
            "Model": "",
            "Manufacturer": "",
            "Serial Number": "",
            "Data Sampling Interval": "(sec)",
            "Distance to Antenna": "(m)",
            "Accuracy": "",
            "Aspiration": "(UNASPIRATED/NATURAL/FAN/etc)",
            "Height Diff to Ant": "(m)",
            "Calibration date": "(CCYY-MM-DD)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    @property
    def instrument(self):
        return self.instrument

    @instrument.setter
    def instrument(self, value):
        if not isinstance(value, SensorType):
            raise ValueError("Input needs to be a SensorType()")
        else:
            self.title = value.value
            if value.value == "HUMIDITY":
                self.subtitle = "1."
            elif value.name == "PRESSURE":
                self.subtitle = "2."
            elif value.name == "TEMPERATURE":
                self.subtitle = "3."
            elif value.name == "WATERVAPOR":
                self.subtitle = "4."
            elif value.name == "OTHER":
                self.subtitle = "5."
            else:
                self.subtitle = "x."

    @property
    def other(self):
        return self._data["Other Instrumentation"]

    @other.setter
    def other(self, value):
        self._data["Other Instrumentation"] = value

    @property
    def model(self):
        return self._data["Model"]

    @model.setter
    def model(self, value):
        self._data["Model"] = value

    @property
    def manufacturer(self):
        return self._data["Manufacturer"]

    @manufacturer.setter
    def manufacturer(self, value):
        self._data["Manufacturer"] = value

    @property
    def serial_number(self):
        return self._data["Serial Number"]

    @serial_number.setter
    def serial_number(self, value):
        self._data["Serial Number"] = value

    @property
    def data_interval(self):
        return self._data["Data Sampling Interval"]

    @data_interval.setter
    def data_interval(self, value):
        self._data["Data Sampling Interval"] = value

    @property
    def distance_antenna(self):
        return self._data['Distance to Antenna']

    @distance_antenna.setter
    def distance_antenna(self, value):
        self._data['Distance to Antenna'] = value

    @property
    def accuracy(self):
        return self._data[f"Accuracy"]

    @accuracy.setter
    def accuracy(self, value):
        self._data[f"Accuracy"] = value

    @property
    def aspiration(self):
        return self._data[f"Aspiration"]

    @aspiration.setter
    def aspiration(self, value):
        self._data[f"Aspiration"] = value

    @property
    def height_diff(self):
        return self._data["Height Diff to Ant"]

    @height_diff.setter
    def height_diff(self, value):
        self._data["Height Diff to Ant"] = value

    @property
    def calibration_date(self):
        return self._data["Calibration date"]

    @calibration_date.setter
    def calibration_date(self, value):
        if not re.match(r"^\d{4}\-\d\d\-\d\d", value):
            raise ValueError("Calibration date must be of the format CCYY-MM-DDT")
        self._data["Calibration date"] = value

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
        self.subsubtitle = _format_string(self.subsubtitle, "subsubsecnr")
        self.title = _format_string(self.title, "subsubsectitle")
        self.notes = _format_string(self.notes,"multilinevalue")
        self.model = _format_string(self.model,"multilinevalue")
        if self.subtitle == "5.":
            section_text = f"""
{self.subsubtitle}{self.title}{self.model}
"""
        elif self.subtitle == '2.':
            section_text = f"""
{self.subsubtitle}{self.title}{self.model}
       Manufacturer           : {self.manufacturer}
       Serial Number          : {self.serial_number}
       Data Sampling Interval : {self.data_interval}
       Accuracy               : {self.accuracy}
       Height Diff to Ant     : {self.height_diff}
       Calibration date       : {self.calibration_date}
       Effective Dates        : {self.effective_dates}
       Notes                  : {self.notes}
"""
        elif self.subtitle == '4.':
            section_text = f"""
{self.subsubtitle}{self.title}{self.model}
       Manufacturer           : {self.manufacturer}
       Serial Number          : {self.serial_number}
       Distance to Antenna    : {self.distance_antenna}
       Height Diff to Ant     : {self.height_diff}
       Calibration date       : {self.calibration_date}
       Effective Dates        : {self.effective_dates}
       Notes                  : {self.notes}
"""           
        else:
            section_text = f"""
{self.subsubtitle}{self.title}{self.model}
       Manufacturer           : {self.manufacturer}
       Serial Number          : {self.serial_number}
       Data Sampling Interval : {self.data_interval}
       Accuracy (% rel h)     : {self.accuracy}
       Aspiration             : {self.aspiration}
       Height Diff to Ant     : {self.height_diff}
       Calibration date       : {self.calibration_date}
       Effective Dates        : {self.effective_dates}
       Notes                  : {self.notes}
"""
        return section_text


class Meteorological(SectionList):
    def __init__(self):
        super().__init__()
        self.list_subtitles = []
        self.subsection_type = MetInstrument
        self.section_type = "subsubsectionheader"


    def string(self):

        section_text = f"""
8.   Meteorological Instrumentation
"""
        if self._subsections:
            self._subsections = sorted(self._subsections, key=lambda x: x.subtitle)
            for subsection in self._subsections:
                self.list_subtitles.append(subsection.subtitle)
                # hvis intet eller ugyldigt instrument er givet
                if subsection.title == gen_title:
                    subsection.subtitle = "x."
                if subsection.subtitle == "x.":
                    subsection.subsubtitle = "x"
                else:
                    subsection.subsubtitle = str(
                        self.list_subtitles.count(subsection.subtitle)
                    )
                subsection.subsubtitle = (
                    "8." + subsection.subtitle + subsection.subsubtitle
                )
                section_text += subsection.string()
        else:
            s = self.subsection_type()
            s.title = gen_title
            s.subtitle = "x."
            s.subsubtitle = "8." + s.subtitle + "x"
            section_text += s.string()
        return section_text
