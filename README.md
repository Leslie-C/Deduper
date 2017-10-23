# Deduper

## Part 1
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

## Part 2
An important part of writing code is reviewing code - both your own and other's. In this portion of the assignment, you will be assigned 3 students' algorithm to review. Be sure to evaluate the following points:
- Does the proposed algorithm make sense to you? Can you follow the logic?
- Does the algorithm do everything it's supposed to do? (see part 1)
- Are proposed functions reasonable? Are they "standalone" pieces of code?

You can find your assigned reviewees on Canvas. You can find your fellow students' repositories at 
```
github.com/uo-bgmp/deduper-<user>
```
Be sure to leave comments on their repositories by creating issues or by commenting on the pull request.
