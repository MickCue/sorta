#!/usr/bin/python


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


regexp1 = "(?i)(.*)(s[0-9][0-9])|(.*)([0-9999]{4})"
s_letter = ""
e_letter = ""
title_name = ""
directory_chose = ""
directory_tree = ""
dest = ""
source = ""
goodbye_msg = "Goodbye..."
load = 0
movie_count = 0

#{Release}{Minor}{Updates}
version = '1.2.1'
date_released = 'Jan 27th 2018'


def getCurrentDirectory():
	dirPath = os.getcwd()
	return dirPath


def checkDirectoryName(title):

	directory_name = os.path.basename(directory_chose)
	
	if directory_name == title:		
		return True
	else:		
		return False


def cleanTitle(name):
	tmp_name = name.replace(".", " ")
	tmp_name = tmp_name.replace("-", " ")
	return tmp_name


def listFiles(path):
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	i = 0
	f = 0
	global load
	load = len(onlyfiles)
	if len(onlyfiles) == 1:
		print(goodbye_msg)

	while i < len(onlyfiles):

		extenstion_check = onlyfiles[i]
		if not extenstion_check.endswith('.py'):
			r1 = re.compile("(\.mp4)|(\.avi)$|(\.mkv)$")  
			if r1.search(onlyfiles[i]):			
				match(onlyfiles[i])
				f += 1
		i += 1

	print("Processed "+str(f)+" files/folders")		
	if movie_count >0 :
		print("Found {} movies".format(movie_count))


def isWin(title, s, f):
	global dest
	global directory_tree
	global source


	if checkDirectoryName(title) == True:
		if os.name == 'nt':
			source = directory_chose+'\\'+f
			directory_tree = directory_chose+'\\Season '+s
			dest = directory_tree+"\\"+f
		else:
	
			source = directory_chose+'/'+f
			directory_tree = directory_chose+'/Season '+s
			dest = directory_tree+"/"+f

	elif checkDirectoryName(title) != True:
		
		if os.name == 'nt':
		
			source = directory_chose+'\\'+f
			directory_tree = directory_chose+'\\'+title+'\\Season '+s
			dest = directory_tree+"\\"+f
	
		else:
	
			source = directory_chose+'/'+f
			directory_tree = directory_chose+'/'+title+'/Season '+s
			dest = directory_tree+"/"+f


def move(title, s, f):

	isWin(title, s, f)	
	if not os.path.exists(directory_tree):
		
		os.makedirs(directory_tree)			
		shutil.move(source,dest)

	if os.path.exists(directory_tree):
		
		if not os.path.exists(dest):
			os.rename(source, dest)


def removeLetter_S(t, s, e):

	if s.startswith("S0"):
		s = s.replace("S0", "")
	elif s.startswith("s0"):
		s = s.replace("s0", "")


	if s.startswith("S"):
		s = s.replace("S", "")
	elif s.startswith("s"):
		s = s.replace("s", "")

	move(t.title().rstrip(), s, e)


def match(test_str):

	global title_name
	global s_letter
	global movie_count


	m = re.match(regexp1, test_str)

	if m.group(1):
		title_name = m.group(1) #Show Name
		s_letter = m.group(2)	#Season

	elif m.group(3):
		#print(m.group(3)) #Movie Name
		#print(m.group(4)) #Movie Year
		movie_count += 1

	if not cleanTitle(title_name) == "":

		removeLetter_S(cleanTitle(title_name), s_letter, test_str)
		title_name = ""
		s_letter = ""

		
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
	if option_3 == "y" or option_3 == "Y" or option_3 == "":
		
		directory_chose = getCurrentDirectory()		
		listFiles(getCurrentDirectory())
	elif option_3 == "n":
		directory_chose_1 = input('Please enter path e.g (C://User..): ')
		directory_chose = directory_chose_1
		print(("CHOOSEN: "+directory_chose_1))
		option_4 = input('Is the path correct? Y/n: ')
		if option_4 == "y" or option_4 == "Y" or option_4 == "":
			listFiles(directory_chose_1)
		else:
			print(goodbye_msg)
	elif option_3 == "q":
		print(goodbye_msg)
		quit()

	else:
		print(goodbye_msg)


def checkPy():
    if sys.version_info[:2] <= (2, 9):
        print(goodbye_msg+" Python v3 is needed to run this script!")
        sys.exit()


if __name__ == '__main__':
	checkPy()
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
		if option_2 == "y" or option_2 == "Y" or option_2 == "":
			listFiles(directory_chose)
		else:
			print(goodbye_msg)

	else:
		auto()		