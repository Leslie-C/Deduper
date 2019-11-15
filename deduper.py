import re
import argparse

def get_UMI(QNAME):
    return(QNAME.split(':')[-1])

def isReverse(FLAG):
    if FLAG & 16:
        return True
    return False

def isMapped(FLAG):
    if FLAG & 4:

        return False
    return True

#@profile
def main_code(filename):

    dupe_counter = 0

    prev_chr = None

    output_dict = set()

    with open('STL96.txt', 'r') as f:
        valid_UMIs = f.read().splitlines()

    output_file_name = filename.split('.sam')[0] + '_deduped.sam'

    with open(filename, 'r') as f, open(output_file_name,'a') as fo:

        for line in f:
            if line.startswith('@'):
                fo.write(line)
                continue

            cols = line.split('\t')

            UMI = get_UMI(cols[0])

            if UMI in valid_UMIs:

                bit_flag = int(cols[1])
                isReverseStrand = isReverse(bit_flag)


                if isMapped(bit_flag):
                    offset = 0
                    CIGAR_split = re.findall(r'\d+[MIDNSHP=X]', cols[5])
                    sam_pos = int(cols[3])

                    if isReverseStrand == False:
                        if 'S' in CIGAR_split[0]:
                            offset -= int(CIGAR_split[0][:-1])
                    else:
                        for index,id in enumerate(CIGAR_split):
                            if ('S' in id) & (index == 0):
                                offset -=  int(id[:-1])
                            elif ('S' in id) & (index != 0):
                                offset += int(id[:-1])
                            elif ('D' in id) or ('N' in id) or ('M' in id):
                                offset +=  int(id[:-1])
                    actual_pos = sam_pos + offset
                if (UMI, actual_pos, isReverseStrand) in output_dict:
                    dupe_counter += 1
                else:
                    output_dict.add((UMI, actual_pos, isReverseStrand))
                    fo.write(line)

    print('Successfully deleted ' + str(dupe_counter) + ' PCR duplicates.')

if __name__ == "__main__":
    # add arguments for argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input", help="Enter the path of the sorted SAM file.")

    args = parser.parse_args()
    code_to_test = main_code(args.input)
