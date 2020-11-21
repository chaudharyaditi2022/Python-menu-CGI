#!/usr/bin/python3
print("content-type:text/plain")
print()

import subprocess as sp
import cgi

field = cgi.FieldStorage()
task = field.getvalue("task")
output = sp.getstatusouput("sudo {}".format(task))
print(ouput[1])

			


