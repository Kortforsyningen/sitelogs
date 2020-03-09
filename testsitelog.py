from sitelog import (
    SiteLog,
    GnssReceiver,
    MetInstrument,
    SensorType,
    AntennaType,
)
from sitelog.local_conditions import (
    LocalCondition,
    ConditionTypes,
)

from sitelog.episodic_effects import Effect
from sitelog.contact_agency import ContactAgency
from sitelog.responsible_agency import ResponsibleAgency


if __name__ == "__main__":
    # Læs fra en eksisterende sitelog
    sitelog = SiteLog("fyha_20161220.log")
    # ændr noget
    sitelog.header.code = "FLAF"
    sitelog.collocation[0].status = "Mobile"
    sitelog.contact_agency[1].fax = "1111"
    sitelog.write("test.log")

    # Lav en ny fra scratch
    log2 = SiteLog()
    log2.header.code = "STAT"
    log2.form.prepared_by = "Kristian Evers"
    log2.form.site_name = "Station station"
    log2.form.site_code = "STAT"
    log2.form.report_type = "NEW"
    log2.form.date = "2020-02-05"

    log2.site_identification.date = "2020-02-05"
    log2.site_identification.bedrock_condition = "FRESH"
    log2.gnss[0] = GnssReceiver()
    log2.gnss[1] = GnssReceiver()
    log2.gnss[0].receiver_type = "Receiver 1"
    log2.gnss[1].receiver_type = "Receiver 2"
    log2.antenna[0] = AntennaType()
    log2.antenna[0].up = 222
    log2.meteorological[0] = MetInstrument()
    log2.meteorological[1] = MetInstrument()
    log2.meteorological[2] = MetInstrument()
    log2.meteorological[3] = MetInstrument()
    log2.meteorological[1].model = "second."
    log2.meteorological[0].instrument = SensorType.HUMIDITY
    #    log2.meteorological[0].instrument = 'Humidity Sensor Model'
    log2.meteorological[2].instrument = SensorType.WATERVAPOR
    log2.meteorological[3].instrument = SensorType.HUMIDITY
    log2.meteorological[0].model = "first"
    log2.meteorological[2].model = "third"
    log2.meteorological[3].model = "fourth"
    log2.local_conditions[0] = LocalCondition()
    log2.local_conditions[0].condition = ConditionTypes.MULTIPATH
    log2.local_conditions[0].dates = "2020-12-12"
    log2.episodic_effects[0] = Effect()
    log2.episodic_effects[0].date = "2019-12-12"
    log2.contact_agency.agency = "SDFE"
    log2.contact_agency[0] = ContactAgency()
    log2.contact_agency[0].contact_name = "SDFE"
    log2.contact_agency[1] = ContactAgency()
    log2.contact_agency[1].contact_name = "SDFE1"
    log2.responsible_agency[0] = ResponsibleAgency()
    log2.responsible_agency[0].fax = "13212312"
    log2.more_info.graphic = """
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
