# Improved Version with Academic Tone and Spelling Check

## Enhancing the OCR Refinement Algorithm for Dutch Books: A Critical Examination
### Roel Smeets, Radboud University
### By Celis Tittse (2023)

## Abstract
This paper scrutinizes the efficacy of the OCR refinement algorithm designed for enhancing Dutch literary texts, as developed by Radboud University scholars. The algorithm is implemented for the post-OCR correction of Dutch literature books, albeit with a notable drawback of sluggish processing speed. The algorithm leverages the Levenshtein distance and a language-based AI model. Surprisingly, the removal of both models yields comparable outcomes while significantly expediting the execution process. Moreover, program optimization measures, including the elimination of redundant input/output (I/O) files, global variables, the incorporation of compounds, and the utilization of regular expressions (regex), contribute to a substantial reduction in execution time (with a performance enhancement of approximately 1068% to 5543%). The streamlined version of the program still demonstrates its efficacy in rectifying OCR errors, particularly for earlier 20th-century literary works compared to more contemporary texts.

## Program and issue
### Program Structure
0.
- Addition of names and numerals to the lexicon.
- Opening of text book files.

0.1 Identification and removal of page numbers.

1. Rectification of words composed of separate letters (e.g., 'c h i l d' becomes 'child').

2.0 Restoration of words split by hyphenation at the end of lines (e.g., 'sep-\narate' becomes '\nseparate').

2.1 Rectification of words divided by a page number at the line's conclusion (e.g., 'sep44\narate' becomes '\nseparate').

3. Insertion of spaces between words and punctuation marks, ensuring each word is present in the lexicon (e.g., 'dog.' becomes 'dog . ').

3.1 Correction of frequently misread quotation marks (e.g., 'Hallo?/' becomes 'Hallo?').

3.2 Rectification of detached initial letters, as seen in 'l etter'.

3.3 Implementation of targeted adjustments for frequently encountered errors.

4. Conversion of the line's string into a list of words, while retaining space positions in 'spatiepos'.

5. Identification of non-lexicon words that are compounds and their subsequent addition to the lexicon.

6. Submission of non-lexicon words to language models for correction.

7. Reconversion of the list to a string format while preserving spacing.

8. Elimination of excessive spacing around punctuation marks.

### Issue
The primary issue pertains to the program's sluggish performance.

### Potential Factors
1. Overreliance on global variables.
2. Extensive utilization of I/O files.
3. Redundant utilization of regex.
4. Incorporation of Bert.
5. Manual computation of Levenshtein distance, entailing comparisons of every word against an expansive dictionary.
6. Generation and inclusion of duplicated words.

