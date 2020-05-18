import re

from sitelog.sections import (
    SubSection,
    SectionList,
    Section,
)
from sitelog import _format_string
from datetime import datetime as dt


class GnssReceiver(SubSection):
    def __init__(
        self,
        receiver_type="",
        sat_sys="",
        serial="",
        firmware="",
        cutoff="",
        date_installed="",
        date_removed="",
        temperature="",
        additional="",
    ):
        super().__init__()
        self._data = self._template_dict()
        self.receiver_type = receiver_type
        self.sat_sys = sat_sys
        self.serial = serial
        self.firmware = firmware
        self.cutoff = cutoff
        self.date_installed = date_installed
        self.date_removed = date_removed
        self.temperature = temperature
        self.additional = additional

    def _template_dict(self):
        data = {
            "Receiver Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Satellite System": "(GPS+GLO+GAL+BDS+QZSS+SBAS)",
            "Serial Number": "(A20, but note the first A5 is used in SINEX)",
            "Firmware Version": "(A11)",
            "Elevation Cutoff Setting": "(deg)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Date Removed": "(CCYY-MM-DDThh:mmZ)",
            "Temperature Stabiliz.": "(none or tolerance in degrees C)",
            "Additional Information": "(multiple lines)",
        }
        return data

    @property
    def receiver_type(self):
        return self._data["Receiver Type"]

    @receiver_type.setter
    def receiver_type(self, value):
        if len(value) > 20:
            raise ValueError(
                "Receiver Type from rcvr_ant.tab must be no longer than 20 characters long"
            )
        self._data["Receiver Type"] = value

    @property
    def sat_sys(self):
        return self._data["Satellite System"]

    @sat_sys.setter
    def sat_sys(self, value):
        self._data["Satellite System"] = value

    @property
    def serial(self):
        return self._data["Serial Number"]

    @serial.setter
    def serial(self, value):
        if not len(value) < 20:
            raise ValueError("Serial Number must be no longer than 20 characters")
        self._data["Serial Number"] = value

    @property
    def firmware(self):
        return self._data["Firmware Version"]

    @firmware.setter
    def firmware(self, value):
        if len(value) > 11:
            raise ValueError("Firmware string can not be longer than 11 characters")
        self._data["Firmware Version"] = value

    @property
    def cutoff(self):
        return self._data["Elevation Cutoff Setting"]

    @cutoff.setter
    def cutoff(self, value):
        self._data["Elevation Cutoff Settingn"] = value

    @property
    def date_installed(self):
        return self._data["Date Installed"]

    @date_installed.setter
    def date_installed(self, value):
        if isinstance(value, dt):
            try:
                value = value.strftime("%Y-%m-%dT%H:%M%Z")
            except:
                value = value.strftime("%Y-%m-%d")
        elif value == "":
            pass
        else:
            datetime_object = None
            time_formats = ["%Y-%m-%dT%H:%M%Z", "%Y-%m-%dT%H:%MZ", "%Y-%m-%d"]

            for format in time_formats:
                try:
                    datetime_object = dt.strptime(value, format)
                    break
                except:
                    continue

            if datetime_object is None:
                raise ValueError("Incorrect date format, should be (CCYY-MM-DDThh:mmZ)")
        self._data["Date Installed"] = value

    @property
    def date_removed(self):
        return self._data["Date Removed"]

    @date_removed.setter
    def date_removed(self, value):
        if isinstance(value, dt):
            try:
                value = value.strftime("%Y-%m-%dT%H:%M%Z")
            except:
                value = value.strftime("%Y-%m-%d")
        elif value == "":
            pass
        else:
            datetime_object = None
            time_formats = ["%Y-%m-%dT%H:%M%Z", "%Y-%m-%dT%H:%MZ", "%Y-%m-%d"]

            for format in time_formats:
                try:
                    datetime_object = dt.strptime(value, format)
                    break
                except:
                    continue

            if datetime_object is None:
                raise ValueError("Incorrect date format, should be (CCYY-MM-DDThh:mmZ)")
        self._data["Date Removed"] = value

    @property
    def temperature(self):
        return self._data["Temperature Stabiliz."]

    @temperature.setter
    def temperature(self, value):
        self._data["Temperature Stabiliz."] = value

    @property
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        self.subsectionheader = _format_string(
            "Receiver Type", "subsectitle", len(str(self.subtitle))
        )
        self.additional = _format_string(self.additional, "multilinevalue")
        section_text = f"""
3.{self.subtitle}{self.subsectionheader}{self.receiver_type}
     Satellite System         : {self.sat_sys}
     Serial Number            : {self.serial}
     Firmware Version         : {self.firmware}
     Elevation Cutoff Setting : {self.cutoff}
     Date Installed           : {self.date_installed}
     Date Removed             : {self.date_removed}
     Temperature Stabiliz.    : {self.temperature}
     Additional Information   : {self.additional}
"""

        return section_text


class GNSS(SectionList):
    def __init__(self):
        super().__init__()
        self.subsection_type = GnssReceiver
        self.section_type = "subsectionheader"  # subsection

    def string(self):

        section_text = f"""
3.   GNSS Receiver Information
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string()
        else:
            s = self.subsection_type()
            s.subtitle = "x"
            section_text += s.string()

        return section_text
