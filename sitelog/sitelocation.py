import sitelog.sitelogger as sitelogger
import re

class SiteLocation(sitelogger.Section):

    def _template_dict(self):

        data = {
            "City or Town": "",
            "State or Province": "",
            "Country": "",
            "Tectonic Plate": "",
            "Approximate Position (ITRF)" : "",
            "X coordinate (m)": "",
            "Y coordinate (m)": "",
            "Z coordinate (m)": "",
            "Latitude (N is +)": "(+/-DDMMSS.SS)",
            "Longitude (E is +)": "(+/-DDDMMSS.SS)",
            "Elevation (m,ellips.)": "(F7.1)",
            "Additional Information": "(multiple lines)",
        }
        return data

    def __init__(self):
        self._data = self._template_dict()

    @property
    def city(self):
        return self._data['City or Town']

    @city.setter
    def city(self, value):
        self._data['City or Town'] = value

    @property
    def state(self):
        return self._data['State or Province']

    @state.setter
    def state(self, value):
        self._data['State or Province'] = value

    @property
    def country(self):
        return self._data['Country']

    @country.setter
    def country(self, value):
        self._data['Country'] = value

    @property
    def tectonic_plate(self):
        return self._data['Tectonic Plate']

    @tectonic_plate.setter
    def tectonic_plate(self, value):
        self._data['Tectonic Plate'] = value

    @property
    def x(self):
        value = self._data['X coordinate (m)']
        if  re.match(r'^[\d\.]+$', value):
            value = '{:8.1f}'.format(float(value))
            value = f"{float(value):8.1f}"
        elif re.match(r'^[\d\.]+\s*[^0-9.]+$', value):
            value = '{:8.1f}'.format(float(re.sub(r'\s*[^0-9.]+', '', value)))
        return value

    @x.setter
    def x(self, value):
        self._data['X coordinate (m)'] = value

    @property
    def y(self):
        value = self._data['Y coordinate (m)']
        if  re.match(r'^[\d\.]+$', value):
            value = '{:8.1f}'.format(float(value))
        elif re.match(r'^[\d\.]+\s*[^0-9.]+$', value):
            value = '{:8.1f}'.format(float(re.sub(r'\s*[^0-9.]+', '', value)))
        return value

    @y.setter
    def y(self, value):
        self._data['Y coordinate (m)'] = value

    @property
    def z(self):
        value = self._data['Z coordinate (m)']
        if  re.match(r'^[\d\.]+$', value):
            value = '{:8.1f}'.format(float(value))
        elif re.match(r'^[\d\.]+\s*[^0-9.]+$', value):
            value = '{:8.1f}'.format(float(re.sub(r'\s*[^0-9.]+', '', value)))
        return value

    @z.setter
    def z(self, value):
        self._data['Z coordinate (m)'] = value

    @property
    def latitude(self):
        return self._data['Latitude (N is +)']

    @latitude.setter
    def latitude(self, value):
        self._data['Latitude (N is +)'] = value

    @property
    def longitude(self):
        return self._data['Longitude (E is +)']

    @longitude.setter
    def longitude(self, value):
        self._data['Longitude (E is +)'] = value

    @property
    def elevation(self):
        value = self._data['Elevation (m,ellips.)']
        if  re.match(r'^[\d\.]+$', value):
            value = '{:7.1f}'.format(float(value))
        elif re.match(r'^[\d\.]+\s*[^0-9.]+$', value):
            value = '{:7.1f}'.format(float(re.sub(r'\s*[^0-9.]+', '', value)))
        return value


    @elevation.setter
    def elevation(self, value):
        self._data['Elevation (m,ellips.)'] = value

    @property
    def additional(self):
        return self._data['Additional Information']

    @additional.setter
    def additional(self, value):
        self._data['Additional Information'] = value

    def string(self):

        section_text = f"""
2.   Site Location Information

     City or Town             : {self.city}
     State or Province        : {self.state}
     Country                  : {self.country}
     Tectonic Plate           : {self.tectonic_plate}
     Approximate Position (ITRF)
       X coordinate (m)       : {self.x}
       Y coordinate (m)       : {self.y}
       Z coordinate (m)       : {self.z}
       Latitude (N is +)      : {self.latitude}
       Longitude (E is +)     : {self.longitude}
       Elevation (m,ellips.)  : {self.elevation}
     Additional Information   : {self.additional}
"""
        return section_text
