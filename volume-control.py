#!/usr/bin/env python
import argparse
import os
import subprocess
# MAX OUTPUT / INPUT VOLUME
out_max = 100
def getVolume(sink):
	sname = "sinks" if int(sink) == 0 else "sources"
	csname = "Sink" if int(sink) == 0 else "Source"

	p1 = subprocess.Popen(["pactl", "list",sname], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["grep",csname+" #"+sink,"-A","10"],stdin=p1.stdout,stdout=subprocess.PIPE)
	p3 = subprocess.Popen(["grep","Volume"],stdin=p2.stdout,stdout=subprocess.PIPE)
	p4 = subprocess.Popen(["awk","{print $5}"],stdin=p3.stdout,stdout=subprocess.PIPE)

	volume = p4.communicate()[0].split('%')[0]
	return volume

def getMute(sink):
	sname = "sinks" if int(sink) == 0 else "sources"
	csname = "Sink" if int(sink) == 0 else "Source"	

	o1 = subprocess.Popen(["pactl", "list",sname],stdout=subprocess.PIPE)
	o2 = subprocess.Popen(["grep",csname+" #"+sink,"-A","10"],stdin=o1.stdout,stdout=subprocess.PIPE)
	o3 = subprocess.Popen(["grep","Mute"],stdin=o2.stdout,stdout=subprocess.PIPE)

	mute = True if "yes" in o3.communicate()[0] else False

	return mute

def notify(sink):

	volume = getVolume(sink)
	mute = getMute(sink)
	icon = None
	stype = "audio-volume" if int(sink) == 0 else "microphone-sensitivity"

	if mute:
		icon = "notification-"+stype+"-muted"
	else:
		if int(volume) == 0:
			# There is no icon for microphone off
			icon = "notification-"+stype+"-off" if int(sink) == 0 else "notification-"+stype+"-low"
		elif int(volume) <35:
			icon = "notification-"+stype+"-low"
		elif int(volume) <70:
			icon = "notification-"+stype+"-medium"
		else:
			icon = "notification-"+stype+"-high"

	subprocess.call(['notify-send','-i',icon,'-h','int:value:'+volume,'-h','string:synchronous:volume'," "])


	return None

parser = argparse.ArgumentParser()
parser.add_argument("command", help="{up|down|mute-toggle}")
parser.add_argument("magnitude", help="Integer - Percent Change")
parser.add_argument("sink",help="Default Sink 0 for Output, Source 1 for Input")
args = parser.parse_args()

sname = "sink" if int(args.sink) == 0 else "source"

volume = getVolume(args.sink)
mute = getMute(args.sink)

if args.command == "mute-toggle":

	subprocess.call(['pactl','set-'+sname+'-mute',args.sink,'toggle'])
	notify(args.sink)


elif args.command == "up":
	if int(volume)<out_max:
		subprocess.call(['pactl','set-'+sname+'-volume',args.sink,'+'+args.magnitude+'%'])
	notify(args.sink)
	overvol = getVolume(args.sink)
	if(int(overvol)>out_max):
		subprocess.call(['pactl','set-'+sname+'-volume',args.sink,str(out_max)+'%'])
elif args.command== "down":
	subprocess.call(['pactl','set-'+sname+'-volume',args.sink,'-'+args.magnitude+'%'])
	notify(args.sink)
