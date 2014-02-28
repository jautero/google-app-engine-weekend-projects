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
bootstrapurl="http://twitter.github.com/bootstrap/assets/bootstrap.zip"

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

def askyesno(question,default):
    answer=""
    while answer != "y" and answer != "n":
        answer=raw_input("%s (y/n) [%s]" % (question,default))
        if not answer:
            answer=default
        answer=answer.lower()
    if answer == "y":
        return True
    else:
        return False

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

bootstrap=askyesno("Do you want Twitter's Bootstrap?","y")
unittests=askyesno("Do you want have unit tests and TDDStateTarcker","y")

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
if unittests:
    convertfile(os.path.join(templatedir,"application-ut.py"),
        os.path.join(applicationname,applicationname+".py"),subst_dict)
else:
    convertfile(os.path.join(templatedir,"application.py"),
	    os.path.join(applicationname,applicationname+".py"),subst_dict)
# Fetch Bootstrap
if bootstrap:
    import urllib2, zipfile, cStringIO
    zip=zipfile.ZipFile(cStringIO.StringIO(urllib2.urlopen(bootstrapurl).read()))
    for filename in zip.namelist():
        if filename.endswith('/'):
            os.makedirs(os.path.join(applicationname,staticdir,filename))
        else:
            zip.extract(filename,os.path.join(applicationname,staticdir))

if unittests:
        convertfile(os.path.join(templatedir,"test","tdd-state-tracker.css"),
            os.path.join(applicationname,staticdir,"tdd-state-tracker.css"),subst_dict)
        convertfile(os.path.join(templatedir,"test","tdd-state-tracker.js"),
            os.path.join(applicationname,staticdir,"tdd-state-tracker.js"),subst_dict)
        convertfile(os.path.join(templatedir,"test","test.html"),
            os.path.join(applicationname,"test.html"),subst_dict)
