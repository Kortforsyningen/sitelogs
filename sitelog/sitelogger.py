import re
import pathlib
import datetime as dt

from sitelog import _determine_line_type
import sitelog.header_form as header_form
import sitelog.siteidentification as siteidentification
import sitelog.sitelocation as sitelocation
import sitelog.receiver as receiver
import sitelog.antenna as antenna
import sitelog.surveyedties as surveyedties
import sitelog.frequencystandard as frequencystandard
import sitelog.collocation as collocation
import sitelog.meteorologicalinstruments as meteorologicalinstruments


class SiteLog:
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
        self.meteorological = meteorologicalinstruments.Meteorological()
        if sitelogfile is not None:
            self._read()

    def _read(self):
        with open(self.logfile, "r") as sl:
            lines = sl.read().splitlines()
            sections = []
            for line_no, line in enumerate(lines):
                if _determine_line_type(line) == "sectionheader":
                    sections.append(line_no)

            self.header.code = re.findall(r"\s+([A-Z0-9]{4})", lines[0])[0]
            self.form.read_lines(lines[sections[0] : sections[1]])
            self.site_identification.read_lines(lines[sections[1] : sections[2]])
            self.site_location.read_lines(lines[sections[2] : sections[3]])
            self.gnss.read_lines(lines[sections[3] : sections[4]])
            self.antenna.read_lines(lines[sections[4] : sections[5]])
            self.local_ties.read_lines(lines[sections[5] : sections[6]])
            self.frequency.read_lines(lines[sections[6] : sections[7]])
            self.collocation.read_lines(lines[sections[7] : sections[8]])
            self.meteorological.read_lines(lines[sections[8] : sections[9]])

    def write(self, sitelogfile):
        with open(sitelogfile, "w") as f:
            f.write(self.header.string())
            f.write(self.form.string())
            f.write(self.site_identification.string())
            f.write(self.site_location.string())
            f.write(self.gnss.string())
            f.write(self.antenna.string())
            f.write(self.local_ties.string())
            f.write(self.frequency.string())
            f.write(self.collocation.string())
            f.write(self.meteorological.string())
