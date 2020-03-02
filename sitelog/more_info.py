import re
from sitelog.sections import Section
from sitelog import _format_string


class MoreInfo(Section):
    def __init__(self):
        self._data = self._template_dict()

    def _template_dict(self):
        """
        We use the keys from the site log as keys in the data dict to ease
        reading of the site log
        """
        data = {
            "Primary Data Center": "",
            "Secondary Data Center": "",
            "URL for More Information": "",
            "Site Map": "(Y or URL)",
            "Site Diagram": "(Y or URL)",
            "Horizon Mask": "(Y or URL)",
            "Monument Description": "(Y or URL)",
            "Site Pictures": "(Y or URL)",
            "Additional Information": "(multiple lines)",
        }
        return data

    @property
    def primary_center(self):
        return self._data["Primary Data Center"]

    @primary_center.setter
    def primary_center(self, value):
        self._data["Primary Data Center"] = value

    @property
    def secondary_center(self):
        return self._data["Secondary Data Center"]

    @secondary_center.setter
    def secondary_center(self, value):
        self._data["Secondary Data Center"] = value

    @property
    def info_url(self):
        return self._data["URL for More Information"]

    @info_url.setter
    def info_url(self, value):
        self._data["URL for More Information"] = value

    @property
    def site_map(self):
        return self._data["Site Map"]

    @site_map.setter
    def site_map(self, value):
        self._data["Site Map"] = value

    @property
    def site_diagram(self):
        return self._data["Site Diagram"]

    @site_diagram.setter
    def site_diagram(self, value):
        self._data["Site Diagram"] = value

    @property
    def horizon_mask(self):
        return self._data["Horizon Mask"]

    @horizon_mask.setter
    def horizon_mask(self, value):
        self._data["Horizon Mask"] = value

    @property
    def monument(self):
        return self._data["Monument Description"]

    @monument.setter
    def monument(self, value):
        self._data["Monument Description"] = value

    @property
    def site_pictures(self):
        return self._data["Site Pictures"]

    @site_pictures.setter
    def site_pictures(self, value):
        self._data["Site Pictures"] = value

    @property
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        self.additional = _format_string(self.additional, "multilinevalue")
        section_text = f"""

13.  More Information

     Primary Data Center      :
     Secondary Data Center    :
     URL for More Information : 
     Hardcopy on File
       Site Map               : (Y or URL)
       Site Diagram           : (Y or URL)
       Horizon Mask           : (Y or URL)
       Monument Description   : (Y or URL)
       Site Pictures          : (Y or URL)
     Additional Information   : (multiple lines)
"""

        return section_text
