# DSP OCR Improvement Algorithm reviewed
OCR Dutch Books Roel Smeets

Evaluation of the OCR refinement for Dutch books created by Radboud University studies. (https://github.com/FlorisCos/DSP_OCR_improvement_algorithm/tree/main)

**Abstract** 
The OCR improvement algorithm post-OCR corrector improves Dutch literature books but runs very slowly. It utilises the Levenshtein distance and language AI model. Unexpectedly, removing both models yield the same results and slows down the process. In addition, optimising the program by removing unnecessary O/I files, global variables, the addition of compounds, and regex shows a significant decrease in execution time (an increase of c. 1068% to 5543%). The reduced program still improves OCRs yielding more significant corrections for older (beginning of the 20th-century books) than  younger books. 

**Problem:**
The program is running very slowly. 

**Potential causes:**
1. Heavy use of global variables.
2. Extensive use of O/I files.
3. Unnecessary use of regex.
4. Use of Bert.
5. Use manual Levenshtein distance calculations comparing every word with an extensive dictionary.
6. The creation and addition of double words 

**Test corpora:**
1. Fragment from De Ontdekking van de Hemel (Harry Mulisch, 1992) (2057 words)
2. Fragment from De Oogst (Stijn Streuvels, 1901) (2097 words)
3. A small fragment from De Oogst (316 words)
4. The Dutch Dictionary from OpenTaal is used (https://github.com/OpenTaal/opentaal-wordlist)
5. Combined with the Family-names-in-the-Netherlands (https://github.com/digitalheir/family-names-in-the-netherlands) and first names in Dutch (https://github.com/hgrif/dutch-names/blame/master/app/static/names.json)
   
**Testing Methods**
Calculating the differences between tests based on Word (WER) and character (CER) error, the ocrevalUAtion is used. (https://github.com/impactcentre/ocrevalUAtion/releases)

**Experiment 1:**
Rewrite code to minimize the use of regex, O/I files and global variables. Measure the difference in running time and accuracy in CER and WER on both Mulisch and Streuvels. These results are compared with the epub as ground truth. 

**Results 1:**
| Mulisch  | CER | WER  | Execution time | 
| ------------- | ------------- | ------------- | ------------- |
| Raw OCR  | 1,57 | 1,60 | 0 sec |
| Original code | 1,35 | 1,16 | 2200 sec |
| Rewritten code | 1,33 | 1,07 | 416 sec |

| Streuvels  | CER | WER  | Execution time | 
| ------------- | ------------- | ------------- | ------------- |
| Raw OCR  | 4,07 | 7,44 | 0 sec |
| Original code | 3,65 | 7,40 | 10920 sec |
| Rewritten code | 3,54 | 6,77 | 203 sec |

Both scripts are increased in speed and unexpectedly increased in accuracy. This might be caused by adding Dutch surnames and given names to the lexicon and the adjustment of a few typos in the code. 

**Experiment 2**
The original code uses Levenshtein distance and pre-trained AI model Bert to correct words which are not recognised as Dutch words or names. Both models propose a word which is respectively a word closest to the unrecognised word and a word that is plausible in the context. If both words are the same, it is changed in the text. 
The Levenshtein distance is calculated within the code, which increases the running speed. Replacing it with an optimized Python module difflib. The inbuild function get_close_matches gives the same results but faster (https://docs.python.org/3/library/difflib.html). 
This experiment entails the comparison of CER, WER and execution time with Bert and difflib, with difflib, with Bert and without both of them. 

| Mulisch  | CER | WER  | Execution time | 
| ------------- | ------------- | ------------- | ------------- |
| Raw OCR  | 1,57 | 1,60 | 0 sec |
| Bert and Diff | 1,33 | 1,07 | 658 sec |
| Bert | 1,38 | 1,18 | 416 sec |
| Diff | 1,49 | 1,41 | 347 sec |
| Neither | 1,33 | 1,07 | 206 sec |

| Streuvels  | CER | WER  | Execution time | 
| ------------- | ------------- | ------------- | ------------- |
| Raw OCR  | 4,07 | 7,44 | 0 sec |
| Bert and Diff | 3,53 | 6,72 | 507 sec |
| Bert | 3,54 | 6,77 | 203 sec |
| Diff | 3,53 | 6,72 | 486 sec |
| Neither | 3,53 | 6,72 | 197 sec |

In conclusion, it shows that combining Bert and Levenshtein seems like a good and reasonable idea. But the results stay the same. In the initial report from the research group the combination of the two yields the best results in comparison with applying one of the two methods. Looking at the words both methods return in the text manually, the proposed words make no sense in either the context of the sentence. In lists of ten proposed words, Bert and diff almost never return the same suggestions and no correction is processed. Resulting in the same error rate for applying the algorithms and leaving them out. It only slows down the program. 
