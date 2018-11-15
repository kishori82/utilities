import sys
from optparse import OptionParser


parser = OptionParser()
parser.add_option("--f1", dest="file1", default = None, help="first file path")
parser.add_option("--f2", dest="file2", default = None, help="second file path")


def compare_files(argv):
     global parser
     (opt, args) = parser.parse_args(argv)

     document1 = read_file(opt.file1)
     document2 = read_file(opt.file2)

     totwt1 = num_words_including_repeats(document1)
     totwt2 = num_words_including_repeats(document2)

     first_in_second=num_matches_from_one_into_other(document1, document2)
     second_in_first=num_matches_from_one_into_other(document2, document1)

     print totwt1, len(document1.keys()), first_in_second
     print totwt2, len(document2.keys()), second_in_first

def num_words_including_repeats(document):
     # total wt of words in document
     totwt = 0
     for word in document:
        totwt += document[word]
     return totwt


def num_matches_from_one_into_other(document1, document2):
     count1in2=0 
     for word in document1:
        if word in document2:
            count1in2 += min(document2[word], document1[word])   
     return count1in2


def read_file(filename):
     document = {}
     with open(filename, 'r') as fin:
         for line in fin:
            fields = [ x.strip() for x in line.strip().split(' ') if x.strip() ]
            for field in fields:
               if not field  in document:
                   document[field] = 0
               document[field] = 1
     return document
     


if __name__=="__main__":
    compare_files(sys.argv[1:])
