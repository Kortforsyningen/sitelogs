import sitelog.sitelogger as sitelogger
import re

class MetInstrument(sitelogger.Section):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.number = None
        self.type = ''
        self.header_title = ''
        self.subsubtitle = ''

    def _template_dict(self):
        data = {
            "Other Instrumentation": "",
            "Water Vapor Radiometer": "",
            "Temp. Sensor Model": "",
            "Pressure Sensor Model": "",
            "Humidity Sensor Model": "",
            "Manufacturer": "",
            "Serial Number": "",
            "Data Sampling Interval": "(sec)",
            f"Accuracy (% rel h)": f"(% rel h)",
            "Aspiration": "(UNASPIRATED/NATURAL/FAN/etc)",
            "Height Diff to Ant": "(m)",
            "Calibration date": "(CCYY-MM-DD)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    @property
    def other(self):
        return self._data['Other Instrumentation']

    @other.setter
    def other(self, value):
        self._data['Other Instrumentation'] = value

    @property
    def header_val(self):
        return self._data['Pressure Sensor Model'] #skal kunne variere

    @header_val.setter
    def header_val(self, value):
        self._data['Pressure Sensor Model'] = value

    @property
    def manufacturer(self):
        return self._data['Manufacturer']

    @manufacturer.setter
    def manufacturer(self, value):
        self._data['Manufacturer'] = value

    @property
    def serial_number(self):
        return self._data['Serial Number']

    @serial_number.setter
    def serial_number(self, value):
        self._data['Serial Number'] = value

    @property
    def data_interval(self):
        return self._data['Data Sampling Interval']

    @data_interval.setter
    def data_interval(self, value):
        self._data['Data Sampling Interval'] = value


    def string(self):
        if self.title == 5: #re.match(r'^8\.5\.[\dx]+.+:$', self.subtitle[0]):
            section_text = f"""
8.{self.title} {self.other}
    """
        else:
            section_text = f"""
8.{self.subsubtitle}.{self.title} {self.header_title} {self.header_val}
       Manufacturer           : 
       Serial Number          : 
       Data Sampling Interval : (sec)
       Accuracy               : (hPa)
       Height Diff to Ant     : (m)
       Calibration date       : (CCYY-MM-DD)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
    """
        return section_text



class Meterological(sitelogger.SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = MetInstrument
        self.section_type = 'subsubsectionheader'
        self.subsubtitle = ''
        self.header_title = ''


    def _template_dict(self):
        data = {
            "Other Instrumentation": "",
            "Water Vapor Radiometer": "",
            "Temp. Sensor Model": "",
            "Pressure Sensor Model": "",
            "Humidity Sensor Model": "",
            "Manufacturer": "",
            "Serial Number": "",
            "Data Sampling Interval": "(sec)",
            f"Accuracy (% rel h)": f"(% rel h)",
            "Aspiration": "(UNASPIRATED/NATURAL/FAN/etc)",
            "Height Diff to Ant": "(m)",
            "Calibration date": "(CCYY-MM-DD)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data


    def string(self):

        section_text = f"""
8.   Meteorological Instrumentation
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string() 
        else:
            # subsubtitles = ['8.1.x Humidity Sensor Model   :', '8.2.x Pressure Sensor Model   :', '8.3.x Temp. Sensor Model      :', '8.4.x Water Vapor Radiometer  :', '8.5.x Other Instrumentation   :']
            # for subsubtitle in subsubtitles:
            s = self.subsection_type()
            s.subsubtitle = [self.subsubtitle]
            s.header_title = [self.header_title]
            section_text += s.string()
        return section_text

class Humidity(Meterological):
    def __init__(self):
        self.type = 'Humidity Sensor Model'
        self.header_title = 'Humidity Sensor Model   :'
        self.subsubtitle = 1
        super().__init__()

# class Pressure(Meterological):
#     def __init__(self):
#         super().__init__()
#         self.type = 'Pressure Sensor Model'
#         self.header_title = 'Pressure Sensor Model   :'
#         self.subsubtitle = 2

# class Temp(Meterological):
#     def __init__(self):
#         super().__init__()
#         self.type = 'Temp. Sensor Model'
#         self.header_title = 'Temp. Sensor Model      :'
#         self.subsubtitle = 1
