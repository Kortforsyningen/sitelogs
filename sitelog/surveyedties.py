import sitelog.sitelogger as sitelogger
import re

class Tie(sitelogger.SubSection):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.number = None

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
5.{self.title}  Tied Marker Name         : 
     Tied Marker Usage        : (SLR/VLBI/LOCAL CONTROL/FOOTPRINT/etc)
     Tied Marker CDP Number   : (A4)
     Tied Marker DOMES Number : (A9)
     Differential Components from GNSS Marker to the tied monument (ITRS)
       dx (m)                 : (m)
       dy (m)                 : (m)
       dz (m)                 : (m)
     Accuracy (mm)            : (mm)
     Survey method            : (GPS CAMPAIGN/TRILATERATION/TRIANGULATION/etc)
     Date Measured            : (CCYY-MM-DDThh:mmZ)
     Additional Information   : (multiple lines)
"""
        return section_text

class LocalTies(sitelogger.SectionList):
    def __init__(self):
        super().__init__()
        self._data = self._template_dict()
        self.subsection_type = Tie
        self.section_type = 'subsectionheader'

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
            s.subtitle = ['5.x']
            section_text += s.string()
        return section_text
