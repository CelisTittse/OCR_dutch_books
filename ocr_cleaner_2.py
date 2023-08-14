# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 15:20:49 2023

@author: Celis Tittse
"""

# -*- coding: utf-8 -*-

import regex as re
import os
import multiprocessing

""" Data Science Project - OCR post-correction code - Revisited """

"""Part 0: Preparations."""
'''Part 0.1: Open lexicon with names, words and numbers till 1000 in Dutch'''
def open_lexicon ():

  """ Open local files with names and dutch words"""  
  with open("full_wordlist.txt", encoding = 'utf-8-sig') as wordlist_f:
      wordlist = [word.strip() for word in wordlist_f.readlines()]
      wordlist_f.close()
      
  return wordlist


'''Part 0.2: Open book OCR'''
def open_book_txt (titel):
    
    """Open the txt with the title from bookmarks.txt and return as tekst list with lines"""
    with open(titel,"r", encoding = 'utf-8-sig') as tekst_f:
        tekst_lines = [line.strip() for line in tekst_f.readlines()]
        tekst_f.close()
        
    return tekst_lines


def vind_paginanummers(line):
  
  """Find lines that contain a misread page number."""
  line = line.strip()
  if len(line) < 5:
    line = re.sub(pattern = " ",repl = "",string = line)
  if len(line) < 4:
    """Check if the line contains the following pattern:
    1. any non digit character -- [^\d]
    2. followd by any character, zero or more times -- .*
    3. followed by a character that's none of the following characters -- .!?’'"/-:)K
    4. followed by the end of the line.
    """
    if len(re.findall(pattern = "[^\d].*[^\.!\?’'\"/\-:\)K]$",string = line)) > 0:
      origineel = line
      """Repair a misread page number."""
      if len(re.findall(pattern = "[^VXIL]",string = line)) > 0:
        line = re.sub(pattern = "[JIiTj*l!rïxX»«']",repl = "1",string = line)
        line = re.sub(pattern = "[nMH\"u”]",repl = "11",string = line)
        line = re.sub(pattern = "[oO°óÓ]",repl = "0",string = line)
        line = re.sub(pattern = "\?",repl = "7",string = line)
        line = re.sub(pattern = "g",repl = "9",string = line)
        line = re.sub(pattern = "a",repl = "2",string = line)
        line = re.sub(pattern = "\.",repl = "",string = line)
      if len(re.findall(pattern = "^I+$",string = line)) > 0:
        line = re.sub(pattern = "I",repl = "1",string = line)
      if len(re.findall(pattern = "[^\dVXIL]",string = line)) > 0:
        line = origineel

  return line


def paginanummers_fixen_en_verwijderen(tekst_lines):
  
  """Remove pagenumbers.
  input: String that contains the name of your text file.
  output: A new list without page numbers. 
  """
  nieuw_bestand = []
  
  for line_o in tekst_lines:
    line = vind_paginanummers(line_o)
    
    """Write all lines that are not a page number to your new text file."""
    if not (len(line)<6 and re.search(pattern = "[^\dVXIL]",string = line) == None):
        nieuw_bestand.append(line)

  return nieuw_bestand


"""Part 2: corrections on line-level"""

def spatieoplossing(line, lexicon):
    
    """Fix two white space errors.
    input: a line (string) from the textfile.
    output: a (string) line from the textfile with less white space errors.
    """
    
    """Count the number of spaces and the number of non-spaces in each line.
    
    Key arguments:
    spaties -- integer variable with the number of spaces 
    andere -- integer variable with the number of non-spaces
      """
    line = line.strip()
    
    spaties = line.count(' ')
    andere = len(line) - spaties
    
    """Split line on white spaces."""
    zin = ""
    
    for word in line:
      """Remove spaces inbetween isolated characters.
      
      Key arguments:
      line -- list of words (characters separated by spaces) that make up your line.
      zin -- string variable that will contain the new line.
      Add all words in 'line' to 'zin' with spaces inbetween, unless there's more than one isolated character in a row. Then, put no spaces inbetween these characters.
      """
      if len(word) != 1:
        if len(zin) ==  0:
          zin += (word+" ")
        else:
          zin += (" "+word+" ")
      elif re.search(string = word,pattern = "[.,!?]"):
        zin += (word+" ")
      else:
        zin += word
    
    """Replace multiple successive spaces with only a single space."""
    line = re.sub(string = zin, pattern = " {2,}",repl = " ") 
    """If a line ends with a space, remove this whites space"""
    if line.endswith(" "):
      line = line[0:(len(line)-1)]
    
    """If the percentage of spaces in the line is more than 37, remove all spaces."""
    if(spaties/(spaties+andere)>0.37):
      beginpunt = 0
      line_los = ""
      """Add spaces to form longest possible words.
      
      Key arguments:
      beginpunt -- integer variable that contains the index of the character in the old line without spaces that the next word in the new line starts with.
      line_los -- string variable that will be the new line by adding words and spaces.
      tijdelijk -- string variable that contains an increasingly smaller part of the initial line without spaces.
      """
      while beginpunt < len(line):
        """
        If 'tijdelijk' is in your lexicon, add 'tijdelijk' to 'line_los.
        If 'tijdelijk' is not in your lexicon, or is a puntuation character, or is just one character long, Remove one character from 'tijdelijk'.
        """
        for i in range(len(line)):
          tijdelijk = line[beginpunt:len(line)-i]
          
          if (tijdelijk.lower() in lexicon
              or tijdelijk in "([-—.,:;!\?'\(\) ])" 
              or len(tijdelijk) == 1):
            beginpunt = len(line)-i
            break

        line_los += tijdelijk+" "
      line_los += "\n"
      """Replace multiple successive white spaces with only a single white space."""
      line_los = re.sub(string = line_los, pattern = " {2,}",repl = " ")
      """If a line ends with a white space, remove this whites space"""
      line_los = re.sub(string = line_los, pattern = " ([-—.,:;!\?\(\) ])",repl = "\\1")  
      return(line_los)
    
    line += "\n"
    
    return line


''' 2.0 Repair words that have been split in twain by end of line hyphenation '''
def verwijder_regelafbrekingen(line, deel1, regelafbraak):
  
  """Remove end-of-line hyphenation and glue the broken off word back together.  
  
  Key arguments:
  regelafbraak -- boolean variable that is set to 'True' when end-of-line hyphenation is found and is set back to 'False' when the broken off word is glued together again.
  deel1 -- string variable that contains the first part of the broken off word.
  input: 
  1. 'line', containing the line.
  2. 'deel1' (empty at first), containing the first part of a broken off word. 
  3. 'regelafbraak' (default is 'False'), containing a boolean that says if there has been a detection of end-of-line hyphenation in the previous line.
 
  Set 'regelafbraak to 'False' when the previous sentence contained end-of-line hyphenation."""
  if regelafbraak == True:
    strippedline = line.strip()
    #for when there's only a linenumber on a line:
    if not strippedline.isdigit():
      regelafbraak = False
      #plakt woorddelen aan elkaar:
      "Paste the first part of the word in front of the second part of the word."
      line = deel1+line 
  """
  Check if line ends with end-of-line hyphenation.
  If so, assign the first part of the broken off word in 'deel1', set 'regelafbraak' to 'True'.
  """
  if line.endswith("-\n") and not line.endswith(" -\n"):
    """
    Check if the following pattern is in the line:
    1. a space
    2. then any letter in the alphabet one or more times
    3. then a hyphen
    4. then an end-of-line character
    """
    match = re.findall(string = line, pattern = " [a-z]+-\n",flags = re.IGNORECASE)
    if len(match)>0:
      regelafbraak = True
      deel1 = match[0]
      """Remove the first part of the broken off word."""
      line = line.replace(deel1,"\n")
      """Assign the first part of the broken off word to 'deel1'."""
      deel1 = re.sub(string = deel1, pattern = " ([a-z]+)-\n", repl = "\\1")
  
  return line, deel1, regelafbraak


