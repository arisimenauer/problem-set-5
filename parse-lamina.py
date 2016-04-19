#! /usr/bin/env python

import ipdb
from collections import Counter
filename ='/Users/arisimenauer/data-sets/fastq/SP1.fq'

cstart = 0
bigchrom = ''
bigend = 0
bigendchrom = ''
bigendstart = 0

for line in open('/Users/arisimenauer/data-sets/bed/lamina.bed'):
    if line.startswith('#'):continue
    parts = line.strip().split('\t')
    chrom = parts[0]
    start = int(parts[1])
    end = int(parts[2])

    if start > cstart:
        cstart = start
        bigchrom = chrom

    if chrom == 'chrY':
        if end > bigend:
            bigend = end
            bigendchrom = chrom
            bigendstart = start


def reverse_complement(seq):
    num_rec = 0
    comps =  []
    for char in seq:
        if char == 'A':
            comps.append('T')
        if char == 'T' or char == 'U':
            comps.append('A')
        if char == 'G':
            comps.append('C')
        if char == 'C':
            comps.append('G')
    rev_comp = ''.join(reversed(comps))
    return rev_comp


def sum_quals(qual):
    sum = 0
    for char in qual:
        sum += ord(char)
    return sum

MaxC = 0
SeqName = ''
line_num = 0
seqnum = 0
BigQual = 0
revlist = []
for line in open(filename):

    line_type = line_num % 4

    if line_type == 0:
        name = line.strip()
    elif line_type == 1:
        seq = line.strip()
    elif line_type == 3:
        seqnum += 1
        quals = line.strip()

        CurrentCount = Counter(seq)
        if CurrentCount['C'] > MaxC and seqnum <= 10:
            MaxC = CurrentCount['C']
            SeqName = name

        CurrentQual = sum_quals(quals)
        if CurrentQual > BigQual:
            BigQual = CurrentQual

        if seqnum <= 10:
            revlist.append(reverse_complement(seq))
    line_num += 1
print 'answer-1:', bigchrom
print 'answer-2: {}:{}-{}'.format(bigendchrom, bigendstart, bigend)
print 'answer-3:', SeqName
print 'answer-4:', BigQual
print 'answer-5:', revlist
