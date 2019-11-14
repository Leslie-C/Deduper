import re
import argparse

# use samtools sort to sort the sam file by position.

# function get_UMI(first_col):
    #extract UMI using regex
    #return UMI

def get_UMI(QNAME):
    return(QNAME.split(':')[-1])

# function isReverse(second_col):
    # parse bitflag using bitwise operations (&)
    # if 16 bit is set:
        # return True
    # else
        # return False

def isReverse(FLAG):
    if FLAG & 16:
        return True
    return False

# function isMapped(second_col)
    # parse bitflag using bitwise operations (&)
    # if 4 bit is set:
        # return False
    # else
        # return True

def isMapped(FLAG):
    if FLAG & 4:
        return False
    return True

def main_code(filename):

    dupe_counter = 0
    with open('STL96.txt', 'r') as f:
        valid_UMIs = f.read().splitlines()

    prev_chr = None

    with open(filename) as f:

        output_file_name = filename.split('.sam')[0] + '_deduped.sam'

        for line in f:

            if line.startswith('@'):
                with open(output_file_name,'a') as fo:
                    fo.write(line)
                continue

            cols = line.split('\t')

            if (prev_chr != cols[2]):
                if prev_chr is None:
                    output_dict = {}
                else:
                    print('Writing chromosome ' + str(prev_chr) + ' to the output file.')
                    with open(output_file_name, 'a') as fo:
                        for key in output_dict:
                            fo.write(output_dict[key])
                    output_dict = {}


            UMI = get_UMI(cols[0])

            if UMI not in valid_UMIs:
                continue

            bit_flag = int(cols[1])
            CIGAR_split = re.findall(r'\d+[MIDNSHP=X]', cols[5])
            if isMapped(bit_flag):
                sam_pos = int(cols[3])
                offset = 0
                if isReverse(bit_flag) == False:
                    if 'S' in CIGAR_split[0]:
                        offset = int(CIGAR_split[0][:-1])
                        actual_pos = sam_pos - offset
                    else:
                        actual_pos = sam_pos

                else:
                    for index,id in enumerate(CIGAR_split):
                        if ('S' in id) & (index != 0):
                            offset -=  int(id[:-1])
                        elif 'D' in id:
                            offset +=  int(id[:-1])
                    actual_pos = sam_pos + offset

            if (UMI, actual_pos) not in output_dict:
                output_dict[(UMI, actual_pos)] = line
            else:
                dupe_counter += 1


            prev_chr = cols[2]


    with open(output_file_name, 'a') as fo:
        print('Writing chromosome ' + str(prev_chr) + ' to the output file.')
        for key in output_dict:
            fo.write(output_dict[key])
    print('Successfully deleted ' + str(dupe_counter) + ' PCR duplicates.')

if __name__ == "__main__":
    # add arguments for argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input", help="Enter the path of the sorted SAM file.")

    args = parser.parse_args()
    main_code(args.input)
