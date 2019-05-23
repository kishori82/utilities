import sys, re
import argparse


sizeStep= re.compile(r'^==:(\d+)')
pattStep= re.compile(r'^\d+[.]\s([a-zA-Z]+)')
memSize = re.compile(r'Maximum resident set size \(kbytes\):\s+(\d+)')

cputime = re.compile(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):') 
hourpatt = re.compile(r'(\d+)[:](\d+)[:](\d+)') 
minpatt = re.compile(r'(\d+)[:](\d+)') 


def main():
    parser = argparse.ArgumentParser(description="Formats nohup stats to tabular form")
    parser.add_argument("--memory", dest="memory", action='store_true', default=False)
    parser.add_argument("--cpu", dest="cpu", action='store_true', default=False)
    parser.add_argument("--in", dest="input",  default=None)
    args = parser.parse_args()

    samplesizes =[]
    stats = {}
    samplesize= None
    stepname= None
    with open(args.input, 'r') as fin:
      for line in fin:
        sizeres=sizeStep.search(line)
        if sizeres:    
          #print(sizeres.group(1))
          samplesize = sizeres.group(1)
          samplesizes.append(samplesize)
    
        stepnameres=pattStep.search(line)
        if stepnameres:    
          #print(stepnameres.group(1))
          stepname = stepnameres.group(1)
          if not samplesize in stats:
             stats[samplesize] = {}
          if not stepname in stats[samplesize]:
             stats[samplesize][stepname] = []

        if args.memory:
           memsizeres=memSize.search(line)
           if memsizeres:    
              #print('RAM', memsizeres.group(1))
              ram = int(memsizeres.group(1))
              stats[samplesize][stepname].append(ram)

        if args.cpu:
           cputimeres=cputime.search(line)
           if cputimeres:
              #print(samplesize, stepname,  'CPU', line)
              hourpattres=hourpatt.search(line)
              if hourpattres:
                 #print('HR', hourpattres.group(1), hourpattres.group(2), hourpattres.group(3))
                 secs = ((int(hourpattres.group(1))*60 + int(hourpattres.group(2)))*60) + int(hourpattres.group(3))
                 stats[samplesize][stepname].append(secs)
              else:
                minpattres=minpatt.search(line)
                if minpattres:
                  #print('MIN', minpattres.group(1), minpattres.group(2))
                  secs = int(minpattres.group(1))*60 + int(minpattres.group(2))
                  stats[samplesize][stepname].append(secs)

      
    #print( stats)
    sys.stdout.write( '\t' + '\t'.join(steps) + '\n')
    for samplesize in samplesizes:
        n = len(stats[samplesize]['StarAlignedBamSingleEnd'])
        if len(stats[samplesize])==16:
          sys.stdout.write(samplesize)
          for step in steps:
             #sys.stdout.write('\t{}'.format( sum(stats[samplesize][step])/n ))
             sys.stdout.write('\t{}'.format( max(stats[samplesize][step]) ))
          sys.stdout.write('\n')
        

steps= ["FastqtoBam", "AttachBarcodes", "MergeSortBamFiles", "SplitBamByCellBarcode", 
        "StarAlignedBamSingleEnd", "TagGenes", "SortAndCorrectUmiMarkDuplicates", "GeneSortBam", 
        "CellSortBam", "CalculateGeneMetrics", "CalculateCellMetrics", "CreateSparseCountMatrix", 
        "MergeSortedBamFiles", "MergeGeneMetrics", "MergeCellMetrics", "MergeCountFiles"
       ]

if __name__=="__main__":
   main()

