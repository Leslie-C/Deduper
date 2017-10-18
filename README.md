# Deduper

### Part 1
Write up a strategy for writing a Reference based PCR duplicate removal tool. That is, given a sam file of uniquely mapped reads, remove all PCR duplicates (retain only a single copy of each read). Develop a strategy that avoids loading everything into memory. You should not write any code for this portion of the assignment. Be sure to:
- Define the problem
- Write examples:
    - Include a properly formated input sam file
    - Include a properly formated expected output sam file
- Develop your algorithm using pseudocode
- Determine high level functions
    - Description
    - Function headers
    - Test examples (for individual functions)
    - Return statement
    
For this portion of the assignment, you should design your algorithm for single-end data, with 96 UMIs. UMI information will be in the QNAME, like so: ```NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT```. Discard any UMIs with errors.
