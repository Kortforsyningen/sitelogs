# """
# Start med at læse fra bunden hvor jeg har eksempler på hvordan man
# kan bruge SiteLog :-)
# """

import re
import pathlib
import datetime as dt


def _determine_line_type(line):
    if line.strip() == '':
        line_type = 'blank'
    elif re.match(r'^\d{1,2}\.\s', line):
        line_type = 'sectionheader'
    elif re.match(r'^\d{1,2}\.[\dx]{1,2}\s', line):
        line_type = 'subsectionheader'
    elif re.match(r'^\d{1,2}\.\d{1,2}\.[\dx]{1,2}\s', line):
        line_type = 'subsubsectionheader'
    elif re.match(r'^\s+.*\s:\s.+$', line):
        if re.match(r'^\s*:\s.*$', line):
            line_type = 'key_value_continued'
        elif re.match(r'^\s+[\S ]+\s:\s+$', line):
            line_type = 'key_value_empty'
        else:
            line_type = 'key_value'
    else:
        line_type = 'freeform'
    
    return line_type

class Section():
    #TODO: Handle subsections
    #TODO: Handle subsubsections

    def __init__(self):
        self.title = ''
        self.subtitle = []
        self.subsections = []
        self._data = {}

    def read_lines(self, lines):
        """
        Read data from a site log section
        """
        for line in lines:
            line_type = _determine_line_type(line)

            if line_type == 'blank':
                continue

            if line_type == 'sectionheader':
                self.title = line.strip()

            if line_type == 'key_value':
                (key, value) = [s.strip() for s in line.split(' : ')]
                self._data[key] = value
                previous_key = key

            if line_type == 'key_value_continued':
                (key, value) = line.split(' : ')
                self._data[previous_key] = self._data[previous_key] + ' ' + value.strip()

            if line_type == 'subsectionheader' or line_type == 'subsubsectionheader':
                if line_type == 'subsectionheader':
                    self.subtitle.append(re.sub(r'\s.*','',line))
                else:
                    self.subtitle.append(re.findall(r'^.*:',line)[0])
                line = re.sub(r'^[\d{1,2}\.]+[\dx]{1,2}','',line)
                (key, value) = [s.strip() for s in line.split(' : ')]
                self._data[key] = value



                


class Header():
    def __init__(self, code='XXXX'):
        if not re.match(r'^[A-Z0-9]{4}$', code):
            raise ValueError("The Four Character ID *must* be 4 characters long!")
        self.code = code

    def string(self):
        text=f"""
     {self.code} Site Information Form (site log)
     International GNSS Service
     See Instructions at:
       ftp://igs.org/pub/station/general/sitelog_instr.txt
"""
        return text

class Form(Section):
    
    def __init__(self):
        self._data = self._template_dict()

    def _template_dict(self):
        data = {
            "Prepared by (full name)": "",
            "Date Prepared": "(CCYY-MM-DD)",
            "Report Type": "(NEW/UPDATE)",
            "Update:" : "",
            "Previous Site Log": "(ssss_ccyymmdd.log)",
            "Modified/Added Sections" : "(n.n,n.n,...)",
        }
        return data


    @property
    def prepared_by(self):
        return self._data["Prepared by (full name)"] 

    @prepared_by.setter
    def prepared_by(self, value):
        self._data["Prepared by (full name)"] = value

    @property
    def site_name(self):
        return self._data['Site Name']

    @site_name.setter
    def site_name(self, value):
        self._data['Site Name'] = value

    @property
    def date(self):
        return self._data['Date Prepared']

    @date.setter
    def date(self, value):
        self._data['Date Prepared'] = value

    @property
    def report_type(self):
        return self._data['Report Type']

    @report_type.setter
    def report_type(self, value):
        if value not in ('NEW', 'UPDATE'):
            raise ValueError("Report type can only be set to 'NEW' or 'UPDATE'")
        self._data['Report Type'] = value

    @property
    def previous_log(self):
        return self._data['Previous Site Log']

    @previous_log.setter
    def previous_log(self, value):
        self._data['Previous Site Log'] = value

    @property
    def changed_sections(self):
        return self._data['Modified/Added Sections']

    @changed_sections.setter
    def changed_sections(self, value):
        self._data['Modified/Added Sections'] = value

    def string(self):
        text = f"""
0.   Form

     Prepared by (full name)  : {self.prepared_by}
     Date Prepared            : {self.date}
     Report Type              : {self.report_type}
"""
        update = ""
        if self.report_type == "UPDATE":
            update = f"""
     Update:
      Previous Site Log       : {self.previous_log}
      Modified/Added Sections : {self.changed_sections}"""

        return text.rstrip()+update

