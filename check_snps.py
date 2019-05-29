import pysam,sys
import re


refgenome = sys.argv[1]

var_list = sys.argv[2]

#chrn= sys.argv[2]
#position= int(sys.argv[3])
#leng= int(sys.argv[4])

#start = position - 1


chromosome_seq = {}
with pysam.FastxFile(refgenome) as fh:
   for entry in fh:
         chromosome_seq[entry.name] = entry.sequence


with open(var_list, 'r') as fp:
  for line in fp:      
     if re.search(r'^#', line):
        continue
     fields = [ x.strip() for x in line.strip().split('\t') ]
     #print(fields)
     chrom = fields[0]
     position = int(fields[1])
     refseq = fields[3]
     leng = len(fields[3])
     start = position - 1
     end = start + leng
     print( chrom, start, end, leng, refseq, chromosome_seq[chrom][start:end])


#   print(entry.sequence[start:end])
     
      #print(entry.sequence)
      #print(entry.comment)
      #print(entry.quality)
