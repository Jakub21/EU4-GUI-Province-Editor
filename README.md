# EU4 GUI Province Editor
Created by [Jakub21](https://github.com/Jakub21)  
Editor [GitHub Repository](https://github.com/Jakub21/EU4-GUI-Province-Editor)  
Started Feb. 2018



## General usage

#### Python
Program was developed for [Python 3.6](https://www.python.org/). As of May 2018 program was not tested with other versions of Python.

#### Packages
The following packages are required to run the program
- [wxPython](https://www.wxpython.org/)
- [PyYAML](https://pyyaml.org/)

#### Executable
To run program execute `Editor.pyw` with Python 3. To open debug console in background execute `Debug.py` instead. No argument are taken.

#### First use
When program is launched first time a Configurator will start. Selecting assignment and localisation files is mandatory. Check [Configurator Section](#Configurator) for detailed description.



## Configurator
To open configurator, on top bar, click `Main` menu and choose `Run Configurator` option

#### Files
Editor needs 4 files from game directory to work properly. These are:
- Area assignment file (path is `game/map/area.txt`)
- Region assignment file (path is `game/map/region.txt`)
- Super-region assignment file (path is `game/map/superregion.txt`)
- Province names localisation file (path is `game/localisation/prov_names_l_LANG.yml`) User can choose any language variation.

#### Display
Program displays data representation in frame in the center of main window. In configurator there are a few options that affect the way program does it. These are:
- `Font size`: Modifies font size in representation frame.
- `Hide provinces with no super-region`: Do not display provinces that are not assigned to any super-region.
- `Hide provinces with specified super-regions`: Do not display provinces that are assigned to super-region listed in `Hidden super-regions`
- `Hidden columns`: Do not display checked columns.



## Commands
Program can receive commands from Command Line and text file with Commands Set. This section explains how to use commands.

#### List syntax
Commands parser supports lists. If argument allows multiple values, wrap those values in `[]`. See examples below:
```
select sub area [champagne ile_de_france]
```
```
in prov [183 4389] fort yes
```
#### Comments
To add comment use `>#`. Comment ends when next `>` character is found. Example:
```
> command
># This is comment
Comments end when 'is larger' char is found. There is one in next line.
> command
```
#### Commands File
In files, each command should start with `>` and first word should be preceded with space. Example:
```
> select new culture westphalian
```

#### Valid Commands
List of valid commands (functions) with arguments  
`[]` - Required argument,  
`{}` - Conditional argument,  
`*` - Argument supports multiple values,  
###### Load
```
load [type] [path] {date}
```
`{date}` argument is only required if `[type]` has value `orig`
###### Load-Update
```
loadu [type] [path] {date}
```
`{date}` argument is only required if `[type]` has value `orig`
###### Save
```
save [type] [path]
```
###### Select
```
select [attribute] [columns]*
```
###### Sort
```
sort [mode]
```
###### Set
```
set [attribute] [value]
```
###### In-scope
```
in [condition attribute] [condition value]* [value attribute] [value]
```
###### Represent
```
repr
```
###### Exit
```
exit
```
