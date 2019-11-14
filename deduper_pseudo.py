"""
The Poblem:
When amplifying RNA-seq libraries many duplicates RNA molecules are produced.
These duplicates must be removed so that an accurate count of all RNA transcripts can be made.

Strategy:
1. Read in a sam file that is sorted by chromosome and left most position (use samtools sort to sort).
2. Make a reference dictionary for the forward mapping reads and for reverse mapping reads which has the
"chromosome" and "five prime position" that the read mapped to as the key and a list of the "UMIs" associated
with that chromosome and five prime position as the value.
3. In order to get the five prime position that the read mapped to the cigar string must be parsed.
Cigar strings are parsed differently depending on the direction of the strand that the read mapped to,
therefore the bitwise flag must be parsed. Functions for these parsings must be defined.
4. (Referencing the ditionaries) do not write out reads that have the same UMIs and mapped to the same
chromosome, strand and five prime position.
4a. Also do not write out reads if they have UMIs that are not in the given list of UMIs

Notes:
1. All sequences are the same length
2. Flush the dictionaries after each chromosome is handled
"""

"""
Main Code:
import regex
import my functions

open input sam file for reading
open an output sam file for writing
read in a list of umis

make a global dictionary for referencing forward mapped reads
make a global dictionary for referencing reverse mapped reads
set a variable (which is meant to keep track of the chromosomes) to 1. (This variable needs to exist for dictionary flushing logic)
for line in input sam file:
    if the first character of the line has an @:
        1. output_file.write(line)
    else the first character is a read:
        2. find the "umis", "flag", "chromosome", "left position" and "cigar string"
        3. pass "flag", "cigar string" and "left position" into the function that parses the cigar string (shown below)
        4. make a "tuple" that contains the "chromosome" and "five prime mapped position"
        5. if "umis" are not valid then do not write out the line
        6. if the chromosome is not the same as the global chromosome variable then set the chromosome to whatever the current
           chromosome is and flush/reset the global dictionaries)
        7. if the read mapped to the forward strand
            a. if the "tuple" is not in the global forward dictionary then save it as the key and save the umi as an item in a list
            b. else the "tuple" is in the global forward dictionary
                - if the "umi" is in the list of values associated with the tuple don't write it out
                - if the "umi" is not the list of values associated with the tuple write it out
        8. if the read mapped to the reverse strand
            a. if the "tuple" is not in the global forward dictionary then save it as the key and the "umi" as an item in a list
            b. else the "tuple" is in the global forwad dictionary
                - if the "umi" is in the list of values associated with the tuple don't write it out
                - if the "umi" is not the list of values associated with the tuple write it out
"""
"""
Functions:
def function to parse flags
  "parses the bitwise flag"
    a. checks whether a read was mapped (will not write out) (e.g. 100 not mapped)
    b. returns True if the read mapped to the forward strand (e.g. 30 forward)
    c. returns false if the read mapped to the reverse strand (e.g. 64 reverse)

def function to parse the cigar string
  "find the five prime position that the read mapped to and whether the read was mapped to the forward or reverse strand"
    a. if function to parse flags equals true
        - if there is softclipping at the beginning of the "cigar string" then subtract the softclipping from the "left position"
          return that as the "5' position" (e.g. 1S70M + 1148 = 1218)
        - else the "left position" is the "5' position"
          return the "left position" as the "5' position" (e.g. 1148 = 1148)
    b. if function to parse flag equals false
        - sum the number in the "cigar string"
        - if there is softclipping at the beginning of the "cigar string" subtract that number from the sum
          return this as the "5' position"(e.g. 1S70M - 1180 = 109)
        - if there is indexing anywhere in the string then subtract that indexing from the sum
          return this as the "5' position" (e.g. 1S2I68M - 1180 = 109)
        - else return the string sum + "left_position" as the "5' position" (e.g. 70M - 1180 = 110)
"""
