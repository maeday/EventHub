EventHub
========

Setup
-----
Creating a local settings file:  
* Copy the file 'settings.py' from 'EventHub' and name it 
  'settings_local.py'
* Delete the last 5 lines of 'settings_local.py'
* Modify any settings in 'settings_local.py' that you want

Notes:  
* Please use the branch 'dev' to do development work. This branch 
  will be merged to 'master' for each release
* To switch to branch 'dev', enter the command: 
  `git checkout -b dev origin/dev`
* Please use the branch 'readme' to make changes to the README (_and_
  _only to the README_). This is to prevent the need to cherry pick 
  commits and from merge conflicts that can result from doing so
* For those of you unfamiliar with Python syntax, Python is strict 
  about consistent indentation. _Tabs and spaces do not mix well._ 
  **DO NOT USE TABS. ONLY USE SPACES!**
