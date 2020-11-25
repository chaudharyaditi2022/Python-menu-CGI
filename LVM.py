#!/usr/bin/python3
print("content-type:text/plain")
print()

import subprocess as sp
import cgi

field = cgi.FieldStorage()
btn = field.getvalue("btn")
output = (0,"")

if btn == "vgbtn":
	vgname= field.getvalue("vgname")
	disks= field.getvalue("disks")
	sp.getstatusoutput("sudo pvcreate {}".format(disks))
	output = sp.getstatusoutput("sudo vgcreate {} {}".format(vgname,disks))
	if output[0] == 0:
		print("Volume group created successfully!!")
		info = sp.getstatusoutput("sudo vgdisplay {}".format(vgname))
		print(info[1])
elif btn == "lvbtn":
	vgname = field.getvalue("vgname")
	lvname = field.getvalue("lvname")
	size = field.getvalue("size")
	mountpt = field.getvalue("mountpt")
	output = sp.getstatusoutput("sudo lvcreate -n {} --size {} {} ".format(lvname,size,vgname))
	print(output[1],"\n")
	if(output[0] == 0):
		output = sp.getstatusoutput("sudo mkfs.ext4 /dev/{}/{}".format(vgname,lvname))
		print(output[1],"\n") 
		if(output[0] == 0):
			rc = sp.getstatusoutput("sudo mkdir {}".format(mountpt))
			output = sp.getstatusoutput("sudo mount /dev/{}/{} {}".format(vgname,lvname,mountpt))
	if(output[0] == 0):
		print("Logical volume created successfully!!")
		info = sp.getstatusoutput("sudo lvdisplay {}/{}".format(vgname,lvname))
		print(info[1])
elif btn == "stbtn":
	vgname = field.getvalue("vgname")
	lvname = field.getvalue("lvname")
	size = field.getvalue("size")
	task = field.getvalue("task")
	if task == 'reduce':
		mountpt = sp.getoutput("sudo findmnt -n -o TARGET /dev/{}/{}".format(vgname,lvname))
		output = sp.getstatusoutput("sudo umount /dev/{}/{}".format(vgname,lvname))
		if(output[0] == 0):
			output = sp.getstatusoutput("sudo e2fsck -f -p /dev/{0}/{1} ; sudo resize2fs /dev/{0}/{1} {2}".format(vgname,lvname,size))
			print(output[1],"\n")
			if(output[0] == 0):
				output = sp.getstatusoutput("sudo lvreduce -y -L {} /dev/{}/{}".format(size,vgname,lvname))
				if(output[0] == 0):
					output=sp.getstatusoutput("sudo mount /dev/{}/{} {}".format(vgname,lvname,mountpt))
	
	elif task == 'extend':
		output = sp.getstatusoutput("sudo lvextend -L {} /dev/{}/{}".format(size,vgname,lvname))
		if(output[0] == 0):
			output = sp.getstatusoutput("sudo resize2fs /dev/{}/{}".format(vgname,lvname))

	if(output[0] == 0):
		print("Logical volume created successfully!!")
		info = sp.getstatusoutput("sudo lvdisplay {}/{}".format(vgname,lvname))
		print(info[1])
elif btn == "delvgbtn":
	vgname = field.getvalue("vgname")
	output = sp.getstatusoutput("sudo vgchange -a n {}".format(vgname))
	if(output[0] == 0):
		output = sp.getstatusoutput("sudo vgremove -y  {}".format(vgname))
	if(output[0] == 0):
		print("Volume group deleted successfully!!")
elif btn == "vginfobtn":
	vgname = field.getvalue("vgname")
	output = sp.getstatusoutput("sudo vgdisplay {}".format(vgname))
	if(output[0] == 0):
		print("Volume group {} Info : \n {}".format(vgname,output[1]))
elif btn == "lvinfobtn":
	vgname = field.getvalue("vgname")
	lvname = field.getvalue("lvname")
	output = sp.getstatusoutput("sudo lvdisplay {}/{}".format(vgname,lvname))
	if(output[0] == 0):
		print("Logical Volume group {} Info : \n {}".format(vgname,output[1]))
elif btn == "dellvbtn":
	vgname = field.getvalue("vgname")
	lvname = field.getvalue("lvname")
	output = sp.getstatusoutput("sudo umount /dev/{}/{}".format(vgname,lvname))
	output = sp.getstatusoutput("sudo lvremove -f /dev/{}/{}".format(vgname,lvname))
	if(output[0] == 0):
		print("Logical Volume group {} Deleted successfully!!".format(lvname))
elif btn == "diskinfobtn":
	output = sp.getstatusoutput("sudo fdisk -l")
	print("Disks Available : \n {}".format(output[1]))
elif btn == "partinfobtn":
	output = sp.getstatusoutput("sudo df -h")
	print("Partition Info : \n {}".format(output[1]))
elif btn == "allvginfobtn":
	output = sp.getstatusoutput("sudo vgdisplay")
	print("All virtual groups Available : \n {}".format(output[1]))

if(output[0] != 0):
	print("Something went wrong!! : \n {} ".format(output[1]))