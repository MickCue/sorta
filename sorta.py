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
import json

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
savem = False
extensions_regexp1 = ".mp4|.mkv|.avi"
regexp1 = "((.*)([Ss]\d{1,2}))|((.*[. _-])(\d{1,2})(?=x))|((.+)(\d{4}))|(.*(?="+extensions_regexp1+"))"
custom_show_flag = False

CDEF = '\033[0m'
CRED = '\33[31m'
CGRE = '\33[92m'


#{Release}{Minor}{Patches}
version = '1.4.3'
date_released = 'v1.4 Released: November 9th 2018'


def dateStamp():
	x = datetime.datetime.now()
	return (x.strftime("%d-%m-%Y"))


def createCuShJSON():
	#ds = os.path.dirname(__file__) # Directory of sorTA
	ds = os.path.dirname(os.path.realpath(__file__))
	placeholder = {"sorTA":{"Name" : "Config File"},"sorTA-Movies":{"unix" : "/home/","win": "c"}}


	if os.path.exists(ds+"/showList.json"):
		print("Custom Show List Succesfully Loaded")

	else:
		print("Creating Custom Show List File")
		
		sortaPath = r'{}'.format(ds) # path to be created

		config = os.path.join(sortaPath, 'showList.json')
		f = open(config, "a")

		with open(ds+"/showList.json" , 'w') as f:
			json.dump(placeholder, f)


def getShowList():
	#ds = os.path.dirname(__file__) # Directory of sorTA
	ds = os.path.dirname(os.path.realpath(__file__))
	with open(ds+"/showList.json") as jsonData:
		d = json.load(jsonData)

		for key in d.keys():
			if key != "sorTA" and key != "sorTA-Movies":
				print("Match:"+key)
				print("+Replace with:"+d[key]["Name"])
				print("------------------------------")


def getloc():

	ds = os.path.dirname(os.path.realpath(__file__))
	with open(ds+"/showList.json") as jsonData:
		d = json.load(jsonData)
		print("Movies will be moved to these locations:")
		print("------------------------------")
		for key in d.keys():
			if key == "sorTA-Movies":
				print("+Win Location:"+d[key]["win"])
				print("+Unix Location:"+d[key]["unix"])
		print("------------------------------")


def checkShowInList(show):
	#ds = os.path.dirname(__file__) # Directory of sorTA
	ds = os.path.dirname(os.path.realpath(__file__))
	
	with open(ds+"/showList.json") as jsonData:
		d = json.load(jsonData)
		for x in d:

			#print(show.lower() + "=" + x.lower())
			if show.lower() == x.lower():
				# Loop problem
				print("Found Custom Show ({}) for: {}".format(d[x]["Name"], x))
				#show = d[x]["Name"]

			elif show.lower().startswith(x.lower()): # Unmatched Media files but specified in Show JSON
				#print("Found Custom Show ({}) for: {}".format(d[x]["Name"], x))
				show = d[x]["Name"]

	#print("Found Custom Show ({}) for: {}".format(showC1, show))
	return show


def addCustomShow(data):
	# Format Match:Replace
	csData = data.split(':')
	ds = os.path.dirname(os.path.realpath(__file__))# Directory of sorTA

	entry = {csData[0]: { "Name" : csData[1]}}

	with open(ds+"/showList.json") as f:
		data = json.load(f)
		data.update(entry)

	with open(ds+"/showList.json" , 'w') as f:
		json.dump(data, f)
		print("Succesfully added {}({})".format(csData[0],csData[1]))


def addMovieLoc(loc):
	ds = os.path.dirname(os.path.realpath(__file__))# Directory of sorTA


	with open(ds+"/showList.json") as f:
		data = json.load(f)
		if os.name == 'nt':
			data["sorTA-Movies"]["win"] = loc
		else:
			data["sorTA-Movies"]["unix"] = loc
		#data.update(entry)

	with open(ds+"/showList.json" , 'w') as f:
		json.dump(data, f)
		print("Succesfully added ({}) to Movie location".format(loc))


def getMovieLocation():
	#ds = os.path.dirname(__file__) # Directory of sorTA
	ds = os.path.dirname(os.path.realpath(__file__))
	with open(ds+"/showList.json") as jsonData:
		d = json.load(jsonData)

		if os.name == 'nt':		
			winlC = d["sorTA-Movies"]["win"]
			if os.path.exists(winlC):
				return (d["sorTA-Movies"]["win"]) 
			else:
				print(CRED + "Movie location not found" +CDEF)
				print("Add Movie location using --addloc")
				exit()

		else:
			unixlC = d["sorTA-Movies"]["unix"]
			if os.path.exists(unixlC):
				return (d["sorTA-Movies"]["unix"]) 
			else:
				print(CRED + "Movie location not found" + CDEF)
				print("Add Movie location using --addloc")
				exit()
				



