#!/usr/bin/python3
print("content-type:text/plain")
print()

import subprocess as sp
import cgi
from lxml import etree as ET

field = cgi.FieldStorage()
btn = field.getvalue("btn")
output=(0,"")

if btn == "configbtn":

	ip = field.getvalue("IP")
	folder = field.getvalue("folder")
	rc=sp.getstatusoutput("sudo mkdir {}".format(folder))
	node = field.getvalue("node")
	

	htree = ET.parse("/etc/hadoop/hdfs-site.xml")
	hroot = htree.getroot()
	if(len(hroot) == 0):
		hp = ET.SubElement(hroot, 'property')
	else:
		hp = hroot[0]
	if(len(hp) == 0):
		hn = ET.SubElement(hp, 'name')
		hv = ET.SubElement(hp,'value')
	else:
		hn = hp[0]
		hv = hp[1]
	

	#core-site configure
	ctree = ET.parse("/etc/hadoop/core-site.xml")
	croot = ctree.getroot()
	if len(croot) == 0:
		cp = ET.SubElement(croot, 'property')
	else:
		cp = croot[0]
	if(len(cp) == 0):
		cn = ET.SubElement(cp, 'name')
		cv = ET.SubElement(cp,'value')
	else:
		cn = cp[0]
		cv = cp[1]


	
	cn.text = "fs.default.name"
	cv.text = "hdfs://{}:9001".format(ip)

	ctree.write("/etc/hadoop/core-site.xml",pretty_print=True)


	if node == 'namenode':
		hn.text = "dfs.name.dir"
		hv.text =  folder
		htree.write("/etc/hadoop/hdfs-site.xml",pretty_print=True)
		print("Formatting namenode ...")
		output = sp.getstatusoutput("sudo yes Y | hadoop namenode -format")
		output = (0,"")

	else:
		hn.text = "dfs.data.dir"
		hv.text =  folder
		htree.write("/etc/hadoop/hdfs-site.xml",pretty_print=True)
		output = (0,"")

	if(output[0] == 0):
			print("Configured as {} Successfully!!".format(node))

elif btn == "stnbtn":
	task = field.getvalue("task")
	output = sp.getstatusoutput("sudo hadoop-daemon.sh {} namenode".format(task))
	if(output[0] == 0):
			print("Namenode {} Successfully!!".format(task))

elif btn == "stdbtn":
	task = field.getvalue("task")
	output = sp.getstatusoutput("sudo hadoop-daemon.sh {} datanode".format(task))
	if(output[0] == 0):
			print("Datanode {} Successfully!!".format(task))

elif btn == "configcbtn":

	ip = field.getvalue("IP")
	ctree = ET.parse("/etc/hadoop/core-site.xml")
	croot = ctree.getroot()
	if(len(croot) == 0):
		cp = ET.SubElement(croot, 'property')
	else:
		cp = croot[0]
	if(len(cp) == 0):
		cn = ET.SubElement(cp, 'name')
		cv = ET.SubElement(cp,'value')
	else:
		cn = cp[0]
		cv = cp[1]

	cn.text = "fs.default.name"
	cv.text = "hdfs://{}:9001".format(ip)
	ctree.write("/etc/hadoop/core-site.xml",pretty_print=True)

	print("System configured as Client Successfully!!")


elif btn == "opbtn":
	file = field.getvalue("file")
	operation = field.getvalue("operation")
	if operation == "-put":
		output = sp.getstatusoutput("sudo hadoop fs -put {} /".format(file))
		if output[0] == 0:
			print("File uploaded Successfully!! \n {} ".format(output[1]))

	elif operation == "-cat":
		output = sp.getstatusoutput("sudo hadoop fs -cat {}".format(file))
		if output[0] == 0:
			print("File read Successfully \n {} ".format(output[1]))
	elif operation == "-touchz":
		output = sp.getstatusoutput("sudo hadoop fs -touchz {}".format(file))
		if output[0] == 0:
			print("File created Successfully \n {} ".format(output[1]))

	elif operation == "-rm":
		output = sp.getstatusoutput("sudo hadoop fs -rm {}".format(file))
		if output[0] == 0:
			print("File removed Successfully \n {} ".format(output[1]))

elif btn == "infobtn":
	output = sp.getstatusoutput("sudo hadoop dfsadmin -report | less")
	if output[0] == 0:
		print("Information of Cluster:  \n {} ".format(output[1]))

elif btn == "fileinfobtn":
	output = sp.getstatusoutput("sudo hadoop fs -ls /")
	if output[0] == 0:
		print("Files information in the Cluster: \n {} ".format(output[1]))

elif btn == "getlink":
	ip = field.getvalue("IP")
	print("Link to WebUI : 'http://{}:50070'".format(ip))
	output = (0,"")

if(output[0] != 0):
	print("Something went wrong!! : \n {} ".format(output[1]))



			

