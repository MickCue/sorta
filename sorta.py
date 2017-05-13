# A Python program with some comments

# Program name - sorta.py
# Written by - Philip McHugh (mickcue@gmail.com)
# Date:  May 11th 2017
# Version: v1.0

import re
import argparse
import shutil
import os
from os import listdir
from os.path import isfile, join
import os.path
import sys, getopt
import time
import sys
import time
import progressbar


regex = r"(?i)(S[0-9][0-9]|E[0-9][0-9])|(s[0-9]|e[0-9])|(.+?(?=S[0-9]|[0-9]))"

s_letter = ""
e_letter = ""
tt_string = ""
directory_chose = ""

load = 0

version = '1.0'
date_released = 'May 11th 2017'


def menu():
	print ("*** Sorta v0.1 ALPHA ****")

	print ("You are working from the current directory:",getCurrentDirectory())
	option = raw_input('Do you want to continue? y/N: ')

	if option == "n" or option == "":
		directory_chose = raw_input('Please enter path e.g (C://User..): ')
		print ("CHOOSEN: "+directory_chose)
		option_2 = raw_input('Is the path correct? Y/n: ')
		if option_2 == "y" or option_2 == "":
			listFiles(directory_chose)


def getCurrentDirectory():
	dirPath = os.getcwd()
	return dirPath

def cleanTitle(name):
	tmp_name = name.replace(".", " ")
	tmp_name = tmp_name.replace("-", " ")
	return tmp_name


def listFiles(path):
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	#print (onlyfiles)
	i = 0
	f = 0
	global load
	load = len(onlyfiles)
	if len(onlyfiles) == 1:
		print "No files to sort....goodbye"

	bar = progressbar.ProgressBar()
	for i in bar(range(load)):
		time.sleep(1.0)


		while i < len(onlyfiles):
			#print(onlyfiles[i])
			extenstion_check = onlyfiles[i]
			if not extenstion_check.endswith('.py'):
				r1 = re.compile("(\.pdf)|(\.txt)$|(\.lk)$")  # Only Move these extensions
				if r1.search(onlyfiles[i]):
					#print "yes"
					#print(onlyfiles[i])

					match(regex,onlyfiles[i])
					f += 1
			i += 1
	print "Processed "+str(f)+" files/folders"		
		
            #yield file


#Function to move file | Takes in title, Season & raw Filename	
def move(title, s, f):
	source = directory_chose+'\\'+f
	directory_tree = directory_chose+'\\'+title+'\\Season '+s
	#dest1 = directory_chose+'/'+title+'/Season '+s+'/'+f
	#print (directory_tree)
	dest = directory_tree+"\\"+f
	#print "Moving '"+f+"' into the folder '"+title+"' under Season '"+s+"'"
	#print "directory_tree:"+directory_tree
	#print "Processing: "+f

	if not os.path.exists(directory_tree):

		#print "making directory tree....."
		os.makedirs(directory_tree)
		
		
		shutil.move(source,dest)
	
		#print (source)
		#print (dest)
	
		
	if os.path.exists(directory_tree):
		
		if not os.path.exists(dest):
			#print("Yep")
			os.rename(source, dest)

		#print (dest)
	
	
		#print (directory_tree+"/"+f)
		#os.rename(source, directory_tree+"/"+f)
	#if not os.path.exists(directory_tree):
		#os.mkdir(directory_tree)

	#shutil.move(source, dest1)


def moveE(t, s, e):

	#Strip Zero
	if s.startswith("S0"):
		s = s.replace("S0", "")
	elif s.startswith("s0"):
		s = s.replace("s0", "")

	#Strip Season
	if s.startswith("S"):
		s = s.replace("S", "")
	elif s.startswith("s"):
		s = s.replace("s", "")


	#print "Path"+directory_chose
	#print "Moving to folder:"+t.title()+"/Season "+s+"/"+e
	#print ("QQ:"+t.title().rstrip())
	move(t.title().rstrip(), s, e)


def match(regex, test_str):
	
	matches = re.finditer(regex, test_str)
	global tt_string
	global s_letter


	for matchNum, match in enumerate(matches):
		matchNum = matchNum + 1
		#print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
		string_tv = ("{match}".format(match = match.group()))
		
		if re.match("s[0-9][1-9]|s[0-9]", string_tv):
			s_letter = ("{match}".format(match = match.group()))
		elif re.match("S[0-9][1-9]|S[0-9]", string_tv):
			s_letter = ("{match}".format(match = match.group()))
		elif re.match("E[0-9][1-9]|E[0-9]", string_tv):
			e_letter = ("{match}".format(match = match.group()))
		elif re.match("e[0-9][1-9]|e[0-9]", string_tv):
			e_letter = ("{match}".format(match = match.group()))
		else:
			tt_string = ("{match}".format(match = match.group()))

	if not cleanTitle(tt_string) == "":
		moveE(cleanTitle(tt_string), s_letter, test_str)

		
def logo():
	print "  _____  ___   ____  ______   ____ ";
	print " / ___/ /   \ |    \|      | /    |";
	print "(   \_ |     ||  D  )      ||  o  |";
	print " \__  ||  O  ||    /|_|  |_||     |";
	print " /  \ ||     ||    \  |  |  |  _  |";
	print " \    ||     ||  .  \ |  |  |  |  |";
	print "  \___| \___/ |__|\_| |__|  |__|__|v"+version+"";
	print "                                   ";
	print "*************************************"
	print date_released
	print "\nUSE: sorta.py -p PATH"
	print "*************************************"


def auto():
	logo()
	global directory_chose
	print "\nCurrent Directory: "+getCurrentDirectory()
	option_3 = raw_input("Sort current directory?  Y/n/q: ")
	if option_3 == "y" or option_3 == "":
		
		directory_chose = getCurrentDirectory()		
		listFiles(getCurrentDirectory())
	elif option_3 == "n":
		directory_chose_1 = raw_input('Please enter path e.g (C://User..): ')
		directory_chose = directory_chose_1
		print ("CHOOSEN: "+directory_chose_1)
		option_4 = raw_input('Is the path correct? Y/n: ')
		if option_4 == "y" or option_4 == "":
			listFiles(directory_chose_1)
		else:
			print "Goodbye...."
	elif option_3 == "q":
		print "Goodbye...."
		quit()

	else:
		print "Goodbye...."



if __name__ == '__main__':
	#global directory_chose
	parameter = (sys.argv)
	
	if '-v' in parameter or '--version' in parameter:
		print "Current version: v"+version
	elif '-h' in parameter or '--help' in parameter:
		print "\nUSE: sorta.py -p PATH\n\n-logo Print Logo"
	elif '-logo' in parameter:
		logo()
	elif '-p' in parameter or '--path' in parameter:
		logo()
		directory_chose = sys.argv[2]
		print ("Path Selection: "+directory_chose)
		option_2 = raw_input('Is the path correct? Y/n: ')
		if option_2 == "y" or option_2 == "":
			listFiles(directory_chose)
		else:
			print "Goodbye...."

	else:
		auto()
		
def loadbar():

	toolbar_width = 40

	# setup toolbar
	sys.stdout.write("[%s]" % (" " * toolbar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['
	
	for i in xrange(toolbar_width):
	    time.sleep(0.1) # do real work here
	    # update the bar
	    sys.stdout.write("*")
	    sys.stdout.flush()
	
	sys.stdout.write("\n")

def prog():
	bar = progressbar.ProgressBar()
	for i in bar(range(100)):
		time.sleep(0.02)

