import pyasdf

asdf="../seis/proc/run0001.T090-250s.proc_synt.h5"
ds = pyasdf.ASDFDataSet(asdf, mode='r')
    
inv=ds.waveforms[ds.waveforms.list()[0]].StationXML

print(inv)

for nw in inv:
    nw_code = nw.code
    print(nw.code)
    for sta in nw:
        sta_code = sta.code
        print(sta.code)
        for chan in sta:
            chan_code = chan.code
            print(chan.code)
            if (chan.code[:2] == "MX"):
                print ("hello")
            print(chan.sensor.description)
     #     loc_code = chan.location_code
     #     key = "%s.%s.%s.%s" % (nw_code, sta_code, loc_code, chan_code)
     #     print(key)
     #     instruments[key]["latitude"] = chan.latitude
     #     instruments[key]["longitude"] = chan.longitude
     #     instruments[key]["elevation"] = chan.elevation
     #     instruments[key]["depth"] = chan.depth
del ds