## Data
### Testing Corpus
1. Extract from "De Ontdekking van de Hemel" by Harry Mulisch, 1992 (2057 words).
2. Extract from "De Oogst" by Stijn Streuvels, 1901 (2097 words).
3. Small fragment from "De Oogst" (316 words).
4. Utilization of Dutch Dictionary from OpenTaal (https://github.com/OpenTaal/opentaal-wordlist).
5. Combination with "Family-names-in-the-Netherlands" (https://github.com/digitalheir/family-names-in-the-netherlands) and Dutch first names (https://github.com/hgrif/dutch-names/blame/master/app/static/names.json).

## Method and results
### Testing Methodology
The evaluation encompasses the calculation of Word Error Rate (WER) and Character Error Rate (CER) using the ocrevalUAtion tool (https://github.com/impactcentre/ocrevalUAtion/releases).

### Experiment 1: Code Optimization
The code is refactored to minimize the reliance on regex, I/O files, and global variables. Subsequent evaluation entails the comparison of execution times and accuracy in CER and WER for both Mulisch and Streuvels extracts against the ground truth ePub.

### Results 1
Results for Mulisch:
| Condition  | CER | WER  | Execution Time | 
| :------------- | :-------------: | :-------------: | :-------------: |
| Raw OCR  | 1.57 | 1.60 | 0 sec |
| Original Code | 1.35 | 1.16 | 2200 sec |
| Rewritten Code | 1.33 | 1.07 | 416 sec |

Results for Streuvels:
| Condition  | CER | WER  | Execution Time | 
| :------------- | :-------------: | :-------------: | :-------------: |
| Raw OCR  | 4.07 | 7.44 | 0 sec |
| Original Code | 3.65 | 7.40 | 10920 sec |
| Rewritten Code | 3.54 | 6.77 | 203 sec |

Both scripts display improved speed and unexpectedly enhanced accuracy, potentially attributed to the incorporation of Dutch surnames and given names into the lexicon, alongside minor typographical code adjustments.

### Experiment 2: Bert and Levenshtein Models
The original code employs both Levenshtein distance and pre-trained AI model Bert for correcting unrecognized Dutch words. The experiment replaces the Levenshtein calculation with the optimized Python module difflib. Comparison includes CER, WER, and execution times with Bert, difflib, both, and neither.

### Results 2
Results for Mulisch:
| Condition  | CER | WER  | Execution Time | 
| :------------- | :-------------: | :-------------: | :-------------: |
| Raw OCR  | 1.57 | 1.60 | 0 sec |
| Bert and Diff | 1.33 | 1.07 | 658 sec |
| Bert | 1.38 | 1.18 | 416 sec |
| Diff | 1.49 | 1.41 | 347 sec |
| Neither | 1.33 | 1.07 | 206 sec |

Results for Streuvels:
| Condition  | CER | WER  | Execution Time | 
| :------------- | :-------------: | :-------------: | :-------------: |
| Raw OCR  | 4.07 | 7.44 | 0 sec |
| Bert and Diff | 3.53 | 6.72 | 507 sec |
| Bert | 3.54 | 6.77 | 203 sec |
| Diff | 3.53 | 6.72 | 486 sec |
| Neither | 3.53 | 6.72 | 197 sec |

Despite an initial promise, combining Bert and Levenshtein distance appears not to enhance outcomes. Manual assessment of the proposed words from both methods indicates nonsensical suggestions in the text's context, resulting in comparable error rates with or without the algorithms, and subsequently slowing the program.

### Experiment 3: AI Models
Given Bert's suboptimal results, an alternative Dutch sentence AI language model, Byt5, was evaluated against Bert. This experiment was conducted on a small sample from "De Oogst" (

316 words). The assessment includes Bert, difflib, and Byt5 individually.

### Results 3
Results for "De Oogst" Sample:
| Model  | CER | WER  | Execution Time | 
| :------------- | :-------------: | :-------------: | :-------------: |
| Raw OCR  | 2.72 | 5.33 | 0 sec |
| Byt5 | 4.05 | 8.98 | 201 sec |
| Bert | 2.10 | 4.44 | 66.7 sec |
| Diff | 3.03 | 7.56 | 61.8 sec |
| Neither | 2.02 | 4.00 | 35.3 sec |

Byt5 showcases inferior results along with lengthier execution times. The superior performance is evident when both models are employed.

### Experiment 4: Compound Dictionary
The program iterates through words, identifying compounds based on the presence of neighboring lexicon words, potentially slowing the program due to the expanded lexicon. The removal of this feature is explored, and its effect on speed and accuracy is examined.

### Results 4
Results for Books:
| Books  | Compound Lexicon | Basic Lexicon  | Execution Time Difference| 
| :------ | :-----: | :---: | :--------- |
| Streuvels (CER; WER) | (3.54 ; 6.77) | (3.54 ; 6.77) | -270 sec (411% faster) |
| Mulisch (CER; WER) | (1.33 ; 1.07) | (1.33 ; 1.07) | -277 sec (430% faster)|

While the error rate remains consistent, the program's speed improves significantly, running four times faster.

## Conclusion
The exclusion of Bert models and Levenshtein distance exhibits parallel results while expediting the process. Furthermore, program optimization through the elimination of unnecessary I/O files, global variables, compound additions, and regex contributes to a noteworthy reduction in execution time (a performance boost of approximately 1068% to 5543%). Despite the streamlined version, the program maintains its capacity to rectify OCR errors, particularly for early 20th-century texts, and serves as a valuable tool for rectifying Dutch OCRs, particularly in instances of spacing or word separation inaccuracies.
