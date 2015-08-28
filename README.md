# README 

---

This script uses the LibGuides API to create metadata records for research guides that:
	
* are published
* have a guide type of (can change this with **option parsing settings**):
	* course
	* subject
	* or topic
* have a description 

##### To run:

1. Modify apikey.txt with your api key.
2. Create a writeable directory called 'temp' in the same directory as the script. 
3. Run pylibguides.py

##### Options (none are required):

**Default Settings**

The default settings are:

* Status published
* Course, Subject, and Topic Guides
* Since the beginning of time

**Getting more specific**

The following options are available:

* -h "Shows the help message and exits"
* -f "Enter a date as yyyy-mm-dd and harvest records updated or created since then"
* -g "Specify the types of guide you want to return in a comma separated list (1,2,3)"
	* 1 for General
	* 2 for Course
	* 3 for Subject
	* 4 for Topic
	* 5 for Internal
	* 6 for Template
* -s "Specify the status of the types of guides you want in a comma separated listed (0,1)" 
	* 0 for Unpublished
	* 1 for Published
	* 2 for Private
	* 3 for Submit for Review 
	
#### Example:

This is an example of a command that can be executed from the command line.  It overrides the defaults and creates metadata records for all LibGuides created since April 1, 2015 that have the type of course or subject and are published:

	python pylibguides.py -f 2015-04-01 -g 2,3 -s 1
