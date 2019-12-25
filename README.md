# x_ops module "Crosstalk"

Crossword constructor tool for beginners

### Setup
Simply download and unzip the folder - then run the x_ops program, enter the file location of your (unscored) wordlist, and start mining it for themes!

1. Get the wordlist:
    * -(E.g. in crossword compiler, go to Words->Word List Manager->Convert->List to Plain Text File .. do not include word scores.)
1.  Double-click to run the x_ops.exe file from the folder you unzipped
1.  In the window that pops up, type in the file location of your list, e.g.:  C:\Downloads\mylist.txt
1.  Use the functions to mine your list.  It's that easy!

### Crossword Archetypes Currently Supported
* Add a phrase to make another valid phrase
  * `add mit` yields words like COMMITMENT (comment+mit)
* Anagrams - 10 randomly selected anagrams are tested<sup>1</sup>
  * `anagram mouse` yields words like EXCUSEMOI on one try, BECOMEUSELESS on another, or nothing on another
* Backwards entries
  * `backwards party` yields words like VENUSFLYTRAP
* Beginning of a phrase
  * `b qa` yields words like QATAR
* Ending a phrase
  * `e zz` yields words like HOTFUZZ
* Near-same words
  * `near mouse` yields words like MOOSE
* One-off, with a specific letter (This is a sample specialty search, where you need the missing letters to spell something in particular)
  * `oneoff moss` , then `a` yields all words containing both MOAS (e.g. SAMOAS) and MASS (e.g. LEGMASSAGE).
* Regex - for advanced users, you can use straight python regex: https://docs.python.org/3/library/re.html
  * `regex ^bea.*dy$` yields words like BEARDEDLADY
* Sandwich a phrase as the bun outside another phrase
  * `sandwich bacon` yields words like BACKGAMMON
  
### Utility functions
* Plus - add a word to the list
  * `plus livinmybestlife` adds LIVINMYBESTLIFE to the list
* Minus - delete a word from the list
  * `minus fetch` removes FETCH from the list; seriously stop trying to make fetch happen
* Write - write the entire wordlist in memory to a new file
  * `write my_new_list` writes the your list to the file my_new_list.txt
  
### Notes
* You can limit the range of results - just type in a number or range of numbers separated by a dash to restrict the output: `5-16`
* Type 'help' to get a list of keywords and a short description
* Use `.` as for a wildcard "any letter"
* Regex expressions work on the endpoints.  So you could do something like `b [A,U][A,G]` for words that begin with the combinations of A or U as the first letter and A or G as the second letter.

### Disclaimers
* This module is not intended for entries with spaces.  You can do some stuff like `regex $STAR W.*` to get STAR WARS on such a list, but all functionality is not guaranteed
* This release is not optimized by, nor does it support, word scores
* Decoding is basic utf8, so nonstandard A-Z characters are **IGNORED**.  ÉCHAMELACULPA will render as only CHAMELACULPA in the list

<sup>1</sup>Possible anagrams increase exponentially, with 6 possibilities for a 3-letter word and 720 possibilities for a 6-letter word.  This particular release does not have an optimization module for re-searching a giant wordlist that many times, so a random subset is taken.

x_ops "Crosstalk" release v1.0
All rights reserved
