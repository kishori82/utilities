import pysam, gzip, bz2, sys
import re, argparse



def read_reference(refgenome):
    chromosome_seq = {}
    with pysam.FastxFile(refgenome) as fh:
       for entry in fh:
             chromosome_seq[entry.name] = entry.sequence
    return chromosome_seq 
    
def open_by_suffix(filename, mode):
    if filename.endswith('.gz'):
        return gzip.open(filename, mode)
    elif filename.endswith('.bz2'):
        return bz2.BZ2file(filename, mode)
    else:
        return open(filename, 'r')


def read_variants(vcf_file):
    variants = []
    with open_by_suffix(vcf_file, 'rt') as fp:
      for _line in fp:      
         line = str(_line)
         if re.search(r'^#', line):
            continue
         fields = [ x.strip() for x in line.strip().split('\t') ]
         chrom = fields[0]
         position = int(fields[1])
         refseq = fields[3]
         leng = len(fields[3])
         alt =fields[4]
         start = position - 1
         end = start + leng
         variants.append( [chrom, start, end, leng, refseq, alt ])
         #print( chrom, start, end, leng, refseq, chromosome_seq[chrom][start:end])
    return variants

#   print(entry.sequence[start:end])
     
      #print(entry.sequence)
      #print(entry.comment)
      #print(entry.quality)

def main():
    parser= argparse.ArgumentParser()
    parser.add_argument("--refgenome", dest="refgenome", default=None)
    parser.add_argument("--vcf", dest="vcf_file", default=None)
    parser.add_argument("--bam-in", dest="bam_file_in", default=None)
    parser.add_argument("--bam-out", dest="bam_file_out", default=None)
    args = parser.parse_args()


    variants = read_variants(args.vcf_file)
    chromosome_seq=read_reference(args.refgenome)

    insamfile = pysam.AlignmentFile(args.bam_file_in, "r", check_sq=False, check_header=False)
    outsamfile = pysam.AlignmentFile(args.bam_file_out, "wb", template=insamfile)
    v = 0
    o = 75
    for read in insamfile:
       #print(read.query_name, read.query_alignment_sequence, read.query_alignment_length, len(read.query_alignment_sequence), read.is_read1, read.is_read2)
       if read.is_read1:
          chrom= variants[v%10][0]
          p= variants[v%10][1]
   
          l1 = len(variants[v%10][4])
          l2 = len(variants[v%10][5])
   
          part1 = chromosome_seq[chrom][p-o: p]
          part2 = variants[v%10][5]
          part3 = chromosome_seq[chrom][p + l1 :  p -o + 250 + l1 - l2]
          #print(variants[v%10])
          read_seq = part1 + part2 + part3

          #print('+', chromosome_seq[chrom][p - o :  p], chromosome_seq[chrom][p: p + l1],  chromosome_seq[chrom][p + l1: p -o + 250])
       else:
          p= variants[v%10][1]
          chrom= variants[v%10][0]
          letters = list(chromosome_seq[chrom][p - o  + 250:  p - o + 500])
          letters.reverse()
          for i in range(len(letters)):
             if letters[i]=='A':
                letters[i]=='T'
             elif letters[i]=='T':
                 letters[i]=='A'
             elif letters[i]=='C':
                letters[i]=='G'
             else:
                letters[i]=='C'
          read_seq = ''.join(letters)
          v = v + 1
       query_qualities = read.query_qualities
  


       read.query_sequence = read_seq
       read.query_qualities = query_qualities

       outsamfile.write(read)

    insamfile.close()
    outsamfile.close()



    #for variant in variants: 
    #  print(variant, chromosome_seq[variant[0]][variant[1]:variant[2]])



#   print(entry.sequence[start:end])
     
      #print(entry.sequence)
      #print(entry.comment)
      #print(entry.quality)
if __name__=="__main__":
   main()
