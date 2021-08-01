# gwynantblacklist
A script that scrapes various pieces of info from the campsite booking system and compares against a blacklist CSV file, flagging any matches.  

A slightly modified version of this script currently runs once a day on my machine at work.  The script uses Python's Selenium framework to navigate 
and then scrape data from a campsite booking system.  It then compares this data against a blacklist held in CSV format and reports any matches that 
are found.  It was written in the absense of blacklist functionality within the booking system itself.  

This script means that the campsite now has an effective way of ensuring that troublemakers are unable to return time and time again.  
