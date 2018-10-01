# SorTA - Powerful TV Show Sorter

SorTA is a powerful TV Show file sorter that will match **Name.s01e01** and sort it into folders based on the Name and Season.

xyz.s01e01.mp4 will be sorted as follows:

 - xyz.s01e01.mp4 is cut
 - xyz folder created
 - Season 1 sub-folder created inside xyz
 - File is pasted into xyz/Season 1/xyz.s01e01.mp4

___
### Installation & Usage

SorTA requires Python v3 to run.

Specify path to sort:

```sh
user@host: sorta.py -p "c:/files/videos/shows"
```
Automatically sort current working directory:
```sh
user@host: sorta.py 
```
Custom Show if sorTA fails to sort, will check if filename with xyz exists and make folder:
```sh
user@host: sorta.py -s xyz
```
Queue Episodes for watching inside season folder, e.g /XYZ/Season 1/Episodes/'''FILES DROPPED HERE''':
```sh
user@host: sorta.py -qe
```

___
### Future development
- Clean Titles ( xyz.s01e02.ABC.[720p].mp4 -> xyz.s01e02.mp4 )
- Move files to another specified location ( sorta.py -mp "/xyz" :All files moved here)
- Check filesize and replace smaller file 
- Append move date to filename ( Date File: xyz.s01e02 - Title[10-09-2018].mp4 )
- Custom RegExp: Specify Name #Added 1.3.3
- Movie Support 
- Config File

___
### Author
@MickCue
