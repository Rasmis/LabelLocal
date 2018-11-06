#!/usr/bin/python

import os
import subprocess
	
def getCmd(cmd):
    output = ""
    returncode = 0
    try:
      output = subprocess.check_output(cmd, shell=True).strip()
    except subprocess.CalledProcessError as grepexc:                                                                                                   
      #print( "error code", grepexc.returncode, grepexc.output)
      output = grepexc.output
      returncode = grepexc.returncode
    return output.decode("ascii"), returncode


#ability to parse mac address
def mac2hex(macstr):
	return "0x"+"".join(macstr.split(":")).lower()
def hex2mac(h):
	h = h[2:]
	return h[0:2]+":"+h[2:4]+":"+h[4:6]+":"+h[6:8]+":"+h[8:10]+":"+h[10:12]
def hex2int(h):
	return int(h, 0)
def int2hex(i):
	print(i, type(i))
	return "0x%012x"%(i)

	

BASE_MAC_ADDRESS="70:B3:D5:A9:C0:64"
N = 300

if not os.path.exists("data"):
    os.makedirs("data")

pdffiles = []

v, r = getCmd("rm -rf out.pdf")

for i in range(N):
	ih = mac2hex(BASE_MAC_ADDRESS)
	ii = hex2int(ih)
	ii += i
	ix = int2hex(ii)
	ih = hex2mac(ix)


	f = open("original.svg", "r")
	svg = f.read()
	f.close()

	svg = svg.replace("VEO_WEBSITE", "cam.veo.co")
	svg = svg.replace("VEO_WIFI_CODE", "kickoff!")
	svg = svg.replace("VEO_WIFI_SSID", "VEOCAM-"+ix[-3:].upper())
	svg = svg.replace("000000000000", ix[2:].upper())
	svg = svg.replace("VEO_MODEL", "M2704")

	f = open("draft.svg", "w")
	f.write(svg)
	f.close()


	fn = "data/"+ix[2:]+".pdf"
	pdffiles.append(fn)

	v, r = getCmd("inkscape --export-pdf=%s draft.svg"%(fn)) 
	v, r = getCmd("rm -rf draft.svg") 
	
v, r = getCmd("pdfunite " + ' '.join(pdffiles) + " out.pdf") 
v, r = getCmd("rm -rf data") 


