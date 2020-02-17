
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

class SectionList(Section):
#class for sections with subsections
    def __init__(self):
        self.subsubtitle = ''
        super().__init__()
        self._subsections = []
        self.subsection_type = None
        self.section_type = ''

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
                
    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == self.section_type:
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = self.subsection_type()
            s.title = sec_no+1
            if self.section_type == 'subsubsectionheader':
                s.subsubtitle == self.subsubtitle
                s.header_title == 'Humidity Sensor Model   :'

            if subsection == sections[-1]:
                s.read_lines(lines[subsection:])
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])
            self._subsections.append(s)

class SubSection(Section):
    #Class for subsections of SectionList
    def __init__(self):
        super().__init__()

import sitelog.header_form as header_form
import sitelog.siteidentification as siteidentification
import sitelog.sitelocation as sitelocation
import sitelog.receiver as receiver
import sitelog.antenna as antenna
import sitelog.surveyedties as surveyedties
import sitelog.frequencystandard as frequencystandard
import sitelog.collocation as collocation
import sitelog.meterologicalinstruments as meterologicalinstruments

class SiteLog():

    def __init__(self, sitelogfile=None):
        
        self.logfile = sitelogfile
        self.header = header_form.Header()
        self.form = header_form.Form()
        self.site_identification = siteidentification.SiteIdentification()
        self.site_location = sitelocation.SiteLocation()
        self.gnss = receiver.GNSS()
        self.antenna = antenna.Antenna()
        self.local_ties = surveyedties.LocalTies()
        self.frequency = frequencystandard.FrequencyStandard()
        self.collocation = collocation.Collocation()
        self.humidity = meterologicalinstruments.Humidity()
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
            self.humidity.read_lines(lines[sections[8]:sections[9]])



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
            f.write(self.humidity.string())


