Summary
-
turnout2020.py script will fetch voter data file from the Ohio Secretary of State website and match it with the existing file.


The Ohio Secretary of State website
https://www6.ohiosos.gov/ords/f?p=VOTERFTP:HOME::::::


The input file
https://drive.google.com/file/d/1jAAgd5js_PtdFONuQFGXnni-Bdx0oEg4/view

As a result, a new CSV file (output.csv) will be generated.  The data columns are row, name, birth_year, address, city, state, zip, and matched_voterid.

--------------------------------------------------


Environment 
-

Python 3.7.6

Required packages to install:

- fuzzywuzzy:  for fuzzy comparing fields : pip install fuzzywuzzy

- python-Levenshtein (optional, provides a 4-10x speedup in String
Matching) : pip install python-Levenshtein

- python-dateutil : for extracting a year from DATE_OF_BIRTH field  rather than a manual string parse process : pip install python-dateutil

To run 

- Check that your python version is 3.X not 2.X
- Install the required packages
- Unzip
- From the unzipped folder, run 'python turnout2020_code.py'
-------------------------------------------------------------------

Approach
-

The script loads the input CSV file and creates a list of voter objects.

After it loads the voter file from the Ohio Secretary of State website, it loops through each data row and compares it with the list of voter object

It begins to compares 'must-match' fields such as 'zip', 'state', 'city', 'birth_year'.


It then splits the Ohio state voters' address into a street number and address info. 

First, it searches the exact match for the street number.  

To accommodate pre-dir, pre-fix, post-fix, post-dir on the address data, it applies a fuzzy partial ratio score above 80.


For the name comparison, it joins the Ohio state voters' first, middle, last name, then checks both fuzzy token and a partial ratio scores are above 70.

The detail of the fuzzywuzzy package can be found at https://github.com/seatgeek/fuzzywuzzy

When a match is found, it updates the voter object's 'matched_voterid' field with 'SOS_VOTERID'


Finally, the "output.csv" file will be generated with the updated voter data.

----------------------------------------------------------------

Future improvements -------------------------------------------------

First of all, data matching can be improved by researching more about different tools and algorithms.  I found that there is a false positive case where two people who live in the same house, have the same birth year and similar name. (twin sibling or a married couple with a similar name).

Since the data process takes quite a long time, I would do more research on improving that.