class SiteIdentification(Section):

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

    def __init__(self):
        self._data = self._template_dict()

    @property
    def site_name(self):
        return self._data['Site Name']

    @site_name.setter
    def site_name(self, value):
        self._data['Site Name'] = value

    @property
    def site_code(self):
        return self._data['Four Character ID']

    @site_code.setter
    def site_code(self, value):
        if not re.match(r'^[A-Z0-9]{4}$', value):
            raise ValueError("The Four Character ID *must* be 4 characters long!")
        self._data['Four Character ID'] = value

    @property
    def inscription(self):
        return self._data['Monument Inscription']

    @inscription.setter
    def inscription(self, value):
        self._data['Monument Inscription'] = value

    @property
    def IERS_number(self):
        return self._data['IERS DOMES Number']

    @IERS_number.setter
    def IERS_number(self, value):
        if not re.match(r'^[A-Z0-9]{9}$', value):
            raise ValueError("The IERS DOMES Number must be 9 characters long!")
        self._data['IERS DOMES Number'] = value

    @property
    def CDP_number(self):
        return self._data['CDP Number']

    @CDP_number.setter
    def CDP_number(self, value):
        if not re.match(r'^[A-Z0-9]{4}$', value) or value == "":
            raise ValueError("The CDP Number must be 4 characters long!")
        self._data['CDP Number'] = value

    @property
    def monument(self):
        return self._data['Monument Description']

    @monument.setter
    def monument(self, value):
        self._data['Monument Description'] = value

    @property
    def monument_h(self):
        return self._data['Height of the Monument']

    @monument_h.setter
    def monument_h(self, value):
        self._data['Height of the Monument'] = value

    @property
    def foundation(self):
        return self._data['Monument Foundation']

    @foundation.setter
    def foundation(self, value):
        self._data['Monument Foundation'] = value

    @property
    def foundation_depth(self):
        return self._data['Foundation Depth']

    @foundation_depth.setter
    def foundation_depth(self, value):
        self._data['Foundation Depth'] = value

    @property
    def marker(self):
        return self._data['Marker Description']

    @marker.setter
    def marker(self, value):
        self._data['Marker Description'] = value        

    @property
    def date(self):
        return self._data['Date Installed']

    @date.setter
    def date(self, value):
        if not re.match(r'^\d{4}\-\d\d\-\d\d', value):
            raise ValueError("Date Installed must be of the format (CCYY-MM-DDThh:mmZ)")
        self._data['Date Installed'] = value    

    @property
    def geologic(self):
        return self._data['Geologic Characteristic']

    @geologic.setter
    def geologic(self, value):
        self._data['Geologic Characteristic'] = value

    @property
    def bedrock_type(self):
        return self._data['Bedrock Type']

    @bedrock_type.setter
    def bedrock_type(self, value):
        if not value == 'IGNEOUS' or value == 'METAMORPHIC' or value == 'SEDIMENTARY':
            raise ValueError("The Bedrock Type must be IGNEOUS, METAMORPHIC or SEDIMENTARY")
        self._data['Bedrock Type'] = value 

    @property
    def bedrock_condition(self):
        return self._data['Bedrock Condition']

    @bedrock_condition.setter
    def bedrock_condition(self, value):
        if not value == 'FRESH' or value == 'JOINTED' or value == 'WEATHERED':
            raise ValueError("The Bedrock Condition must be FRESH, JOINTED or WEATHERED")
        self._data['Bedrock Condition'] = value 

    @property
    def fracture(self):
        return self._data['Fracture Spacing']

    @fracture.setter
    def fracture(self, value):
        if not value == '1-10 cm' or value == '11-50 cm' or value == '51-200 cm' or value == 'over 200 cm':
            raise ValueError("The Fracture Spacing must be in the ranges 1-10 cm, 11-50 cm, 51-200 cm or over 200 cm")
        self._data['Fracture Spacing'] = value 

    @property
    def fault(self):
        return self._data['Fault zones nearby']

    @fault.setter
    def fault(self, value):
        self._data['Fault zones nearby'] = value

    @property
    def distance(self):
        return self._data['Distance/activity']

    @distance.setter
    def distance(self, value):
        self._data['Distance/activity'] = value

    @property
    def additional(self):
        return self._data['Additional Information']

    @additional.setter
    def additional(self, value):
        self._data['Additional Information'] = value


    def string(self):

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

