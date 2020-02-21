import re

from sitelog import _determine_line_type

class Section():
    #TODO: Handle subsections
    #TODO: Handle subsubsections

    def __init__(self):
        self.title = ''
        self.subtitle = ''
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
                    self.subtitle = re.sub(r'\s.*','',line)
                else:
                    self.subtitle = re.sub(r'^\d{1,2}\.|[\d{1,2}x]\s.*','',line)
                    self.title = re.findall(r'\s.*:',line)[0]
                line = re.sub(r'^[\d{1,2}\.]+[\dx]{1,2}','',line)
                (key, value) = [s.strip() for s in line.split(' : ')]
                self._data[key] = value

class SectionList():
#class for sections with subsections
    def __init__(self):
        #super().__init__()
        self._subsections = []
        self.subsection_type = None
        self.section_type = ''

    def __getitem__(self, index):
        return self._subsections[index]


    def __setitem__(self, index, value):
        try:
            value.subtitle = index+1
            self._subsections[index] = value
        except IndexError:
            if index == len(self._subsections):
                value.subtitle = index+1
                self._subsections.append(value)


    def read_lines(self, lines):
        sections = []
        for line_no, line in enumerate(lines):
            if _determine_line_type(line) == self.section_type:
                    sections.append(line_no)
            # index til subsection header

        for sec_no, subsection in enumerate(sections):
            s = self.subsection_type()
            s.subtitle = sec_no+1
            # if self.section_type == 'subsubsectionheader':
            #     s.subsubtitle == self.subsubtitle
            #     s.header_title == 'Humidity Sensor Model   :'

            if subsection == sections[-1]:
                s.read_lines(lines[subsection:]) 
            else:
                s.read_lines(lines[subsection:sections[sec_no+1]])

            self._subsections.append(s)

class SubSection(Section):
    #Class for subsections of SectionList
    def __init__(self):
        super().__init__()

