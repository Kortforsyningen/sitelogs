from datetime import datetime
from sitelog import (
    SiteLog,
    GnssReceiver,
    MetInstrument,
    SensorType,
    AntennaType,
    Form,
    SiteIdentification,
    LocalTies,
    Tie,
    FrequencyStandard,
    Frequency,
    Collocation,
    CollocationInstrument,
    Header,
)
from sitelog.local_conditions import (
    LocalCondition,
    ConditionTypes,
)
#from sitelog.surveyedties import Tie
from sitelog.episodic_effects import Effect
from sitelog.contact_agency import (ContactAgency, ContactAgencies)
from sitelog.responsible_agency import (ResponsibleAgency, ResponsibleAgencies)
from sitelog.more_info import MoreInfo
#from sitelog.receiver import GnssReceiver


if __name__ == "__main__":
    # Læs fra en eksisterende sitelog
    sitelog = SiteLog("fyha_20161220.log")
    # ændr noget
    sitelog.header.code = "4422"
    sitelog.header.prepared_by = "Tanya"
    sitelog.meteorological
    sitelog.meteorological.add_section(MetInstrument(
        instrument=SensorType.TEMPERATURE,
        model="first"
    ))
    sitelog.collocation[1].status = "Mobile"
    sitelog.collocation.add_section(CollocationInstrument(
        instrumentation_type="GPS"
    ))
    sitelog.responsible_agency[1].contact_name = "SDFE"
    sitelog.responsible_agency[1].fax = "12345"
    sitelog.contact_agency[1].fax = "1111"
    sitelog.write("test.log")

    # Lav en ny fra scratch
    log2 = SiteLog()
    log2.header.code = "STAT"
    log2.form = Form(prepared_by = "Kristian Evers", date="2019-12-12")
    # log2.form.site_name = "Station station"
    # log2.form.site_code = "STAT"
    # log2.form.report_type = "NEW"
    #log2.form.date = "2020-02-05"

    log2.site_identification = SiteIdentification(
        site_name="Station station",
        site_code="STAT",
        bedrock_condition="FRESH",
        monument_h="3m"
        ) 

    log2.gnss.add_section(GnssReceiver(
        receiver_type="ReceiverReceiver"

    ))
    log2.gnss.add_section(GnssReceiver(
        receiver_type="Receiver3"
    ))
    # log2.gnss[0].receiver_type = "Receiver 1"
    # log2.gnss[1].receiver_type = "Receiver 2"
    log2.antenna.add_section(AntennaType(
        antenna_type="Antenna1",
        north = 2
        ))
    log2.antenna.add_section(AntennaType(
        antenna_type="Antenna2",
        north = 2
        ))
    log2.meteorological.add_section(MetInstrument(
        instrument=SensorType.WATERVAPOR,
        model="first",
        manufacturer="This"

    ))
    log2.meteorological.add_section(MetInstrument(
        instrument=SensorType.PRESSURE,
        model="second"
    ))
    log2.meteorological.add_section(MetInstrument(
        instrument=SensorType.HUMIDITY,
        model="third"
    ))
    log2.meteorological.add_section(MetInstrument(
        instrument=SensorType.TEMPERATURE
    ))
    log2.local_ties.add_section(Tie(
        marker_name="markers2",
        marker_domes="1123"
    ))
    log2.frequency.add_section(Frequency(
        standard_type="CESIUM"
    ))
    log2.collocation.add_section(CollocationInstrument(
        instrumentation_type="GPS"
    ))
    log2.local_conditions.add_section(LocalCondition(
        condition=ConditionTypes.MULTIPATH,
        source="Metal roof"
    ))
    log2.episodic_effects.add_section(Effect(
        date = "2019-11-12"
    ))
    log2.contact_agency = ContactAgencies(
        agency = "UPS"
    )
    log2.contact_agency.add_section(ContactAgency(
        contact_name="SDFE",
        fax="12345",
        primary_phone="54321"
    ))
    log2.responsible_agency = ResponsibleAgencies(
        agency = "UPS"
    )
    log2.responsible_agency.add_section(ResponsibleAgency(
        contact_name="SDFE",
        fax="12345",
        primary_phone="54321"
    ))

    log2.more_info = MoreInfo(
        primary_center="SDFE",
        graphic= """
AOAD/M_B  (Allen Osborne Design)

                         -----
                     /     +     \                      <-- 0.096 L2
                    |      +      |                     <-- 0.078 L1
  +-----------------+-------------+------------------+  <-- 0.070 TCR
  |                                                  |
  |                                                  |
  |                                                  |
  |                                                  |
  |                                                  |
  +-----------------+------x------+------------------+  <-- 0.000 ARP
                    |             |
                    +-------------+                     <-- -0.011
                          ||  ||

  <--                    0.351                     -->


ARP: Antenna Reference Point"""
    )
    # Det ville gøre det lettere at bruge koden hvis man kunne gøre sådan her:
    #
    #  log2.gnss[0] = GnssReceiver(
    #      receiver_type = 'Receiver 1',
    #      sat_sys = 'GPS+GLONASS',
    #      firmware = '3.2.5',
    #      cutoff = '12',
    #      additional = 'Dette er en super sej receiver...'
    #  )
    log2.write("test2.log")
