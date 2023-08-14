# OCR_dutch_books
OCR_dutch_books_smeets

Evaluation of the OCR refinement for Dutch books created by Radboud University studies. 

Problem:
The program is running very slowly. 

Potential problems:
1. Heavy use of global variables.
2. Extensive use of O/I files.
3. Unnecessary use of regex.
4. Use of Bert.
5. Use manual Levenshtein distance calculations comparing every word with an extensive dictionary.

Test corpora:
Fragment from De Ontdekking van de Hemel (Harry Mulisch, 1992) (2057 words)
Fragment from De Oogst (Stijn Streuvels, 1901) (2097 words)
A small fragment from De Oogst (316 words)

Experiment 1:
Rewrite code to minimize the use of regex, O/I files and global variables. Measure the difference in running time and accuracy in CER and WER on both Mulisch and Streuvels. These results are compared with the epub as ground truth. 

Results 1:
| Mulisch  | CER | WER  | Execution time | 
| ------------- | ------------- | ------------- | ------------- |
| Raw OCR  | 1,57 | 1,60 | 0 sec |
| Original code | 1,35 | 1,16 | 2200 sec |
| Rewritten code | 1,33 | 1,07 | 416 sec |

| Streuvels  | CER | WER  | Execution time | 
| ------------- | ------------- | ------------- | ------------- |
| Raw OCR  | 4,07 | 7,44 | 0 sec |
| Original code | 3,65 | 7,40 | 10920 sec |
| Rewritten code | 5,54 | 6,77 | 203 sec |

Both scripts are increased in speed and unexpectedly increased in accuracy. This might be caused by adding Dutch surnames and given names to the lexicon and the adjustment of a few typos in the code. 


