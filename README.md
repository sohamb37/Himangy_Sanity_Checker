# Himangy_Sanity_Checker
Automatic sanity checker for the Himangy Corpora Public Release post creation of the corpora.

# The Languages considered for this sanity checking:
Dogri - doi*
Gujarati - gu
Hindi - hi
Kannada - kn
Kashmiri - ks*
Odia - or
Punjabi - pa
Sindhi - sd
Telugu - te
Urdu - ur

# Errors that the sanity checker looks for:
1. New line (\n) inserted in the text.
2. Only a single punctuation mark or symbol in a sentence.
3. Missing sentence.
4. Only URL in the source sentence.
5. Probable sentences of other languages present in between.
6. Untranslated sentences.
7. Probable wrong alignment. For example, Eng-to-Tel alignment in a Tel-to-Eng file.

Note: Detection of different language sentences and detection of wrong alignment are not supported for [doi, ks]. For the other language pairs, it detects the probable existence of these errors.

# To use the sanity checker, the file to be evaluated should be in the same folder as the sanity.py file. These are the following steps to be run in the terminal:

1. To install all the dependencies: pip install -r requirements.txt

2. To run the sanity checker: python sanity.py <filename> <src_lang_code> <target_lang_code>
   For example: We have added a test file called guj_hindi.txt, which is Gujarati to Hindi translated data with respective language codes as gu and hi. The corresponding command will be: python sanity.py guj_hindi.txt gu hi.

3. Note: The expected file format is tab separation between the source and the target language pairs respectively.
   Example: ૭૩માં પ્રજાસત્તાક પર્વનો રાજ્ય કક્ષાનો ધ્વજ વંદન સમારોહ ગીર સોમનાથ જિલ્લામાં	गिर सोमनाथ जिले में गणतंत्र दिवस पर राज्य स्तरीय ध्वजारोहण समारोह. Convert the file to this format to run the sanity checking.  

4. This script may not be compatible with Windows operating systems. 

# Results generated:
The script should print out a list of errors with the total number of errors and generate a file with filename + errors.tsv extension with line-by-line errors!



For any doubts and clarifications, contact:
Soham Bhattacharjee - sohambhattacharjeenghss@gmail.com
Baban Gain - gainbaban@gmail.com