def getCurrentDirectory():
	dirPath = os.getcwd()
	return dirPath


def checkDirectoryName(title):

	directory_name = os.path.basename(directory_chose)
	if fetch_args.p:

		# Match Group 2: /hm1/hm2/hm3/ will get hm3
		# ^\/(.+\/)*(.+)(.+)$
		if os.name == 'nt':
			m = re.match('^[A-Z]:\\(.+\\)*(.+)(.+)$', fetch_args.p) #Win	
		else:
			m = re.match('^\/(.+\/)*(.+)(.+)$', fetch_args.p) #Unix
			
		if m.group(2):
			directory_name = m.group(2)

	title = re.sub('[^a-zA-Z\d\s:]', '', title)

	title = title.strip()
	directory_name = directory_name.strip()

	if re.search(title, directory_name, re.IGNORECASE):
		#print("In Show Folder")	
		return "Show"

	elif directory_name.startswith("Season"):
		#print("In Season Folder")	
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
				if fetch_args.v1:
					print('\033[92m' + "++v1 Messages:onlyfiles[i]:List Files:" + '\033[0m' + onlyfiles[i])
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

	title = checkShowInList(title)


	if fetch_args.v1:
		print('\033[92m' + "++v1 Messages:isWin title,s,f:" + '\033[0m' + "Title:" + title + 
			"s:" + s + "f:" + f)


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


def moveMovie(source, movie):
	
	if fetch_args.m:
		directory_chose = getCurrentDirectory()	

		# If path is set:
		if fetch_args.p:
			print('\033[92m' + "Moving From:" + '\033[0m' + fetch_args.p+movie)
			print('\033[92m' + "Moving To:" + '\033[0m'+ getMovieLocation()+movie)
			shutil.move(fetch_args.p+movie,getMovieLocation()+movie)
		else:
			print('\033[92m' + "Moving From:" + '\033[0m' + getCurrentDirectory()+"/"+movie)
			print('\033[92m' + "Moving To:"+ '\033[0m' + getMovieLocation()+movie)
			shutil.move(getCurrentDirectory()+"/"+movie,getMovieLocation()+movie)
			


def removeLetter_S(t, s, e):

	#print('\033[92m' + "++v1 Messages:removeLetter_S:" + '\033[0m' + "Title: *{}* Season: *{}* Filename: *{}* \
	#	".format(t,s,e))

	if s.startswith("S0"):
		s = s.replace("S0", "")
	elif s.startswith("s0"):
		s = s.replace("s0", "")


	if s.startswith("S"):
		s = s.replace("S", "")
	elif s.startswith("s"):
		s = s.replace("s", "")

	if s.startswith("0"):
		s = s.replace("0", "")
	elif s.startswith("0"):
		s = s.replace("0", "")

	if fetch_args.s:
		move(t.rstrip(), s, e)
	else:
		#print('\033[92m' + "++version1 Messages:move(t.title().rstrip(), s, e):" + '\033[0m' + t.title().rstrip(), s, e)
		
		tR = checkShowInList(t)
	
		if t.rstrip() != tR.rstrip():
			if t.lower().rstrip() == tR.lower().rstrip():
				move(tR.rstrip(), s, e)
		else:
			move(t.title().rstrip(), s, e)