'''2.1. Repair words that have been split in twain by a page number at the end of a line. '''
def fix_paginanummers_eindvdzin(line, deel1, paginanummereind):
  
  """Paste broken off words together that have been separated by a page number at the end of a sentence. 
  For example: 'sep48\narated'.
  Key arguments:
  paginanummereind -- boolean variable that is set to 'True' when a case is found and is set back to 'False' when the broken off word is glued together again.
  deel1 -- string variable that contains the first part of the broken off word.
  input: 
  1. 'line', containing the line.
  2. 'deel1' (empty at first), containing the first part of a broken off word. 
  3. 'paginanummereind' (default is 'False'), containing a boolean that says if there has been a detection of a case in the previous line.
  
  Paste the first part of the broken off word in front of the second part of the word,, and then set paginanummereind to False, when a case has been detected.
  """
  if paginanummereind:
    line = deel1+line
    paginanummereind = False
  """
  Check if the following pattern is in the line:
  1. a space
  2. then any letter in the alphabet one or more times
  3. then any number between 0 and 9 one or more times
  4. then an end-of-line character
  If so, remove that part of the line and assign the first part of the word to 'deel1'.
  """
  matches = re.findall(pattern = " [a-z]+[0-9]+\n",string = line)
  if len(matches)>0:
    paginanummereind = True
    deel1 = matches[0]
    line = line.replace(deel1,"\n")
    deel1 = re.sub(string = deel1, pattern = " ([a-z]+)[0-9]+\n", repl = "\\1")
  
  return line, deel1, paginanummereind


