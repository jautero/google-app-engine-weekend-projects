#!/usr/bin/env python
#
# Quickstart for Google App Engine Weekend Projects
#
# This script asks some questions and then initializes project directory.

import re, os, time
from types import StringType

wordsplit=re.compile("\W+").split
templatedir="ATemplate"
staticdir="static_files"

def convertfile(source,target,subst={}):
    if isinstance(source,StringType):
	source=open(source)
    if isinstance(target,StringType):
	target=open(target,"w")
    data=source.read()
    source.close()
    for key in subst.keys():
	subre=re.compile('@'+key+'@')
	data=subre.sub(subst[key],data)
    target.write(data)
    target.close()

project=raw_input("Project name: ")
projectwords=wordsplit(project.lower())
applicationname="-".join(projectwords)

new=raw_input("Application name (%s): " % applicationname).strip()
if new:
    applicationname=new

handlername="".join([word.capitalize() for word in projectwords])

new=raw_input("Handler class name (%s): " % handlername).strip()
if new:
    handlername=new

authorname=os.popen("git config user.name").read().strip()
authormail=os.popen("git config user.email").read().strip()

new=raw_input("Author name (%s): " %authorname).strip()
if new:
    authorname=new
new=raw_input("Author email (%s): " % authormail).strip()
if new:
    authormail=new
author="%s <%s>" % (authorname,authormail)

year=str(time.localtime()[0])

subst_dict={"project":project,"application":applicationname,
	    "mainhandler":handlername,"author":author,"year":year}

# Create directories
os.mkdir(applicationname)
os.mkdir(os.path.join(applicationname,staticdir))

# Copy template files
convertfile(os.path.join(templatedir,"app.yaml"),
	    os.path.join(applicationname,"app.yaml"),subst_dict)
convertfile(os.path.join(templatedir,"index.html"),
	    os.path.join(applicationname,"index.html"),subst_dict)
convertfile(os.path.join(templatedir,"index.yaml"),
	    os.path.join(applicationname,"index.yaml"),subst_dict)
convertfile(os.path.join(templatedir,"application.css"),
	    os.path.join(applicationname,staticdir,applicationname+".css"),subst_dict)
convertfile(os.path.join(templatedir,"application.js"),
	    os.path.join(applicationname,staticdir,applicationname+".js"),subst_dict)
convertfile(os.path.join(templatedir,"application.py"),
	    os.path.join(applicationname,applicationname+".py"),subst_dict)

