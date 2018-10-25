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
import datetime
import sys


season_str = ""
show_name = ""
directory_chose = ""
directory_tree = ""
dest = ""
source = ""
goodbye_msg = "Goodbye..."
load = 0
movie_count = 0
qe_show_count = 0
path_unix = ".sorta/"
savem = False
#extensions = ["mp4", "avi", "mkv"]
extensions_regexp1 = ".mp4|.mkv|.avi"
main_matcher = "((?i)s\d{1,2})(?i)e\d{1,2}|(.+?)(\d{1,2})(x\d{1,2})|(.*)(\d{4}.\d{2}.\d{2})"
#regexp1 = "(?i)(.*)((?i)s\d{1,2})(?i)e\d{1,2}|(.+?)(\d{1,2})(x\d{1,2})|(.*)(\d{4}.\d{2}.\d{2})|(.*(?="+extensions_regexp1+"))"
custom_show_flag = False

#Patched Depricated Warning
regexp1 = re.compile("(?i)(.*)"+main_matcher+"|(.*(?="+extensions_regexp1+"))")

#{Release}{Minor}{Updates}
version = '1.3.5.TESTING'
date_released = 'v1.3 Released: March 19th 2018'


def dateStamp():
	x = datetime.datetime.now()
	return (x.strftime("%d-%m-%Y"))


def createConfig():
	if os.path.exists(path_unix):
		print("Config Found")
		readConfig()
	else:
		print("Creating Config File")
		os.makedirs(path_unix)	
		config = os.path.join(path_unix, 'config')
		f = open(config, "a")


def getCurrentDirectory():
	dirPath = os.getcwd()
	return dirPath


def checkDirectoryName(title):

	directory_name = os.path.basename(directory_chose)
	title = re.sub('[^a-zA-Z\d\s:]', '', title)
	#print("directory_name:{}\ntitle:{}".format(directory_name, title))

	title = title.strip()
	directory_name = directory_name.strip()

	if re.search(title, directory_name, re.IGNORECASE):
		#print("In Show Folder")	
		return "Show"

	elif directory_name.startswith("Season"):
		#print("In Show Folder")	
		return "Season"

	else:
		#print("New Show")	
		return "New"


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
			extensions_regexp1_tmp = extensions_regexp1.replace(".", "")
			#r1 = re.compile('|'.join(extensions))
			r1 = re.compile(extensions_regexp1_tmp)
			if r1.search(onlyfiles[i]):		
				match(onlyfiles[i])
				f += 1
		i += 1

	print("Processed {} files/folders".format(f))		
	if movie_count >0 :
		print("Success: Found {} movies".format(movie_count))

	if qe_show_count > 0:
		print("Success: Queued {} episodes".format(qe_show_count))



def isWin(title, s, f):
	global dest
	global directory_tree
	global source
	global custom_show_flag
	global qe_show_count 


	if checkDirectoryName(title) == "Show":

		if os.name == 'nt':
			if fetch_args.qe: #If qe, move files into season/episode folder
				qe_show_count += 1
				source = directory_chose+'\\'+f
				directory_tree = directory_chose+'\\Season '+s+'\\Episodes'
				dest = directory_tree+"\\"+f

			else:
				source = directory_chose+'\\'+f
				directory_tree = directory_chose+'\\Season '+s
				dest = directory_tree+"\\"+f

		else:
			if fetch_args.qe:
				qe_show_count += 1
				source = directory_chose+'/'+f
				directory_tree = directory_chose+'/Season '+s+'/Episodes'
				dest = directory_tree+"/"+f
			else:
				source = directory_chose+'/'+f
				directory_tree = directory_chose+'/Season '+s
				dest = directory_tree+"/"+f


	elif checkDirectoryName(title) == "Season":


		if os.name == 'nt':
			if fetch_args.qe: #If qe, move files into season/episode folder
				qe_show_count += 1
				source = directory_chose+'\\'+f
				directory_tree = directory_chose+'\\Episodes'
				dest = directory_tree+"\\"+f

			else:
				source = directory_chose+'\\'+f
				directory_tree = directory_chose
				dest = directory_tree+"\\"+f

		else:
			if fetch_args.qe:
				qe_show_count += 1
				source = directory_chose+'/'+f
				directory_tree = directory_chose+'/Episodes'
				dest = directory_tree+"/"+f
			else:
				source = directory_chose+'/'+f
				directory_tree = directory_chose
				dest = directory_tree+"/"+f

	elif checkDirectoryName(title) == "New":
		#Clean Up titles
		title = re.sub(r'[^\w]', ' ', title) 

		if os.name == 'nt':
			source = directory_chose+'\\'+f
			if s == "":
				directory_tree = directory_chose+'\\'+title

			#If qe, move files into season/episode folder
			elif fetch_args.qe: 
				qe_show_count += 1
				directory_tree = directory_chose+'\\'+title+'\\Season '+s+'\\Episodes'

			elif fetch_args.s and custom_show_flag == True:
				source = directory_chose+'\\'+f
				directory_tree = directory_chose+'\\'+fetch_args.s
				dest = directory_tree+"\\"+f
				custom_show_flag = False

			else:
				directory_tree = directory_chose+'\\'+title+'\\Season '+s
				dest = directory_tree+"\\"+f
			
	
		else:
	
			source = directory_chose+'/'+f
			if s == "":
				directory_tree = directory_chose+'/'+title
			#If qe, move files into season/episode folder
			elif fetch_args.qe: 
				qe_show_count += 1
				directory_tree = directory_chose+'/'+title+'/Season '+s+'/Episodes'
			else:
				directory_tree = directory_chose+'/'+title+'/Season '+s
			
			dest = directory_tree+"/"+f
			if fetch_args.s and custom_show_flag == True:
				source = directory_chose+'/'+f
				directory_tree = directory_chose+'/'+fetch_args.s
				dest = directory_tree+"/"+f
				custom_show_flag = False