def aanhalingstekens_fixen(line, wordlist):
  
  """Fix wrongly recognized quotation marks.
  
  Key arguments:
  linelist -- list that contains your line, split by white spaces, so every position in the list contains a new word or punctuation mark.
  new_linelist -- (starts out empty.) list that will contain the a list of alle the words and puntuation marks in the line.
  startswithquotation -- (default is set to 'False' with every line.) a boolean that says if the current line starts with a quotation mark.
  """
  linelist = line.split()
  new_linelist = []
  
  for word in linelist:
    startswithquotation = False

    """Remove the quotation mark if a word starts with a quotation mark. """
    if word.startswith("'"):
      word = word[1:]
      startswithquotation = True

    """Check if word is not in your lexicon."""
    woord_in_woordenboek = re.search(pattern = re.escape(word.lower()), string = ' '.join(wordlist))
    if woord_in_woordenboek ==  None:

      """Check if the word contains the following pattern:
      1. any letter in the alphabet
      2. followed by one of the characters that are often mistaken for a close quote: '*', '/', 'e', 'c', or any digit.
      """
      pattern_in_word = re.search(pattern = "[a-z][*/ec\d]$", string = word)
      """Check if the word contains the following pattern:
      1. any letter in the alphabet
      2. followed by '!','?' or '.'
      3. followed by one of the characters that are often mistaken for a close quote: '*', '/', 'e', 'c', or any digit.
      """
      pattern_with_punct_in_word = re.search(pattern = "[a-z][!\.\?][*/ec\d]$", string = word)
      
      if pattern_with_punct_in_word:
        """Check if the word without the last two characters is in the lexion."""
        punctuation = word[-2]
        word_til_last_char = word[:-2]
        pattern_in_wordlist = re.search(pattern = re.escape(word_til_last_char.lower()), string = ' '.join(wordlist))
        
        if pattern_in_wordlist:
          """If so, overwrite word with the actual word + the punctuation mark + a close quote."""
          word = word_til_last_char+punctuation+"'"
      
      elif pattern_in_word:
        """Check if the word without the last character is in the lexicon."""
        word_til_last_char = word[:-1]
        pattern_in_wordlist = re.search(pattern = re.escape(word_til_last_char.lower()), string = ' '.join(wordlist))
        
        if pattern_in_wordlist:
          """If so, overwrite word with the actual word + the punctuation mark + a close quote."""
          word = word_til_last_char+"'"
    
    if startswithquotation:
      """If the word started with a quotation mark, add it again."""
      word = "'"+word
    """Append every word to the new list."""
    new_linelist.append(word)

  """Turn the list containing the line into a string again by joining the words with a space inbetween."""
  line = ' '.join(new_linelist)

  return line
  

"""Part 3: Fixes on word-level."""

'''3.1. Repairs frequently misread quotation marks. '''
def leestekens_losmaken(line, wordlist):
  
  """Separates punctuation characters from the words.
  
  input: 
  1.'line' with a string containing the line.
  2. 'wordlist', containing the lexicon as a string.
  output: 'line', with a string containing the line, but now with spaces around the punctuation characters.
  
  Remove excessive spaces."""
  line = re.sub(pattern = " {2,}",repl = " ",string = line)
  """Replace all different kinds of quotation mark for a single kind"""
  line = re.sub(pattern = '"|’|‘|”|«|»|„|“|”',repl = "'",string = line)
  line = aanhalingstekens_fixen(line, wordlist)
  line = line.strip()
  """Place white spaces around punctuation characters. (This is in order to separate the punctuation characters from the words. This will later be turned back.)
  """
  line = re.sub(pattern = "([-—.,:;!\?'\(\)])",repl = " \\1 ",string = line)
  
  return line


