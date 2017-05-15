# SorTA - Powerful Sorter

SorTA is a powerful file sorter that will match **file.s01e01** and move it into the folder **file**->**s1**.

  - Takes in location parameter
  - Creates diretory stucture based on filename
  - Moves files

file.s01e01 will be sorted as follows:

file.s01e01 (Removed From Here)
File (Creates This Folder)
Season 1 (Creates This Folder)
file.s01e01 (Dropped Here)

___
### Installation

SorTA requires Python v3 to run.

```sh
user@host: sorta.py -p "c:/files"
```

___
### Version History

**Current version:** v1.0  - 11th March 2017
___
### Future development
Priority[1-3]
- Check for script updates [3]
- Move files to another specified location [2]
- Check filesize and replace smaller file[Optional Command] [2]
- Move inside folder based on season filename...e.g filname12>sunday.s03e01>>>>>>Season 3>filename12.s03e01 [1]
- Pull all files from Folders in sub folder..e.g Season 1> File.s1e2 [3]
- Append move date to filename [Optional Command] [2]

___
### Author
@MickCue
