# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 19:18:16 2019

@author: the5t
"""

"""
Function tests were conducted below and the resulting return values were stored and saved in the "function_test_out.spydata" file

"""
import re

cig = '5S23M1290N25M2D18M2S'

cig_fw = re.findall(r'(\d+)([M,N,S]{1})', cig)

cig_fw

fw_lengths = [int(item[0]) for item in cig_fw]
fw_len = sum(fw_lengths)



sam = 'K00337:113:HN7KGBBXX:4:2105:11860:30767-ACGAAGGT^AGTGCTGT	99	1	26	255	92M	=	226	292	AAACATTTTCAATCATTACATTGTCATTTTCCCTCCAAATTAAATTTAGCCAGAGGCGCACAACATACGACCTCTAAAAAAGGTGCTGTAAC	FJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJ	NH:i:1	HI:i:1	AS:i:178	nM:i:2'

qname=sam.split('\t')[0]

qname

umi=qname.split(':')[-1]

umi

read =sam

qname=read.split('\t')[0]
umi=qname.split(':')[-1] # the umi is the last thing in the qname
flag=int(read.split('\t')[1])
rname=read.split('\t')[2]
pos=int(read.split('\t')[3])
qual=read.split('\t')[10]
cig=read.split('\t')[5]

lclip = 0
rclip = 0
cig_fw = re.findall(r'(\d+)([M,N,S]{1})', cig)
cig_rv = re.findall(r'(\d+)([M,N,S,D]{1})', cig)


for cha in cig_rv:
    if cha[-1] == 'S':
        rclip = int(cig_rv[-1][0])
    if cig_rv[0][1] == 'S':
        lclip =  int(cig_rv[0][0])
    
    


rev_comp = True
real_start = pos - lclip # adjusting for left clipping
end = pos + fw_len - 1 # finding the end position given length
real_end = end + rclip # adjusting for right clipping

