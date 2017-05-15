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
#import progressbar


#regex = r"(?i)(S[0-9][0-9]|E[0-9][0-9])|(s[0-9]|e[0-9])|(.+?(?=S[0-9]|[0-9]))"
regex = r"(?i)(.+?(?=S[0-9])|(S[0-9][0-9])|s[0-9])"
s_letter = ""
e_letter = ""
tt_string = ""
directory_chose = ""

load = 0

version = '1.0'
date_released = 'May 11th 2017'


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
		print("No files to sort....goodbye")

	#bar = progressbar.ProgressBar()
	#for i in bar(list(range(load))):
		#time.sleep(1.0)

	while i < len(onlyfiles):
			#print(onlyfiles[i])
		extenstion_check = onlyfiles[i]
		if not extenstion_check.endswith('.py'):
			r1 = re.compile("(\.mp4)|(\.avi)$|(\.mkv)$")  
			if r1.search(onlyfiles[i]):
				#
				match(regex,onlyfiles[i])
				f += 1
		i += 1
	print("Processed "+str(f)+" files/folders")		

	
def move(title, s, f):
	source = directory_chose+'\\'+f
	directory_tree = directory_chose+'\\'+title+'\\Season '+s
	
	dest = directory_tree+"\\"+f

	if not os.path.exists(directory_tree):
		
		os.makedirs(directory_tree)			
		shutil.move(source,dest)

	if os.path.exists(directory_tree):
		
		if not os.path.exists(dest):
			os.rename(source, dest)


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

	move(t.title().rstrip(), s, e)


def match(regex, test_str):
	
	matches = re.finditer(regex, test_str)
	global tt_string
	global s_letter


	for matchNum, match in enumerate(matches):
		matchNum = matchNum + 1

		string_tv = ("{match}".format(match = match.group()))
		
		#print ("string_tv:"+string_tv)

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
		#print ("Got this title:"+cleanTitle(tt_string))
		moveE(cleanTitle(tt_string), s_letter, test_str)

		
def logo():
	print("  _____  ___   ____  ______   ____ ");
	print(" / ___/ /   \ |    \|      | /    |");
	print("(   \_ |     ||  D  )      ||  o  |");
	print(" \__  ||  O  ||    /|_|  |_||     |");
	print(" /  \ ||     ||    \  |  |  |  _  |");
	print(" \    ||     ||  .  \ |  |  |  |  |");
	print("  \___| \___/ |__|\_| |__|  |__|__|v"+version+"");
	print("                                   ");
	print("*************************************")
	print(date_released)
	print("\nUSE: sorta.py -p PATH")
	print("*************************************")


def auto():
	logo()
	global directory_chose
	print("\nCurrent Directory: "+getCurrentDirectory())
	option_3 = input("Sort current directory?  Y/n/q: ")
	if option_3 == "y" or option_3 == "":
		
		directory_chose = getCurrentDirectory()		
		listFiles(getCurrentDirectory())
	elif option_3 == "n":
		directory_chose_1 = input('Please enter path e.g (C://User..): ')
		directory_chose = directory_chose_1
		print(("CHOOSEN: "+directory_chose_1))
		option_4 = input('Is the path correct? Y/n: ')
		if option_4 == "y" or option_4 == "":
			listFiles(directory_chose_1)
		else:
			print("Goodbye....")
	elif option_3 == "q":
		print("Goodbye....")
		quit()

	else:
		print("Goodbye....")



if __name__ == '__main__':

	parameter = (sys.argv)
	
	if '-v' in parameter or '--version' in parameter:
		print("Current version: v"+version)
	elif '-h' in parameter or '--help' in parameter:
		print("\nUSE: sorta.py -p PATH\n\n-logo Print Logo")
	elif '-logo' in parameter:
		logo()
	elif '-p' in parameter or '--path' in parameter:
		logo()
		directory_chose = sys.argv[2]
		print(("Path Selection: "+directory_chose))
		option_2 = input('Is the path correct? Y/n: ')
		if option_2 == "y" or option_2 == "":
			listFiles(directory_chose)
		else:
			print("Goodbye....")

	else:
		auto()		