"""#3.2. Hardcoding op lineniveau"""
def losse_beginletter_fixen (line, wordlist):

  """
  Fix words from which the first letter has been separated by the rest of the word by a white space. 
  For example: 's eparated'.
  Check if the following pattern is in the line:
  1. first, a space
  2. followed by one of these letters: 'abcdefghijklmnopqrtvwxyz' once.
  3. followed by a space.
  4. followed by two or more letters of the alphabet.
  """
  patroon = "\s[a-z]{1}\s[a-z]{2,}"
  matches = re.findall(pattern = patroon, string = line)
  """
  For every match to the pattern in the line, do the following: 
  1. save the isolated character in 'eersteletter' and the rest of the letters in 'restvanwoord'.
  2. if 'restvanwoord' is not in the lexicon and if 'eersteletter'+'restvanwoord' is, remove the white space.
  """
  if matches != []:
    for geval in matches:
        restvanwoord, eersteletter = geval.split()
        
        if (restvanwoord.lower() not in wordlist
            and ''.join([restvanwoord, eersteletter]).lower() in wordlist):
            line.replace(geval, ''.join([restvanwoord, eersteletter]))

  return line


'''#3.3. Do some hardcoding on frequent mistakes.'''
def hardcoding_op_woordniveau(line):
    
    """
    Replace the often misrecognized character 'ç' in 'curaçao' or 'Curaçao'.
    Replace the following pattern:
    1. first 'C' or 'c'.
    2. then 'ura'.
    2. then any character.
    3. then 'ao'.
    by part 1, 2 and 4, and instead of part 3, place a 'ç'.
    """
    line = re.sub(pattern = "([Cc]ura).(ao)", repl = "\\1ç\\2", string = line)
      
    """Replace the pattern - starts and ends with 'TK' or 'Tk'- by 'Ik'."""
    if 'TK' in line.split() or 'Tk' in line.split():
        line = re.sub(pattern = "TK|Tk", repl = "Ik", string = line)

    return line


"""Part 4: Remove the excessive spaces around the punctuation marks."""
def plak_leestekens(line):
  
  line = re.sub(pattern = " ([-—.,:;!\?'\(\)]) ",repl = "\\1",string = line)
  
  return line


''' Make the OCR txt files cleaner ''' 
def ocr_verbetering ():

    if __name__ == "__main__":  
      """Part 0: The overarching function."""
    
      """Add names and numbers to the lexicon."""
      #This function is executed only once.
      # 0.1 Open lexicon with Dutch words, names and numbers
      wordlist = open_lexicon()
    
      """Open a (readable) connection to a text file with on every line the file name of a text you want to process."""
      boekenlijst = [boek.strip() for boek in open('boeknamen.txt',"rt", encoding = 'utf-8-sig').readlines()]
    
      """For every text, run the entire algorithm."""
      for titel in boekenlijst:

        # 0.2 Open book
        text_lines = open_book_txt(titel)
        
        # 0.2 Rewrite pages and remove in between page numbers
        tekst_zonder_p_nrs = paginanummers_fixen_en_verwijderen(text_lines)
    
        #Starting variables:
        regelafbraak = paginanummereind = False
        deel1 = deel1vanwoord = ""
        paginanummereind = False
        klaar = []

        #Correct texts line by line:
        for line in tekst_zonder_p_nrs:
          
          #1. Fix words consisting of loose letters ('c h i l d' becomes'child').
          line = spatieoplossing(line, wordlist)
    
          #2.0 Repair words that have been split in twain by end of line hyphenation. ('sep-\narate' becomes '\nseparate').
          line,deel1,regelafbraak = verwijder_regelafbrekingen(line,deel1,regelafbraak)
          
          #2.1 Repair words that have been split in twain by a page number at the end of a line. ('sep44\narate' becomes '\nseparate').
          line,deel1vanwoord,paginanummereind = fix_paginanummers_eindvdzin(line, deel1vanwoord, paginanummereind)
        
          #3. Put spaces between words and punctuation marks, so that every word can be found in the lexicon ('dog.' becomes 'dog . ').
          #3.1. Repairs frequently misread quotation marks. ('Hallo?/ becomes 'Hallo?').
          line = leestekens_losmaken(line, wordlist)
    
          #3.2 Fix loose first letters, like in 'l etter'.
          line = losse_beginletter_fixen(line, wordlist)
          
          #3.3. Do some hardcoding on frequent mistakes.
          line = hardcoding_op_woordniveau(line)
          
          #6. Remove excessive spacing around punctuation marks.
          line = plak_leestekens(line)
          
          klaar.append(line)
          
        # Save corrected OCR tekst to new txt file
        with open('./verbeterd/' + titel.replace('.txt', '') + '_verbeterd.txt', 
                  mode = 'w', encoding = 'utf-8-sig') as verbeterde_tekst_f:
            verbeterde_tekst_f.write('\n'.join(klaar))
            verbeterde_tekst_f.close()
            
        print('{st} is saved as {st}_verbeterd'.format(st = titel.replace('.txt', '')))
        
    return 

for i in range(4): 
    p = multiprocessing.Process(target = ocr_verbetering(), 
                                args=['output'+str(i)])
    p.start()





