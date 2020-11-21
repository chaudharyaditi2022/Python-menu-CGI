#!/usr/bin/python3
print("content-type:text/plain")
print()

import subprocess as sp
import os
import cgi

field = cgi.FieldStorage()
search= field.getvalue("search")

if(search != None):
	output = sp.getstatusoutput("sudo docker search {}".format(search))
	if output[0]==0:
		print("Docker images available : {} ".format(output[1]))
else:
	btn = field.getvalue("btn")
	if btn == "launchbtn":
		osname = field.getvalue("osname")
		image = field.getvalue("image")
		output = sp.getstatusoutput("sudo docker run -dit --name {} {}".format(osname,image))
		if output[0] == 0:
			 print("{} Container Launched successfully!!".format(osname))
	elif btn == "stbtn":
		osname = field.getvalue("osname")
		task = field.getvalue("task")
		output = sp.getstatusoutput("sudo docker {} {}".format(task,osname))
		if output[0] == 0:
			 print("{} Container {} successfully!!".format(osname,task))
	elif btn == "rmbtn":
		osname = field.getvalue("osname")
		output = sp.getstatusoutput("sudo docker rm {}".format(osname))
		if output[0] == 0:
			 print("{} Container removed successfully!!".format(osname))
	elif btn == "rmallbtn":
		output = sp.getstatusoutput("sudo docker rm -f `sudo docker ps -a -q`")
		if output[0] == 0:
			print("All Containers removed successfully!!")
	elif btn == "imgbtn":
		output = sp.getstatusoutput("sudo docker images")
		if output[0] == 0:
			print("List of all downloaded images : \n {}".format(output[1]))

	elif btn == "allcontbtn":
		output = sp.getstatusoutput("sudo docker ps -a")
		if output[0] == 0:
			print("List of all running and stopped containers : \n {}".format(output[1]))
	elif btn == "contbtn":
		output = sp.getstatusoutput("sudo docker ps")
		if output[0] == 0:
			print("List of all running containers : \n {}".format(output[1]))

	elif btn == "logbtn":
		osname = field.getvalue("osname")
		output = sp.getstatusoutput("sudo docker logs {}".format(osname))
		if output[0] == 0:
			print("Logs of {} container : \n {}".format(osname,output[1]))

	elif btn == "infobtn":
		osname = field.getvalue("osname")
		output = sp.getstatusoutput("sudo docker inspect {}".format(osname))
		if output[0] == 0:
			print("Info of {} container : \n {}".format(osname,output[1]))
		
	if output[0] != 0:
		print("Something went Wrong!!\n {}".format(output[1]))









