#! /usr/bin/env python

# Load a profile histo
import yoda
aos = yoda.read("./yoda/ZHvvbb.yoda")

do_h1=0
do_h2=0
do_p1=1

if do_h1:
    h = aos["/RivetHbbBJets/h1_PTnm_0"]
    assert type(h) is yoda.Histo1D 
    bins=h.bins
    print bins

if do_h2:
    h = aos["/RivetHbbBJets/h2_PTmt_PTnm_0"]
    assert type(h) is yoda.Histo2D 
    bins=h.bins
    print bins

if do_p1:
    h = aos["/RivetHbbBJets/p1_PTmt_PTnm_0"]
    assert type(h) is yoda.Profile1D 
    bins=h.bins
    print bins

#aos = yoda.read("./yoda/ZHvvbb2.yoda")
#p = aos["/RivetHbbBJets/p1_PTm_PTnm"]
#assert type(p) is yoda.Profile1D

exit()

#aos = yoda.read("./yoda/ZHvvbb.yoda")
#h = aos["/RivetHbbBJets/h1_PTa"]
#assert type(h) is yoda.Histo1D


h = aos["/RivetHbbBJets/h2_PTmt_PTnm_0"]
assert type(h) is yoda.Histo2D

print h.integral()
print h.numEntries()
print h.sumW()
print h.xMean


