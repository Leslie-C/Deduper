Brett Youtsey-11/15/19

#####THE PROBLEM:
#We have raw RNA-seq data. In library prep, transcripts are randomly amplified. This randomness leads to certain amplicons
# being sequenced more than once on the flow cell. For downstream analysis, we need to filter only the unique amplicons.
#After mapping reads to a genome, the subsequent SAM file can be used to detect reads containing duplicate sequences.
#These duplicate sequences are defined as reads that map to the same region and contain the same UMI.
#The task of this program is to detect these duplicates in a SAM file and output a SAM file with only unique alignments.

#####FUNCTIONS
isClipped(cigarString):
    '''Returns true if a cigarString contains soft clipping. Else False'''
        if("S" in cigarString):
            return True
        else: return False

leftClip(cigarString):
    '''Returns number of bases clipped from leftmost pos'''
    if(second char in cigarString == "S"):
        return first char in cigarString
    else: return 0

with open UMI's file & save as `UMIList`

with open `outputSAM` "a"
#####STEP 1: ORDER SAM FILE
use samtools -sort to order alignments based on their left-most position.

#First line all that matters is setting correct position, cigarstring, and UMI's as the `last` variables
`firstLine` = True
#####STEP 2: PROCESS EACH UNIQUE ALIGNMENT
iterate through each line in SAM as `readLine`:
        #will determine whether or not read is saved to output SAM
        #start with assumption that read is unqiue
        unique = True

        #PROBLEM: Based on strandedness, the cigar string will be either forward or reverse.
            `reverse` = False
            #determines from flag if read is reverse
            if col 2 & 16 == 16:
                `reverse` = True

        #PROBLEM: Soft clipping can change the leftmost position. Need to account for soft clipping in every read
            `cigarString` = col 6 in `readLine`
            if(`reverse`):
                `cigarString` = reverse(`cigarString`)

            `leftPos` = col 4 in `readLine` - leftClip(`cigarString`)
            `UMI` = regex col 1 8th section in ":" delimiter

            #PROBLEM: some UMI's will not be in `UMIList`
            #This means we cannot determine if they are duplicates, so we will error on the safe side and count them as duplicates
            if(`UMI` not in `UMIList`):
                unique = False

    if(firstLine):
            #these variables will be saved as references for the next read
            `lastPos` = `leftPos`
            `lastCigarString` = `cigarString`
            `lastUMI` = `UMI`
            `firstLine` = False

    #####THE REAL MEAT
    else: # read that isn't the first will now be compared with the `last` variables above.

            #Since the input SAM is sorted. The leftmost position for the previous reads can only be equal to or less than the currrent.
            #This means we only have to look at the past read to determine if there is a duplicate
            #EXAMPLE:
            #LEFTPOS    UNIQUE?
            #  1           T
            #  2           F
            #  2           F
            #  2           F
            #  3           T
            #  3           F

            if (`leftMost` == `lastPos` & `UMI` == `lastUMI`):
                unique = False

            if(`UMI` not in `UMIList`):
                unique = False

            #these variables will be saved as references for the next read
            `lastPos` = `leftPos`
            `lastCigarString` = `cigarString`
            `lastUMI` = `UMI`

#####SAVE UNIQUE READS TO FILE
if(unique):
    append `readline` to `outputSAM`
