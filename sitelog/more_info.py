import re
from sitelog.sections import Section
from sitelog import _format_string


class MoreInfo(Section):
    def __init__(
        self,
        primary_center="",
        secondary_center="",
        info_url="",
        site_map="",
        site_diagram="",
        horizon_mask="",
        monument="",
        site_pictures="",
        additional="",
        graphic="",
    ):
        super().__init__()
        self._data = self._template_dict()
        self.primary_center = primary_center
        self.secondary_center = secondary_center
        self.info_url = info_url
        self.site_map = site_map
        self.site_diagram = site_diagram
        self.horizon_mask = horizon_mask
        self.monument = monument
        self.site_pictures = site_pictures
        self.additional = additional
        self.graphic = graphic

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

    @property
    def graphic(self):
        return self.freeform

    @graphic.setter
    def graphic(self, value):
        if value is str:
            value = [value]
        self.freeform = ["Antenna Graphics with Dimensions"] + [value]

    def string(self):
        self.additional = _format_string(self.additional, "multilinevalue")
        section_text = f"""

13.  More Information

     Primary Data Center      : {self.primary_center}
     Secondary Data Center    : {self.secondary_center}
     URL for More Information : {self.info_url}
     Hardcopy on File
       Site Map               : {self.site_map}
       Site Diagram           : {self.site_diagram}
       Horizon Mask           : {self.horizon_mask}
       Monument Description   : {self.monument}
       Site Pictures          : {self.site_pictures}
     Additional Information   : {self.additional}
     Antenna Graphics with Dimensions
"""
        for i, line in enumerate(self.graphic):
            if re.findall("Antenna Graphics with Dimensions", line):
                if len(self.graphic) > i:
                    for line in self.graphic[i + 1 :]:
                        section_text += "\n" + line

        return section_text
