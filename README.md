# OCR_dutch_books
OCR_dutch_books_smeets

Evaluation of the OCR refinement for Dutch books created by Radboud University studies. 

Problem:
The program is running very slowly. 

Potential problems:
1. Use of Bert.
2. Use manual Levenshtein distance calculations comparing every word with an extensive dictionary.
3. Heavy use of global variables.
4. Extensive use of O/I files.
5. Unnecessary use of regex.

Test corpora:


Experiment:
Rewrite code to minimize the use of regex, O/I files and global variables. 

