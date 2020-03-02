from sitelog.sections import (
    SubSection,
    SectionListHeader,
    Section,
)
from sitelog import _format_string


class ResponsibleAgency(Section):
    def __init__(self):
        self._data = self._template_dict()

    def _template_dict(self):
        data = {
            "Contact Name": "",
            "Telephone (primary)": "",
            "Telephone (secondary)": "",
            "Fax": "",
            "E-mail": "",
        }
        return data

    @property
    def contact_name(self):
        return self._data["Contact Name"]

    @contact_name.setter
    def contact_name(self, value):
        self._data["Contact Name"] = value

    @property
    def primary_phone(self):
        return self._data["Telephone (primary)"]

    @primary_phone.setter
    def primary_phone(self, value):
        self._data["Telephone (primary)"] = value

    @property
    def secondary_phone(self):
        return self._data["Telephone (secondary)"]

    @secondary_phone.setter
    def secondary_phone(self, value):
        self._data["Telephone (secondary)"] = value

    @property
    def fax(self):
        return self._data["Fax"]

    @fax.setter
    def fax(self, value):
        self._data["Fax"] = value

    @property
    def email(self):
        return self._data["E-mail"]

    @email.setter
    def email(self, value):
        self._data["E-mail"] = value

    def string(self):
        section_text = f"""
{self.subtitle}
       Contact Name           : {self.contact_name}
       Telephone (primary)    : {self.primary_phone}
       Telephone (secondary)  : {self.secondary_phone}
       Fax                    : {self.fax}
       E-mail                 : {self.email}"""
        return section_text


class ResponsibleAgencies(SectionListHeader):
    def __init__(self):
        super().__init__()
        self.subsection_type = ResponsibleAgency
        self.section_type = "subsectionheader"  # subsection
        self._data = self._template_dict()

    def _template_dict(self):
        data = {
            "Agency": "(multiple lines)",
            "Preferred Abbreviation": "(A10)",
            "Mailing Address": "(multiple lines)",
            "Additional Information": "(multiple lines)",
        }
        return data

    @property
    def agency(self):
        return self._data["Agency"]

    @agency.setter
    def agency(self, value):
        self._data["Agency"] = value

    @property
    def abbreviation(self):
        return self._data["Preferred Abbreviation"]

    @abbreviation.setter
    def abbreviation(self, value):
        self._data["Preferred Abbreviation"] = value

    @property
    def address(self):
        return self._data["Mailing Address"]

    @address.setter
    def address(self, value):
        self._data["Mailing Address"] = value

    @property
    def additional(self):
        return self._data["Additional Information"]

    @additional.setter
    def additional(self, value):
        self._data["Additional Information"] = value

    def string(self):
        if self.header:
            self._data = self.header._data
        self.agency = _format_string(self.agency, "multilinevalue")
        self.address = _format_string(self.address, "multilinevalue")
        self.additional = _format_string(self.additional, "multilinevalue")
        s = []
        section_text = f"""
12.  Responsible Agency (if different from 11.)

     Agency                   : {self.agency}
     Preferred Abbreviation   : {self.abbreviation}
     Mailing Address          : {self.address}"""
        s.append(self.subsection_type())
        s.append(self.subsection_type())
        if self._subsections:
            s[0] = self._subsections[0]
            if len(self._subsections) == 2:
                s[1] = self._subsections[1]

        s[0].subtitle = "     Primary Contact"
        section_text += s[0].string()
        s[1].subtitle = "     Secondary Contact"
        section_text += s[1].string()
        section_text += f"""
     Additional Information   : {self.additional}
        """
        return section_text
