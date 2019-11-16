"""The Problem"""
"""
During PCR amplification there are potential biases against GC rich regions of DNA as the breaking and annealing of these bonds
require a much higher amount of energy. This means that during PCR amplification you will generate a non inconsequential number
of reads that are exact duplicates of other sequences when you align your reads to a database. These reads will effectively start
at the same position and be the exact same sequence.
However it is entirely possible that sequences that are natrually highly expressed will appear in the same fashion.
This leaves us at an impass of wanting to remove spurious copies of alignment reads which causes noise in our alignment data while simultaneously maintaining the signal of highly expressed regions.
In addition accounting for indels and exon length are factors that need to be accounted for when determining starting position
of each mapping read. This is important to determining true PCR duplicates.
"""

"""Assumptions about the data"""
"""
The data has been sorted using samtools, sample commands below
    $samtools view -S -b aligned.out.sam > aligned.bam
    $samtools sort aligned.bam -o aligned.sorted.bam
    $samtools index aligned.sorted.bam
    $samtools view -h -o aligned.sorted.sam aligned.sorted.bam
This data is a sorted single end sam file which can be more easily parsed as the reads will be indexed by chr/scaffold
"""


"""PCR duplication case notes"""
"""
key factors that need to account for : the adjusted 5' postion, the sequence, and the cigar string, the bitwise flag, and the QNAME for soft clipping

First
    open up the list of umis and store them in an array
    open both sam files and store a group of reads by chromosome or scaffold to prevent too many reads from being stored at any one time.
    open up 3 outfiles one file for UMI mismatches, one for PCR duplicates, and one for the rest of the good reads

Second
    check the reads UMI's to see if they match the reference, if they don't write them to a bad out file
    iterate through the stored reads checking the 5' most position accounting for soft clipping by subtracting the given value by S if the cigar string indicates there was left-most softclipping.

Third
    what is the alignment of the new read (+/-)?
    Any reads that have D in the cigar string AND are (-) must have their starting position adjusted similar to accounting for right-soft clipping
    Deletions and insertion do not make an impact on (+) sequence positions

Fourth
    if a read at the leftmost position has not been recorded, write it to an outfile then move on to the next stored read.

Fifth
    if the next/subsequent read has the same left-most position then check to see if the UMI's attached to the reads are the same

        if yes then toss the read with the lower mean quality score since these are PCR duplicates
        if no then it's not a PCR duplicate, and it can be written to the outfile

    if the next sequence starts at a different position than the last observed write it to the outfile and move on to the next read

Sample input file : "input_test.sam"
Sample output file : "test_passed.sam" = pcr duplicate removed file, "bad_umi_test.sam" = umi was not in our list, "dup_test.sam" = file containing the PCR duplicates

"""


"""functions"""
import re

group = "reads grouped by chromosome/scaffold"

def umi_ref(ref):
    """given the input file from the argparse this takes the umis within it and creates a reference array as a key for deduplicating"""
    """importantly the input file must have am umi on each line"""

    with open(ref,'r') as u_ref :
        umi_list = []
        for line in u_ref:
            y = line.strip()
            umi_list.append(y)
        return umi_list
u_ref = umi_ref(ref)

def info(group):
    """given the input of an individual header in the sam file this parses out the relavent info to sort the file by, read is an individual read being inputted into the function
    this returns the values that need to be compared to test for PCR duplication"""
for read in group:
    qname=read.split('\t')[0]
    umi=qname.split(':')[-1] # the umi is the last thing in the qname
    flag=int(read.split('\t')[1])
    rname=read.split('\t')[2]
    pos=int(read.split('\t')[3])
    qual=read.split('\t')[10]
    cig=read.split('\t')[5]
    return qname, flag, rname, pos, qual, cig
#useful flags to be used for the actual parsing

def Umi_error(umi):
    """This takes the umis from the reads and if they do not match an umi in the reference list it writes the read to an out folder"""
if umi not in u_ref:
    bad_umi.write(read)
    read.clear()

def positions(pos,cig,flag):
    """taking in the initial position given from the headerline and the cigar string this function adjusts the position of reads being compared for either right or left soft clipping
    this returns the 'real position' of the 5' most position of the read"""

#start with initial blank values for left or right clipping
lclip = 0
rclip = 0
cig_fw = re.findall(r'(\d+)([M,N,S]{1})', cig)
cig_rv = re.findall(r'(\d+)([M,N,S,D]{1})', cig)

fw_lengths = [int(item[0]) for item in cig_fw]
fw_len = sum(fw_lengths)

rv_lengths = [int(item[0]) for item in cig_rv]
rv_len = sum(rv_lengths)

for cha in cig_rv:
    if cha[-1] == 'S':
        rclip = int(cig_rv[-1][0])
    if cig_rv[0][1] == 'S':
        lclip =  int(cig_rv[0][0])

for read in group:
    #for each read in the group files
    if ((flag & 16) = 16):
        rev_comp = True
        #set a flag to see which strand the read is on
        if rev_comp is False:#if this read is on the (+) strand
            real_start = pos - lclip # adjusting for left clipping
            end = pos + fw_len - 1 # finding the end position given length
            real_end = end + rclip # adjusting for right clipping
        else: # if this read is on the (-) strand
            real_end = pos - lclip # adjusting for left clipping
            start = pos + rv_len - 1 # finding the end position given length
            real_start = start + rclip # adjusting for right clipping

    return (real_start, real_end)#left most and right most positions accounting for strandedness and clipping.



"OUTMODED function being stored for potential future use?!?!"
for cha in cig:
    if cha in 'MIDNSHP=cha':
        #read through the different values in the cigar string
        if cha == 'S':
            #if there has been soft clipping detected
            if lclip is None and cha[-1] !='S':
                #if this is the first instance of soft clipping being detected and is left most positioned store the value
                lclip =  cig.rpartition('S')[0]

            elif lclip is None and cha[-1] =='S':
                #if this is the first instance of soft clipping being detected and is left most positioned store the value
                rclip =  cig.rpartition('S')[0]

            else:
                #if this is the second instance of soft clipping being detected
                rclip = cig.rpartition('S')[1]
    #need to add all M, N, D numbers for (-) position lengths
