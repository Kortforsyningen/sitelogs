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
import sitelog.local_conditions as local_conditions
import sitelog.episodic_effects as episodic_effects
import sitelog.contact_agency as contact_agency
import sitelog.responsible_agency as responsible_agency
import sitelog.more_info as more_info


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
        self.local_conditions = local_conditions.Conditions()
        self.episodic_effects = episodic_effects.EpisodicEffects()
        self.contact_agency = contact_agency.ContactAgencies()
        self.responsible_agency = responsible_agency.ResponsibleAgencies()
        self.more_info = more_info.MoreInfo()
        if sitelogfile is not None:
            self._read()

    def _read(self):
        with open(self.logfile, "r") as sl:
            lines = sl.read().splitlines()
            sections = []
            for line_no, line in enumerate(lines):
                if _determine_line_type(line) == "sectionheader":
                    sections.append(line_no)
            for line in lines[0:4]:
                if re.findall(r"\s+([A-Z0-9]{4,9})", line):
                    self.header.code = re.findall(r"\s+([A-Z0-9]{4,9})", line)[0]
                    break

            self.form.read_lines(lines[sections[0] : sections[1]])
            self.site_identification.read_lines(lines[sections[1] : sections[2]])
            self.site_location.read_lines(lines[sections[2] : sections[3]])
            self.gnss.read_lines(lines[sections[3] : sections[4]])
            self.antenna.read_lines(lines[sections[4] : sections[5]])
            self.local_ties.read_lines(lines[sections[5] : sections[6]])
            self.frequency.read_lines(lines[sections[6] : sections[7]])
            self.collocation.read_lines(lines[sections[7] : sections[8]])
            self.meteorological.read_lines(lines[sections[8] : sections[9]])
            self.local_conditions.read_lines(lines[sections[9] : sections[10]])
            self.episodic_effects.read_lines(lines[sections[10] : sections[11]])
            self.contact_agency.read_lines(lines[sections[11] : sections[12]])
            self.responsible_agency.read_lines(lines[sections[12] : sections[13]])
            self.more_info.read_lines(lines[sections[13] :])

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
            f.write(self.local_conditions.string())
            f.write(self.episodic_effects.string())
            f.write(self.contact_agency.string())
            f.write(self.responsible_agency.string())
            f.write(self.more_info.string())
