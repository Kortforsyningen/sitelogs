from sitelog import (
    SiteLog,
    GnssReceiver,
    MetInstrument,
    SensorType,
)

if __name__ == "__main__":
    # Læs fra en eksisterende sitelog
    sitelog = SiteLog("fyha_20161220.log")
    # ændr noget
    sitelog.header.code = "FLAF"
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