class SiteLocation(Section):

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

class GnssReceiver(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subtitle = []
        self.title = '' 
        self.number = None

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
        return self._data['Receiver Type']

    @receiver_type.setter
    def receiver_type(self, value):
        self._data['Receiver Type'] = value

    @property
    def sat_sys(self):
        return self._data['Satellite System']

    @sat_sys.setter
    def sat_sys(self, value):
        self._data['Satellite System'] = value


    @property
    def firmware(self):
        return self._data['Firmware Version']

    @firmware.setter
    def firmware(self, value):
        self._data['Firmware Version'] = value

    @property
    def cutoff(self):
        return self._data['Elevation Cutoff Setting']

    @cutoff.setter
    def cutoff(self, value):
        self._data['Elevation Cutoff Settingn'] = value

    @property
    def additional(self):
        return self._data['Additional Information']

    @additional.setter
    def additional(self, value):
        self._data['Additional Information'] = value

    def string(self):

        section_text = f"""
3.{self.title}  Receiver Type            : {self.receiver_type}
     Satellite System         : {self.sat_sys}
     Serial Number            : (A20, but note the first A5 is used in SINEX)
     Firmware Version         : {self.firmware}
     Elevation Cutoff Setting : {self.cutoff}
     Date Installed           : (CCYY-MM-DDThh:mmZ)
     Date Removed             : (CCYY-MM-DDThh:mmZ)
     Temperature Stabiliz.    : (none or tolerance in degrees C)
     Additional Information   : {self.additional}

"""
        return section_text

class GNSS(Section):
    def __init__(self):
        self._data = self._template_dict
        self._subsections = []
        self.title = []


    def __getitem__(self, index):
        return self._subsections[index]


    def __setitem__(self, index, value):
        try:
            value.title = index+1
            self._subsections[index] = value
        except IndexError:
            if index == len(self._subsections):
                value.title = index+1
                self._subsections.append(value)

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

    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == 'subsectionheader':
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = GnssReceiver()
            s.title = sec_no+1
            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self._subsections.append(s)


    def string(self):

        section_text = f"""
3.   GNSS Receiver Information
"""
        if self._subsections:
            for subsection in self._subsections:
                section_text += subsection.string() 
        else:
            s = GnssReceiver()
            s.subtitle = ['3.x']
            section_text += s.string()
        return section_text

class AntennaType(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subtitle = [] 
        self.number = None

    def _template_dict(self):
        data = {
            "Antenna Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Serial Number": "(A*, but note the first A5 is used in SINEX)",
            "Antenna Reference Point": "(BPA/BCR/XXX from \"antenna.gra\"; see instr.)",
            "Marker->ARP Up Ecc. (m)": "(F8.4)",
            "Marker->ARP North Ecc(m)": "(F8.4)",
            "Marker->ARP East Ecc(m)": "(F8.4)",
            "Alignment from True N": "(deg; + is clockwise/east)",
            "Antenna Radome Type": "(A4 from rcvr_ant.tab; see instructions)",
            "Radome Serial Number": "",
            "Antenna Cable Type": "(vendor & type number)",
            "Antenna Cable Length": "(m)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Date Removed": "(CCYY-MM-DDThh:mmZ)",
            "Additional Information": "(multiple lines)",

        }
        return data


    def string(self):

        section_text = f"""
{self.subtitle[0]}  Antenna Type             : (A20, from rcvr_ant.tab; see instructions)
     Serial Number            : (A*, but note the first A5 is used in SINEX)
     Antenna Reference Point  : (BPA/BCR/XXX from "antenna.gra"; see instr.)
     Marker->ARP Up Ecc. (m)  : (F8.4)
     Marker->ARP North Ecc(m) : (F8.4)
     Marker->ARP East Ecc(m)  : (F8.4)
     Alignment from True N    : (deg; + is clockwise/east)
     Antenna Radome Type      : (A4 from rcvr_ant.tab; see instructions)
     Radome Serial Number     : 
     Antenna Cable Type       : (vendor & type number)
     Antenna Cable Length     : (m)
     Date Installed           : (CCYY-MM-DDThh:mmZ)
     Date Removed             : (CCYY-MM-DDThh:mmZ)
     Additional Information   : (multiple lines) 
"""
        return section_text

class Antenna(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subsections = []
        self.title = []

    def _template_dict(self):
        data = {
            "Antenna Type": "(A20, from rcvr_ant.tab; see instructions)",
            "Serial Number": "(A*, but note the first A5 is used in SINEX)",
            "Antenna Reference Point": "(BPA/BCR/XXX from \"antenna.gra\"; see instr.)",
            "Marker->ARP Up Ecc. (m)": "(F8.4)",
            "Marker->ARP North Ecc(m)": "(F8.4)",
            "Marker->ARP East Ecc(m)": "(F8.4)",
            "Alignment from True N": "(deg; + is clockwise/east)",
            "Antenna Radome Type": "(A4 from rcvr_ant.tab; see instructions)",
            "Radome Serial Number": "",
            "Antenna Cable Type": "(vendor & type number)",
            "Antenna Cable Length": "(m)",
            "Date Installed": "(CCYY-MM-DDThh:mmZ)",
            "Date Removed": "(CCYY-MM-DDThh:mmZ)",
            "Additional Information": "(multiple lines)",

        }
        return data

    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == 'subsectionheader':
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = AntennaType()
            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self.subsections.append(s)


    def string(self):

        section_text = f"""
4.   GNSS Antenna Information
"""
        if self.subsections:
            for subsection in self.subsections:
                section_text += subsection.string() 
        else:
            s = AntennaType()
            s.subtitle = ['4.x']
            section_text += s.string()
        return section_text

class Tie(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subtitle = [] 
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
{self.subtitle[0]}  Tied Marker Name         : 
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

class LocalTies(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subsections = []
        self.title = []

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

    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == 'subsectionheader':
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = Tie()
            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self.subsections.append(s)


    def string(self):

        section_text = f"""
5.   Surveyed Local Ties
"""
        if self.subsections:
            for subsection in self.subsections:
                section_text += subsection.string() 
        else:
            s = Tie()
            s.subtitle = ['5.x']
            section_text += s.string()
        return section_text

class Frequency(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subtitle = [] 
        self.number = None

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
{self.subtitle[0]}  Standard Type            : (INTERNAL or EXTERNAL H-MASER/CESIUM/etc)
       Input Frequency        : (if external)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
"""
        return section_text

class FrequencyStandard(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subsections = []
        self.title = []

    def _template_dict(self):
        data = {
            "Standard Type": "(INTERNAL or EXTERNAL H-MASER/CESIUM/etc)",
            "Input Frequency": "(if external)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == 'subsectionheader':
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = Frequency()
            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self.subsections.append(s)


    def string(self):

        section_text = f"""
6.   Frequency Standard
"""
        if self.subsections:
            for subsection in self.subsections:
                section_text += subsection.string() 
        else:
            s = Frequency()
            s.subtitle = ['6.x']
            section_text += s.string()
        return section_text

class CollocationInstrument(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subtitle = [] 
        self.number = None

    def _template_dict(self):
        data = {
            "Instrumentation Type": "(GPS/GLONASS/DORIS/PRARE/SLR/VLBI/TIME/etc)",
            "Status": "(PERMANENT/MOBILE)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    def string(self):

        section_text = f"""
{self.subtitle[0]}  Instrumentation Type     : (GPS/GLONASS/DORIS/PRARE/SLR/VLBI/TIME/etc)
       Status                 : (PERMANENT/MOBILE)
       Effective Dates        : (CCYY-MM-DD/CCYY-MM-DD)
       Notes                  : (multiple lines)
"""
        return section_text

class Collocation(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subsections = []
        self.title = []

    def _template_dict(self):
        data = {
            "Instrumentation Type": "(GPS/GLONASS/DORIS/PRARE/SLR/VLBI/TIME/etc)",
            "Status": "(PERMANENT/MOBILE)",
            "Effective Dates": "(CCYY-MM-DD/CCYY-MM-DD)",
            "Notes": "(multiple lines)",
        }
        return data

    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == 'subsectionheader':
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = CollocationInstrument()
            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self.subsections.append(s)


    def string(self):

        section_text = f"""
7.   Collocation Information
"""
        if self.subsections:
            for subsection in self.subsections:
                section_text += subsection.string() 
        else:
            s = CollocationInstrument()
            s.subtitle = ['7.x']
            section_text += s.string()
        return section_text


class MetInstrument(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subtitle = [] 
        self.number = None

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
        return self._data[re.sub(r'\d{1,2}\.\d{1,2}\.[\dx]{1,2}\s|\s*:', '',self.subtitle[0])]

    @header_val.setter
    def header_val(self, value):
        self._data[re.sub(r'\d{1,2}\.\d{1,2}\.[\dx]{1,2}\s|\s*:', '',self.subtitle[0])] = value

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
        if re.match(r'^8\.5\.[\dx]+.+:$', self.subtitle[0]):
            section_text = f"""
{self.subtitle[0]} {self.other}
    """
        else:
            section_text = f"""
{self.subtitle[0]} {self.header_val}
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

class Meterological(Section):
    def __init__(self):
        self._data = self._template_dict()
        self.subsections = []
        self.title = []

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

    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == 'subsubsectionheader':
                    sections.append(line_no)
            # index til subsubsection header

        for sec_no, subsection in enumerate(sections):
            s = MetInstrument()
            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self.subsections.append(s)


    def string(self):

        section_text = f"""
8.   Meteorological Instrumentation
"""
        if self.subsections:
            for subsection in self.subsections:
                section_text += subsection.string() 
        else:
            subsubtitles = ['8.1.x Humidity Sensor Model   :', '8.2.x Pressure Sensor Model   :', '8.3.x Temp. Sensor Model      :', '8.4.x Water Vapor Radiometer  :', '8.5.x Other Instrumentation   :']
            for subsubtitle in subsubtitles:
                s = MetInstrument()
                s.subtitle = [subsubtitle]
                section_text += s.string()
        return section_text

class SiteLog():

    def __init__(self, sitelogfile=None):
        
        self.logfile = sitelogfile
        self.header = Header()
        self.form = Form()
        self.site_identification = SiteIdentification()
        self.site_location = SiteLocation()
        self.gnss = GNSS()
        self.antenna = Antenna()
        self.local_ties = LocalTies()
        self.frequency = FrequencyStandard()
        self.collocation = Collocation()
        self.meterological = Meterological()
        if sitelogfile is not None:
            self._read()

    def _read(self):
        with open(self.logfile, 'r') as sl:
            lines = sl.read().splitlines()
            sections = []
            for line_no, line in enumerate(lines):
                if _determine_line_type(line) == 'sectionheader':
                    sections.append(line_no)

            self.header.code = re.findall(r'\s+([A-Z0-9]{4})', lines[0])[0]
            self.form.read_lines(lines[sections[0]:sections[1]])
            self.site_identification.read_lines(lines[sections[1]:sections[2]])
            self.site_location.read_lines(lines[sections[2]:sections[3]])
            self.gnss.read_lines(lines[sections[3]:sections[4]])
            self.antenna.read_lines(lines[sections[4]:sections[5]])
            self.local_ties.read_lines(lines[sections[5]:sections[6]])
            self.frequency.read_lines(lines[sections[6]:sections[7]])
            self.collocation.read_lines(lines[sections[7]:sections[8]])
            self.meterological.read_lines(lines[sections[8]:sections[9]])



    def write(self, sitelogfile):
        with open(sitelogfile, 'w') as f:
            f.write(self.header.string())
            f.write(self.form.string())
            f.write(self.site_identification.string())
            f.write(self.site_location.string())
            f.write(self.gnss.string())
            f.write(self.antenna.string())
            f.write(self.local_ties.string())
            f.write(self.frequency.string())
            f.write(self.collocation.string())
            f.write(self.meterological.string())


if __name__ == "__main__":
    # Læs fra en eksisterende sitelog
    sitelog = SiteLog('fyha_20161220.log')
    # ændr noget
    sitelog.header.code = 'FLAF'
    sitelog.write('test.log')

    # Lav en ny fra scratch
    log2 = SiteLog()
    log2.header.code = 'STAT'
    log2.form.prepared_by = 'Kristian Evers'
    log2.form.site_name = 'Station station'
    log2.form.site_code = 'STAT'
    log2.form.report_type = 'NEW'
    log2.form.date = '2020-02-05'

    log2.site_identification.date = '2020-02-05'
    log2.site_identification.bedrock_condition = 'FRESH'
    log2.gnss[0] = GnssReceiver()
    log2.gnss[1] = GnssReceiver()
    log2.gnss[0].receiver_type = 'Receiver 1'
    log2.gnss[1].receiver_type = 'Receiver 2'
    # Det ville gøre det lettere at bruge koden hvis man kunne gøre sådan her:
    #
    #  log2.gnss[0] = GnssReceiver(
    #      receiver_type = 'Receiver 1',
    #      sat_sys = 'GPS+GLONASS',
    #      firmware = '3.2.5',
    #      cutoff = '12',
    #      additional = 'Dette er en super sej receiver...'
    #  )
    log2.write('test2.log')


