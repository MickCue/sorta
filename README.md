# SorTA - Powerful TV Show Sorter

SorTA is a powerful TV Show file sorter that will match **Name.s01e01** and sort it into folders based on the Name and Season.

The.TV.SHOW.s01e01.mp4 will be sorted as follows:

 - The.TV.SHOW.s01e01.mp4 is cut
 - The.TV.SHOW folder created
 - Season 1 sub-folder created inside The.TV.SHOW
 - File is pasted into The.TV.SHOW/Season 1/The.TV.SHOW.s01e01.mp4

___
### Installation & Usage

SorTA requires Python v3 to run.
Recommend adding sorTA.py to path (Enviromental Variable)

Add Show (One at a time):
--addshow "The.TV.SHOW:Xero Yi Zone"

Specify Unmatched Show (One at a time/Multiple):
-s "The.TV.SHOW"
-s "The.TV.SHOW:abc:pcb" # Matches media files begining with these

Specify path to sort:

```sh
user@host: sorta.py -p "c:/files/videos/shows"
```
Automatically sort current working directory:
```sh
user@host: sorta.py
```
Custom Show if sorTA fails to sort, will check if filename with The.TV.SHOW exists and make folder:
```sh
user@host: sorta.py -s The.TV.SHOW
```
Queue Episodes for watching inside season folder, e.g /The.TV.SHOW/Season 1/Episodes/'''FILES DROPPED HERE''':
```sh
user@host: sorta.py -qe
```sh
user@host: sorta.py -f
```
Fix titles e.g s01 -> S02 & upper show names
```



Misc Examples

Match media filename that begins with "The.TV.SHOW" and sort into folder "The.TV.SHOW" that is in a specific path:

```sh
user@host: sorta.py -s "The.TV.SHOW" -p /home/shows/

```

Match media "The.TV.SHOW" and name it "Xero Yi Zone" which will create folder with that name and move "The.TV.SHOW" into it:

```sh
user@host: sorta.py --addshow "The.TV.SHOW:Xero Yi Zone"

```

___
### Future Development
- Clean Titles ( The.TV.SHOW.s01e02.ABC.[720p].mp4 -> The.TV.SHOW.s01e02.mp4 )
- Move files to another specified location ( sorta.py -mp "/The.TV.SHOW" :All files moved here)
- Check filesize and replace smaller file
- Append move date to filename ( Date File: The.TV.SHOW.s01e02 - Title[10-09-2018].mp4 )
- Custom RegExp: Specify Name #Added 1.3.3
- Movie Support
- Config File

___
### Author
@MickCue
