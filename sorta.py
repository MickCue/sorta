#!/usr/bin/python
"""
SorTA - Powerful Tv Show Sorter
@MickCue

2018
"""

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
import configparser


regexp1 = "(?i)(.*)(s[0-9][0-9]|s[0-9])|(.*)([0-9999]{4})"
season_str = ""
show_name = ""
directory_chose = ""
directory_tree = ""
dest = ""
source = ""
goodbye_msg = "Goodbye..."
load = 0
movie_count = 0
path = "config.ini"
savem = False

#{Release}{Minor}{Updates}
version = '1.2.7'
date_released = 'March 19th 2018'


def createConfig():
	config = configparser.ConfigParser()
	config.add_section('Locations')
	config.set('Locations', 'Movies', '')

	with open(path, "w") as config_file:
		config.write(config_file)

def saveMovieLocation(location):
	config = configparser.ConfigParser()
	config.add_section('Locations')
	config.set('Locations', 'Movies', location)

	with open(path, "w") as config_file:
		config.write(config_file)

def getMovieLocation():
	parser = configparser.ConfigParser()
	parser.read('config.ini')
	location = parser.get('Locations', 'Movies')
	return location


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

	print("Processed {} files/folders".format(f))		
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


def moveMovies(source):
	
	shutil.move(source,getMovieLocation())


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


def match(filename_str):

	global show_name
	global season_str
	global movie_count


	m = re.match(regexp1, filename_str)

	if m is not None:
		if m.group(1):
			show_name = m.group(1) #Show Name
			season_str = m.group(2)	#Season


		elif m.group(3) and m.group(4):
			#print(m.group(3)) #Movie Name
			#print(m.group(4)) #Movie Year
			movie_count += 1
			if savem == True:
				moveMovies(filename_str)


		if not cleanTitle(show_name) == "":

			removeLetter_S(cleanTitle(show_name), season_str, filename_str)
			show_name = ""
			season_str = ""

		
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
	global savem 
	print("\nCurrent Directory: "+getCurrentDirectory())
	option_3 = input("Sort current directory?  Y/n/q: ")
	if option_3 == "y" or option_3 == "Y" or option_3 == "":

		if fetch_args.m:
			if len(getMovieLocation())>0:
				res1 = input('Do you want to save movies to\nLocation:{}\nY/n:'.format(getMovieLocation()))
				if res1 == "y" or res1 == "Y" or res1 == "":
					savem = True
				elif res1 == "n":
					savem = True
					res3 = input('Enter New Location:')
					saveMovieLocation(res3)
			else:
				res2 = input('Enter Location to save movies Y/n:')
				if res2 == "y" or res2 == "Y" or res2 == "":
					savem = True
					res3 = input('Enter Location:')
					saveMovieLocation(res3)

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
	#if not os.path.exists(path):
		#createConfig()

	parser = argparse.ArgumentParser(description='sorTA | Powerful TV Show Sorter')
	parser.add_argument('-p', dest='p', help='Path to sort')
	parser.add_argument('-logo', dest='l', help='Print Logo', action='store_true')
	parser.add_argument('-v', dest='v', help='Show version details', action='store_true')
	parser.add_argument('-m', dest='m', help='Move movies to this location', action='store_true')

	fetch_args = parser.parse_args()

	if fetch_args.p:
		print(("Path Selection: {}".format(fetch_args.p)))
		option_2 = input('Is the path correct? Y/n: ')
		if option_2 == "y" or option_2 == "Y" or option_2 == "":
			directory_chose = fetch_args.p
			listFiles(fetch_args.p)
		else:
			print(goodbye_msg)

	elif fetch_args.l:
		logo()

	elif fetch_args.v:
		print("Current version: v{}".format(version))

	else:
		auto()