def move(title, s, f):

	isWin(title, s, f)	

	if os.path.exists(dest):
			print("File {} already exists inside folder /{}".format(f, title))

	elif not os.path.exists(directory_tree):
		os.makedirs(directory_tree)			
		shutil.move(source,dest)
	
	elif os.path.exists(directory_tree):
		
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

	if fetch_args.s:
		move(t.rstrip(), s, e)
	else:
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


		elif m.group(6) and m.group(7):
			#print(m.group(3)) #Movie Name
			#print(m.group(4)) #Movie Year
			show_name = m.group(6) #Show Name
			season_str = m.group(7)	#Season
			#movie_count += 1
			#if savem == True:
			#	moveMovies(filename_str)

		elif m.group(3) and m.group(4):
			show_name = m.group(3) #Show Name
			season_str = m.group(4)	#Season
			if season_str.startswith("0"):
				season_str = season_str[1:]

		elif m.group(8):
			if fetch_args.s:
				custom_show = fetch_args.s
				
				if ":" in fetch_args.s:
					custom_show = custom_show.split(":")
					for i in range(len(custom_show)):
						custom_show_tmp = custom_show[i]
						custom_show_tmp = custom_show_tmp.replace(" ", ".*") # FIXED REGEXP, WHEN INPUT HAS SPACE BUT FILENAME HAS .
						if re.search(custom_show_tmp, m.group(8), re.IGNORECASE):
							print("Found Show:"+custom_show[i])
							show_name = custom_show[i]
							season_str = ""
				else:
					print(m.group(8))
					custom_show_tmp = custom_show
					custom_show_tmp = custom_show_tmp.replace(" ", ".*") # FIXED REGEXP, WHEN INPUT HAS SPACE BUT FILENAME HAS .
					if re.search(custom_show_tmp, m.group(8), re.IGNORECASE):
						print("Found Show:"+custom_show)
						show_name = custom_show
						season_str = ""


		if not cleanTitle(show_name) == "":
			removeLetter_S(cleanTitle(show_name), season_str, filename_str)
			show_name = ""
			season_str = ""

		
def logo():
	print("""
   _____  ___   ____  ______   ____ 
  / ___/ /   \ |    \|      | /    |
 (   \_ |     ||  D  )      ||  o  |
  \__  ||  O  ||    /|_|  |_||     |
  /  \ ||     ||    \  |  |  |  _  |
  \    ||     ||  .  \ |  |  |  |  |
   \___| \___/ |__|\_| |__|  |__|__|v"""+version+"""
			                                   
*************************************""")
	print(date_released)
	print("\nUSE:\nsorta.py -p \"/home/desktop\" <- Specfiy Path\nsorta.py -s SHOW <- Custom Show if sorTA fails to sort")
	print("*************************************")


def auto():
	logo()
	global directory_chose
	global savem 
	print("\nCurrent Directory: "+getCurrentDirectory())

	if fetch_args.qe:
		print("Selected -qe: The files will be queued into directory *Episodes*")

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
	parser.add_argument('-s', dest='s', help='Custom Show')
	parser.add_argument('-qe', dest='qe', help='Queue Episodes', action='store_true')
	parser.add_argument('-config', dest='co', help='Config Check', action='store_true')

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

	# elif fetch_args.s:
	# 	print("Custom Show:{}".format(fetch_args.s))

	elif fetch_args.v:
		print("Current version: v{}".format(version))

	elif fetch_args.co:
		createConfig()

	else:
		auto()