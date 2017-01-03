#!/usr/bin/env python
import sys, stat, os
import grp, pwd
import locale
import time
from prettytable import PrettyTable

table = PrettyTable(["Permissions", "# Links", "Owner", "Size", "Last Mod", "Name"])

if len(sys.argv) == 1:
	files=os.listdir(".")
else:
	files=sys.argv[1:]

locale.setlocale(locale.LC_ALL,'')
files.sort(locale.strcoll)

now = int(time.time())
recent = now - (6 * 30 * 24 * 60 * 60) 

colors={"default":"",
		 "white":	"\x1b[01;37m",
		 "gray":	"\x1b[00;37m",
		 "purple":   "\x1b[00;35m",
		 "cyan":   "\x1b[01;36m",
		 "green":  "\x1b[01;32m",
		 "red":    "\x1b[01;05;37;41m"}

def has_colors(stream):
	if not hasattr(stream, "isatty"):
		return False
	if not stream.isatty():
		return False
	try:
		import curses
		curses.setupterm()
		return curses.tigetnum("colors") > 2
	except:
		return False
has_colors = has_colors(sys.stdout)

def get_mode_info(mode, name):
	perms = "-"
	color = "default"
	link = ""

	if stat.S_ISDIR(mode):
		perms = "d"
		color = "cyan"
	elif stat.S_ISLNK(mode):
		perms = "l"
		color = "purple"
		link = os.readlink(filename)
		if not os.path.exists(filename):
			color = "red"
	elif stat.S_ISREG(mode):
		if mode & (stat.S_IXGRP | stat.S_IXUSR | stat.S_IXOTH):
			color = "green"
		else:
			if name[0] == '.':
				color = "gray"
			else:
				color = "white"

	mode = stat.S_IMODE(mode)

	for who in "USR", "GRP", "OTH":
		for what in "R", "W", "X":
			if mode & getattr(stat, "S_I" + what + who):
				perms = perms + what.lower()
			else:
				perms = perms + "-"

	return (perms, color, link)

for filename in files:
	try: 
		stat_info = os.lstat(filename)
	except:
		sys.stderr.write("%s: No such file or directory\n" % filename)
		continue

	perms, color, link = get_mode_info(stat_info.st_mode, filename)

	nlink = "%4d" % stat_info.st_nlink 

	try:
		name = "%-8s" % pwd.getpwuid(stat_info.st_uid)[0]
	except KeyError:
		name = "%-8s" % stat_info.st_uid

	try:
		group = "%-8s" % grp.getgrgid(stat_info.st_gid)[0]
	except KeyError:
		group = "%-8s" % stat_info.st_gid

	size = "%8d" % stat_info.st_size

	ts = stat_info.st_mtime
	if (ts < recent) or (ts > now): 
		time_fmt = "%b %e  %Y"
	else:
		time_fmt = "%b %e %R"
	time_str = time.strftime(time_fmt, time.gmtime(ts))

	if colors[color] and has_colors:
		filenameStr = colors[color] + filename + "\x1b[00m"
	else:
		filenameStr = filename

	if link:
		filenameStr += " -> "
	filenameStr += link

	table.add_row([perms, nlink, name, size, time_str, filenameStr])

table.align["Permissions"] = 'l'
table.align["# Links"] = 'r'
table.align["Owner"] = 'l'
table.align["Size"] = 'r'
table.align["Last Mod"] = 'l'
table.align["Name"] = 'l'
print table
