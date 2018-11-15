#!/usr/bin/python
import os, sys

def string(x, icon):
   a = "<span><i class=\"" + icon + "\"></i> " + x + "</span>"
   return a

def depth(line):
   depth = 0
   for x in line: 
      if x=='\t' :
        depth += 1
      else:
        break
   return depth


def getname(line):
   fields = [ x for x in line.strip().split('\t')  ]
   return fields[0]

def getsize(line):
   fields = [ x for x in line.strip().split('\t')  ]

   size = ""
   if len(fields) < 2:
     return size
    
   _size = fields[1]

   if int(_size) > 1024:
     size =  "%.2f KB" % (int(_size)/1024)
   if int(_size) > 1024*1024:
     size =  "%.2f MB" % (int(_size)/(1024*1024))
   else:
     size =  _size + " Bytes"

   print size
   return size


def tree_string(filename):
   string_print = ''
   with open(filename, 'r') as fp:
       lines = fp.readlines()
   
       SPACE="   "
       pd=-1
       first = True
       for line in lines:
          name = getname(line)
          size = getsize(line)
          d=depth(line)
   
   
   
          if pd < d:
             string_print = string_print +  SPACE*d + "<ul>"  + "\n" + SPACE*(d) + "<li>"  + "\n" + SPACE*(d+ 2) + string(name, "icon-leaf") + size + "\n"

#             print SPACE*d + "<ul>"
#             print SPACE*(d) + "<li>"
#             print SPACE*(d+ 2) + string(name, "icon-leaf")
   
   
          if pd == d:
             string_print = string_print + SPACE*(d+1) + "</li>" + "\n" + SPACE*(d+1) + "<li>" + "\n" + SPACE*(d + 2) + string(name, "icon-leaf") + size +  "\n"

             #print SPACE*(d+1) + "</li>"
             #print SPACE*(d+1) + "<li>"
             #print SPACE*(d + 2) + string(name, "icon-leaf")
   
          if pd > d:
             for i in reversed(range(0, pd -d )):
                string_print = string_print + SPACE*(d + i + 1) + "</li>" + "\n" + SPACE*(d + i) + "</ul>"  + "\n" +  SPACE*(d+1) + "<li>"  + "\n" + SPACE*(d + 2) + string(name, "icon-leaf") + size + "\n"

                #print '   '*(d + i + 1) + "</li>"
                #print '   '*(d + i) + "</ul>"
                #print SPACE*(d+1) + "<li>"
                #print SPACE*(d + 2) + string(name, "icon-leaf")
   
          pd = d
          
   
       while pd > 0 :
         string_print = string_print +  '   '*(pd + 1) + "</li>" + "\n" +  '   '*(pd) + "</ul>" + "\n"

#         print '   '*(pd + 1) + "</li>"
#         print '   '*(pd) + "</ul>"
         pd -= 1

       return string_print

print tree_string('file.txt')
 
