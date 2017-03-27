(c) Copyright Martin Paul Eve, 2016. Released under the GNU Public Affero License v3. See LICENSE for more. 

# dateFile.py

Takes a file called infile.txt and produces an output file, dated_outfile.csv, that contains a list of dates for each word in infile.txt.

The program expects there to be one word per line in infile.txt.

Anticipated usage is for verifying linguistic accuracy of language used in historical fiction/parody.

At the moment, this tool searches for usages on dictionary.com that specify a date range (e.g. 1900-1905) and single dates (900, "before 900") etc.

This scraper uses dictionary.com

# OEDdate.py

Takes a file called infile.txt and produces an output file, dated_outfile.csv, that contains a list of dates for each word in infile.txt.

The program expects there to be one word per line in infile.txt.

Anticipated usage is for verifying linguistic accuracy of language used in historical fiction/parody

This scraper uses the experimental Oxford Dictionaries API: https://developer.oxforddictionaries.com/our-data

# findPopularity.py

Uses Merriam Webster's "how popular is this word" feature to produce an output CSV of popularity for words within "outfile.txt".

# OEDObsolete.py

Takes a file called infile.txt and produces an output file, dated_outfile.csv, that contains a true or false value for each word in infile.txt found in the OED specifying whether the word is obsolete or not.

This scraper uses the experimental Oxford Dictionaries API: https://developer.oxforddictionaries.com/our-data