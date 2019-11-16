######
#Sequencing (mostly) require the usage of PCR amplification in order to get a signal on the sequencer. However, not all sequences are equally amplified. In RNA-seq experiments, we like to look at differential expression of transcripts between genes. If sequences are not equally amplified, then the expression levels seen in the data will not represent the actual expression levels. Because of this, it is important to get rid of PCR duplicates in order to get a true representation of the expression levels.
######




#import re (regex)

# use samtools sort to sort the sam file by position (unless presorted)

#function get_UMI(first_col):

    ```
    #Parameters: first_col
    #This function will extract the UMI from the first column of the record

    #Returns: UMI (string)
    ```

    #extract UMI using regex
    #return UMI

# function isReverse(second_col):
    ```
    #Parameters: second_col
    #This function will figure out which strand the read is aligned to.

    #Returns: True/False (Boolean)
    ```

    # parse bitflag using bitwise operations (&)
    # if 16th bit is set:
        # return True
    # else
        # return False

# function isMapped(second_col)
    ```
    #Parameters: second_col
    #This function will return whether the read is mapped or not.

    #Returns: True/False (Boolean)
    ```

    # parse bitflag using bitwise operations (&)
    # if 4th bit is set:
        # return False
    # else
        # return True

# function main_code(SAM_file):
    ```
    #Parameters: SAM_file
    #This function will contain the code that does all of the processing.

    #Returns: None
    ```

    # open UMI file for reading
        # store UMIs in list

    # instantiate a variable that stores the previous chromosome
    # in the beginning, this variable will be stored as a NoneType (None)
    # this is important for not running into memory issues
    # chromosome is the only thing we can rely on to flush out records from memory bc we don't know softclip limit

    # open SAM file
        # for each line
            #if the line starts with @
                # write this line to output file
                # this is a header line
                # ignore (continue)

            # store record information by splitting the line by tab ('\t')

            # if the current chromosome (second column) is not equal to the previous chromosome
                # if the previous chromosome is None
                    # just create empty dict, nothing is in there initially so no need to write anything yet
                    # will store (UMI, position) as key and the whole record as the value
                # else
                    # create a new file using open and set to append mode
                        # for each key in the dict
                            # write to output file
                        # flush the dict by setting it as empty

            # store UMI by extracting first column, using split function w/ ':' delimeter, then get last element

            # if this UMI is not in our valid UMI list, then move onto next line (continue)

            # store bit flag in variable (second column)

            # make list which contains information about CIGAR string using regex's findall function
            # if CIGAR string is '3S30M40N34M', want list that looks like: ['3S','30M','40N','34M']

            # if isMapped is True:
                # store the leftmost position given in SAM file in "sam_pos"
                # instantiate a variable called "offset" to 0
                # if isReverse is False
                    # only care about softclipping if on the leftside of CIGAR string
                    # if 'S' in the first element of CIGAR string
                        # extract the number from the first element by using string splicing [:-1], convert to int
                        # store this number in 'offset'
                        # create variable called actual_pos = sam_pos - offset
                    # else
                        # set actual_pos to the sam_pos (actual_pos = sam_pos)
                # else
                    # reverse is a little more tricky
                    # loop over the CIGAR string list (use enumerate to store index as well)
                        # only care about softclipping if right hand side of CIGAR string
                        # if 'S' is in the current element and its not the first index (softclip can't be in middle, dont need to explicitly check last position)
                            # offset = offset - softclip_val
                        # elif 'D' in current element:
                            # need to add deletions to the position
                            # deletions can appear multiple times in CIGAR string, need to check entire list
                            # offset = offset + deletion_val

                    # actual_pos = sam_pos + offset

                # if (UMI, actual_pos) is not a key in our dict
                    # add the key to the dict, with the value as the entire record

                # now that we are effectively done processing, set previous_chromosome = current_chromosome

    # the buffer/flush/write logic using the chromosome will not write the final chromosome out to the file because there's no "new" chromosome to look at (since its the last line)
    # therefore outside the file for loop, just write what is left in the dictionary (which contains all of the last chromosome's deduped records)

# if __name__ == "__main__":
    # add argparse arguments
