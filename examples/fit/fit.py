#! /usr/bin/env python

# Load a profile histo
import yoda
aos = yoda.read("./yoda/fit.yoda")
h = aos["/RivetHbbBJets/h2_PTmt_PTnm_0"]
assert type(h) is yoda.Histo2D

print "integral",h.integral()
print "numEntries",h.numEntries()
print "sumW",h.sumW()
#print "xMean",h.xMean()

bins=h.bins()


exit()
for b in h.bins():
    print b



