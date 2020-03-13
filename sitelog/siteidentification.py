import re
from sitelog.sections import Section
from sitelog import _format_string


class SiteIdentification(Section):
    def __init__(
        self, site_name="", site_code="XXXX", inscription="", IERS_number="", CDP_number="", monument="", monument_h="",
        foundation="", foundation_depth="", marker="", date="", geologic="", bedrock_type="", bedrock_condition="",
        fracture="", fault="", distance="", additional=""
        ):
        self._data = self._template_dict()
        self.site_name = site_name
        self.site_code = site_code
        self.inscription = inscription
        self.IERS_number = IERS_number
        self.CDP_number = CDP_number
        self.monument = monument
        self.monument_h = monument_h
        self.foundation = foundation
        self.foundation_depth = foundation_depth
        self.marker = marker
        self.date = date
        self.geologic = geologic
        self.bedrock_type = bedrock_type
        self.bedrock_condition = bedrock_condition
        self.fracture = fracture
        self.fault = fault
        self.distance = distance
        self.additional = additional


    def _template_dict(self):
        """
        We use the keys from the site log as keys in the data dict to ease
        reading of the site log
        """
        data = {
            "Site Name": "",
            "Four Character ID": "(A4)",
            "Monument Inscription": "",
            "IERS DOMES Number": "(A9)",
            "CDP Number": "(A4)",
            "Monument Description": "(PILLAR/BRASS PLATE/STEEL MAST/etc)",
            "Height of the Monument": "(m)",
            "Monument Foundation": "(STEEL RODS, CONCRETE BLOCK, ROOF, etc)",
            "Foundation Depth": "(m)",
            "Marker Description": "(CHISELLED CROSS/DIVOT/BRASS NAIL/etc)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Geologic Characteristic": "(BEDROCK/CLAY/CONGLOMERATE/GRAVEL/SAND/etc)",
            "Bedrock Type": "(IGNEOUS/METAMORPHIC/SEDIMENTARY)",
            "Bedrock Condition": "(FRESH/JOINTED/WEATHERED)",
            "Fracture Spacing": "(1-10 cm/11-50 cm/51-200 cm/over 200 cm)",
            "Fault zones nearby": "(YES/NO/Name of the zone)",
            "Distance/activity": "(multiple lines)",
            "Additional Information": "(multiple lines)",
        }
        return data


    @property
    def site_name(self):
        return self._data["Site Name"]

    @site_name.setter
    def site_name(self, value):
        self._data["Site Name"] = value

    @property
    def site_code(self):
        return self._data["Four Character ID"]

    @site_code.setter
    def site_code(self, value):
        if not (re.match(r"^[A-Z0-9]{4}$", value) or value==""):
            raise ValueError("The Four Character ID *must* be 4 characters long!")
        self._data["Four Character ID"] = value

    @property
    def inscription(self):
        return self._data["Monument Inscription"]

    @inscription.setter
    def inscription(self, value):
        self._data["Monument Inscription"] = value

    @property
    def IERS_number(self):
        return self._data["IERS DOMES Number"]

    @IERS_number.setter
    def IERS_number(self, value):
        if not (re.match(r"^[A-Z0-9]{9}$", value) or value == ""):
            raise ValueError("The IERS DOMES Number must be 9 characters long!")
        self._data["IERS DOMES Number"] = value

    @property
    def CDP_number(self):
        return self._data["CDP Number"]

    @CDP_number.setter
    def CDP_number(self, value):
        if not (re.match(r"^[A-Z0-9]{4}$", value) or value == ""):
            raise ValueError("The CDP Number must be 4 characters long!")
        self._data["CDP Number"] = value

    @property
    def monument(self):
        return self._data["Monument Description"]

    @monument.setter
    def monument(self, value):
        self._data["Monument Description"] = value

    @property
    def monument_h(self):
        return self._data["Height of the Monument"]

    @monument_h.setter
    def monument_h(self, value):
        self._data["Height of the Monument"] = value

    @property
    def foundation(self):
        return self._data["Monument Foundation"]

    @foundation.setter
    def foundation(self, value):
        self._data["Monument Foundation"] = value

    @property
    def foundation_depth(self):
        return self._data["Foundation Depth"]

    @foundation_depth.setter
    def foundation_depth(self, value):
        self._data["Foundation Depth"] = value

    @property
    def marker(self):
        return self._data["Marker Description"]

    @marker.setter
    def marker(self, value):
        self._data["Marker Description"] = value

    @property
    def date(self):
        return self._data["Date Installed"]

    @date.setter
    def date(self, value):
        if not (re.match(r"^\d{4}\-\d\d\-\d\d", value) or value==""):
            raise ValueError("Date Installed must be of the format (CCYY-MM-DDThh:mmZ)")
        self._data["Date Installed"] = value

    @property
    def geologic(self):
        return self._data["Geologic Characteristic"]

    @geologic.setter
    def geologic(self, value):
        self._data["Geologic Characteristic"] = value

    @property
    def bedrock_type(self):
        return self._data["Bedrock Type"]

    @bedrock_type.setter
    def bedrock_type(self, value):
        if value.upper() not in ("IGNEOUS", "METAMORPHIC", "SEDIMENTARY", ""):
            raise ValueError(
                "The Bedrock Type must be IGNEOUS, METAMORPHIC or SEDIMENTARY"
            )
        self._data["Bedrock Type"] = value

    @property
    def bedrock_condition(self):
        return self._data["Bedrock Condition"]

    @bedrock_condition.setter
    def bedrock_condition(self, value):
        if value.upper() not in ("FRESH", "JOINTED", "WEATHERED", ""):
            raise ValueError(
                "The Bedrock Condition must be FRESH, JOINTED or WEATHERED"
            )
        self._data["Bedrock Condition"] = value

    @property
    def fracture(self):
        return self._data["Fracture Spacing"]

    @fracture.setter
    def fracture(self, value):
        if value not in ("1-10 cm", "11-50 cm", "51-200 cm", "over 200 cm", ""):
            raise ValueError(
                "The Fracture Spacing must be in the ranges 1-10 cm, 11-50 cm, 51-200 cm or over 200 cm"
            )
        self._data["Fracture Spacing"] = value

    @property
    def fault(self):
        return self._data["Fault zones nearby"]

    @fault.setter
    def fault(self, value):
        self._data["Fault zones nearby"] = value

    @property
    def distance(self):
        return self._data["Distance/activity"]

    @distance.setter
    def distance(self, value):
        self._data["Distance/activity"] = value

    @property
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        self.additional = _format_string(self.additional, "multilinevalue")
        self.distance = _format_string(self.distance, "multilinevalue")
        section_text = f"""

1.   Site Identification of the GNSS Monument

     Site Name                : {self.site_name}
     Four Character ID        : {self.site_code}
     Monument Inscription     : {self.inscription}
     IERS DOMES Number        : {self.IERS_number}
     CDP Number               : {self.CDP_number}
     Monument Description     : {self.monument}
       Height of the Monument : {self.monument_h}
       Monument Foundation    : {self.foundation}
       Foundation Depth       : {self.foundation_depth}
     Marker Description       : {self.marker}
     Date Installed           : {self.date}
     Geologic Characteristic  : {self.geologic}
       Bedrock Type           : {self.bedrock_type}
       Bedrock Condition      : {self.bedrock_condition}
       Fracture Spacing       : {self.fracture}
       Fault zones nearby     : {self.fault}
         Distance/activity    : {self.distance}
     Additional Information   : {self.additional}
"""

        return section_text
