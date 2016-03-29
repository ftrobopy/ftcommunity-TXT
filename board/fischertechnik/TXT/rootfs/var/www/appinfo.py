#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import ConfigParser
import cgi
import sys, os, pwd, getpass

print "Content-Type: text/html"
print ""
print '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
print '<html xmlns="http://www.w3.org/1999/xhtml">'
print '<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />'
print '<title>fischertechnik TXT community firmware</title>'
print '<link rel="stylesheet" href="txt.css">'
print '<link rel="icon" href="/favicon.ico" type="image/x-icon" />'
print '</head><body>'
print '<h1><div class="outline"><font color="red">fischer</font><font color="#046ab4">technik</font>&nbsp;<font color="#fcce04">TXT</font></div></h1>'
 
arguments = cgi.FieldStorage()
manifestfile = arguments['manifest'].value

def find_owner(filename):
    return pwd.getpwuid(os.stat(filename).st_uid).pw_name

def app_get(manifest, name):
    if not manifest.has_option('app', name):
        return None
    return manifest.get('app', name)

if os.path.isfile(manifestfile):
    manifest = ConfigParser.RawConfigParser()
    manifest.read(manifestfile)

    # get apps directory name from manifest file path
    name = os.path.basename(os.path.dirname(os.path.abspath(manifestfile)))
    
    appname = manifest.get('app', 'name')
    description = manifest.get('app', 'desc')
    iconname = "apps/" + name + "/" + manifest.get('app', 'icon')
    cathegory = manifest.get('app', 'cathegory')
    executable = manifest.get('app', 'exec')
    author = app_get(manifest, 'author')
    url = app_get(manifest, 'url')
    html = app_get(manifest, 'html')
    if html:
        html_path = "apps/" + name + "/" + html

    # preinstalled apps are under ftc user file ownership while
    # user installed app files are owned by the www user
    preinstalled = find_owner(manifestfile) != getpass.getuser()

    print '<h2>Application details</h2>'

    print '<table align="center">'
    print '<tr><td align="center"><img src="' + iconname + '"/></td></tr>'
    print '<tr><td align="center">' + appname + '</td></tr>'
    print '</table>'
    print '<p>'

    # fill table with various infos from manifest file
    print '<table align="center">'
    if author:
        print '<tr><td><b>Author:</b></td><td>', author, '</td></tr>'
    print '<tr><td><b>Cathegory:</b></td><td>', cathegory, '</td></tr>'
    print '<tr><td><b>Description:</b></td><td>', description, '</td></tr>'

    print '</table>'

    print '<h2>Actions</h2>'
    print '<table align="center">'

    appname_enc = appname.replace(' ','%20')
    launch_url = "launch.py?app="+appname_enc

    print '<tr><td><a href="' + launch_url + '">' + 'Launch this application on the TXT' + '</a></td></tr>'

    if url:
        print '<tr><td><a href="'+url+'">' + 'Get more application info' + '</a></td></tr>'
    if html:
        print '<tr><td><a href="'+html_path+'">' + 'Open local application pages' + '</a></td></tr>'

    # only offer to delete apps that were not preinstalled
    # print "Users", find_owner(manifestfile), getpass.getuser(), "<br>"
    if not preinstalled:
        name_enc = name.replace(' ','%20')
        delete_url = "delete.py?app="+name_enc
        print '<tr><td><a href="' + delete_url + '" onclick="return confirm(\'Really delete this app?\')">' + 'Delete this application from the TXT' + '</a></td></tr>'

    print '</table>'

else:
    print '<h1>Error: no such manifest</h1>'
    
print '<p><center><form action="/">'
print '<input type="submit" value="Ok"/>'
print '</form></center>'

print "</body></html>"
