# SorTA - Powerful TV Show Sorter

SorTA is a powerful TV Show file sorter that will match **Name.s01e01** and sort it into folders based on the Name and Season.

file.s01e01 will be sorted as follows:

 - TV.name.s01e01 (Removed)
 - TV Name (Creates This Folder) 
 - Season 1 (Creates This sub-folder) 
 - File/Season 1/TV.name.s01e01 (File Dropped Here)

___
### Installation

SorTA requires Python v3 to run.

Specify path to sort:

```sh
user@host: sorta.py -p "c:/files/videos/shows"
```
Automatically sort current working directory:
```sh
user@host: sorta.py 
```

___
### Future development
Priority[1-3]
- S01:Check for script updates [3]
- S02:Move files to another specified location [2]
- S03:Check filesize and replace smaller file[Optional Command] [2]
- S04:Sort folders with the file.s01e01 name/ Move to specified folder after implementing S02 [3]
- S05:Append move date to filename [Optional Command] [2]

___
### Author
@MickCue