def match(filename_str):

	global show_name
	global season_str
	global movie_count



	m = re.match(regexp1, filename_str)
	

	if m is not None:
		if m.group(10):
			print(m.group(10))
			if m.group(10) != checkShowInList(m.group(10)):
				print("Found Custom Show ({}) for: {}".format(checkShowInList(m.group(10)), m.group(10)))
				show_name = checkShowInList(m.group(10)) # Check if unmatched is in show list json
			#	#print("The group {} and the return {}".format(m.group(8), show_name))
			if fetch_args.s:
				custom_show = fetch_args.s
				
				if ":" in fetch_args.s:
					custom_show = custom_show.split(":")
					for i in range(len(custom_show)):
						custom_show_tmp = custom_show[i]
						custom_show_tmp = custom_show_tmp.replace(" ", ".*") # FIXED REGEXP, WHEN INPUT HAS SPACE BUT FILENAME HAS .
						if re.search(custom_show_tmp, m.group(10), re.IGNORECASE):
							print("Found Show:"+custom_show[i])
							show_name = custom_show[i]
							season_str = ""
				else:
					#print(m.group(8))
					custom_show_tmp = custom_show
					custom_show_tmp = custom_show_tmp.replace(" ", ".*") # FIXED REGEXP, WHEN INPUT HAS SPACE BUT FILENAME HAS .
					if re.search(custom_show_tmp, m.group(10), re.IGNORECASE):
						print("Found Show:"+custom_show)
						show_name = custom_show
						season_str = ""

		elif m.group(1):
			show_name = m.group(2) #Show Name
			season_str = m.group(3)	#Season


		elif m.group(5) and m.group(6):
			#print(m.group(3)) #Movie Name
			#print(m.group(4)) #Movie Year
			show_name = m.group(5) #Show Name
			season_str = m.group(6)	#Season

		elif m.group(2) and m.group(3):
			show_name = m.group(2) #Show Name
			season_str = m.group(3)	#Season
			if season_str.startswith("0"):
				season_str = season_str[1:]


		# Used for movies 
		elif m.group(8):
			
			if m.group(8) != checkShowInList(m.group(8)):
				print("Found Custom Show ({}) for: {}".format(checkShowInList(m.group(8)), m.group(8)))
				show_name = checkShowInList(m.group(8)) # Check if unmatched is in show list json
				#print("The group {} and the return {}".format(m.group(8), show_name))

			if m.group(8) and m.group(9):
				print("Found Movie: {}".format(m.group(8)))
				if fetch_args.m:
					moveMovie(getMovieLocation(), filename_str)

			
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
					#print(m.group(8))
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
  ______                    """+'\033[94m'+"""________   ______"""+'\033[0m'+"""
 /      \                  """+'\033[94m'+"""|        \ /      \\"""+'\033[0m'+""" 
|  $$$$$$\  ______    ______"""+'\033[94m'+"""\$$$$$$$$|  $$$$$$\\"""+'\033[0m'+"""
| $$___\$$ /      \  /      \ """+'\033[94m'+"""| $$   | $$__| $$"""+'\033[0m'+"""
 \$$    \ |  $$$$$$\|  $$$$$$\\"""+'\033[94m'+"""| $$   | $$    $$"""+'\033[0m'+"""
 _\$$$$$$\| $$  | $$| $$   \$$"""+'\033[94m'+"""| $$   | $$$$$$$$"""+'\033[0m'+"""
|  \__| $$| $$__/ $$| $$      """+'\033[94m'+"""| $$   | $$  | $$"""+'\033[0m'+"""
 \$$    $$ \$$    $$| $$      """+'\033[94m'+"""| $$   | $$  | $$"""+'\033[0m'+""" v"""+version+"""
  \$$$$$$   \$$$$$$  \$$       """+'\033[94m'+"""\$$    \$$   \$$"""+'\033[0m'+"""  
			                                   
*************************************""")
	print(date_released)
	print("\nUSE:\nsorta.py -p \"/home/desktop\" <- Specfiy Path \
		\nsorta.py -s SHOW <- Custom Show if sorTA fails to sort \
		\nsorta.py --addshow SHOW <- Add custom show (filename xyz.mp4 sorted into added SHOW)")
	print("*************************************")


def auto():
	logo()
	createCuShJSON()
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

	parser = argparse.ArgumentParser(description='sorTA | Powerful TV Show Sorter')
	parser.add_argument('-p', dest='p', help='Path to sort')
	parser.add_argument('-v', dest='v', help='Show version details', action='store_true')
	parser.add_argument('-m', dest='m', help='Move movies to this location', action='store_true')
	parser.add_argument('-s', dest='s', help='Specify unmatched shows')
	parser.add_argument('--addshow', dest='addshow', help='Custom Show')
	parser.add_argument('--showlist', dest='csl', help='Custom Show List', action='store_true')
	parser.add_argument('--addloc', dest='ml', help='Move movies to this location')
	parser.add_argument('--showloc', dest='sloc', help='Show movie locations', action='store_true')
	parser.add_argument('--qe', dest='qe', help='Queue Episodes', action='store_true')
	parser.add_argument('--v1', dest='v1', help='Display more info to console', action='store_true')
	parser.add_argument('--logo', dest='l', help='Print Logo', action='store_true')

	fetch_args = parser.parse_args()

	if fetch_args.p:
		logo()
		print(("Path Selection: {}".format(fetch_args.p)))
		option_2 = input('Is the path correct? Y/n: ')
		if option_2 == "y" or option_2 == "Y" or option_2 == "":
			directory_chose = fetch_args.p
			listFiles(fetch_args.p)
		else:
			print(goodbye_msg)

	elif fetch_args.l:
		logo()

	elif fetch_args.ml:
		addMovieLoc(fetch_args.ml)

	elif fetch_args.sloc:
		getloc()

	elif fetch_args.v:
		print("Current version: v{}".format(version))

	elif fetch_args.csl:
		getShowList()

	elif fetch_args.addshow:
		addCustomShow(fetch_args.addshow)

	else:
		auto()