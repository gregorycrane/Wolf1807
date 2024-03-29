import sys
import re

# count the arguments
arguments = len(sys.argv) - 1

# output argument-wise
position = 1



lastnausea = 0
lasttischendorf = 190
lastwright = 686
def dofile (fn):
  global lastnausea
  global lasttischendorf
  global lastwright
  lnum = 0 
  innotes = 0

  f = open(fname,"r")
  for l in f:
    l = re.sub("\s+$","",l)

# skip the headers
    if( re.search("(MIRAC[UV]LIS.*THOMAE|PASSIO)",l)):
      continue

    if( re.search("<div",l)):
      print(l)
      continue

# add line numbers

    if( re.search("[a-zα-ωΑ-Ω]",l)):
      lnum = lnum + 1
      l = re.sub("(.+)","<lb n='" + str(lnum) + "'/>\g<1>",l)
# look for references to page breaks in the Thilo edition
    l = re.sub("([0-9]+)\s+(N\.)","<milestone unit='nausea' n='\g<1>'/>",l)
    l = re.sub("(N\.)\s+([0-9]+)","<milestone unit='nausea' n='\g<2>'/>",l)

# check to see if you skip any
    m = re.search("<milestone unit='nausea' n='([0-9]+)'",l)
    if( m ):
      curnausea = int(m.group(1))
      if( curnausea != lastnausea + 1):
        sys.stderr.write(fname + ' skippednausea ' + str(lastnausea) + ' '+ str(curnausea)+'\n')
      lastnausea = curnausea

# look for references to page breaks in the Tischendorf edition
    l = re.sub("([0-9]+)\s+(T\.)","<milestone unit='tischendorf' n='\g<1>'/>",l)
    l = re.sub("(T\.)\s+([0-9]+)","<milestone unit='tischendorf' n='\g<2>'/>",l)
    
# check to see if you skip any
    m = re.search("<milestone unit='tischendorf' n='([0-9]+)'",l)
    if( m ):
      curtischendorf = int(m.group(1))
      if( curtischendorf != lasttischendorf + 1):
        sys.stderr.write(fname + ' skippedtischendorf ' + str(lasttischendorf) + ' '+ str(curtischendorf)+'\n')
      lasttischendorf = curtischendorf

# look for references to page breaks in the Fabricius edition
    l = re.sub("([0-9]+)\s+([fF]\.)","<milestone unit='fabricius' n='\g<1>'/>",l)
    l = re.sub("([fF]\.)\s+([0-9]+)","<milestone unit='fabricius' n='\g<2>'/>",l)
    
# check to see if you skip any
    m = re.search("<milestone unit='fabricius' n='([0-9]+)'",l)
    if( m ):
      curwright = int(m.group(1))
      if( curwright != lastwright + 1):
        sys.stderr.write(fname + ' skippedwright ' + str(lastwright) + ' '+ str(curwright)+'\n')
      lastwright = curwright

# Check that inserted line numbers sync up with those on the print page
    m = re.search("<lb n='([0-9]*[05])'",l)
    if( re.search("[02468].txt",fname) and m):
       sline = int(m.group(1))
       p = re.search("(^| )(" + m.group(1) + ")(<|\\b)",l)
       if( p is None ):
        sys.stderr.write("fail " + fname + ' ' + str(sline) + l + "\n")
       else:
        l = re.sub(" (" + m.group(1) + ")\\b"," <milestone unit='printlnum' n='\g<1>'/>",l)
    if( re.search("[13579].txt",fname) and m):
       sline = int(m.group(1))
       p = re.search("\\b(" + m.group(1) + ")( |<)",l)
       if( p is None ):
        sys.stderr.write("fail2 " + fname + ' ' + str(sline) + l + "\n")
       else:
        l = re.sub("\\b(" + m.group(1) + ") ","<milestone unit='printlnum' n='\g<1>'/> ",l)

       
      
    if( re.search("\\b[ABCDEFGMNPQRSW]\\b|\|\||\\bcf\\b|\\bscr\\b|>\\s*1\\b",l) and innotes is 0):
      print ("<note>")
      innotes = 1
    if( innotes is 1):
       subs = ''
       l = re.sub("(\|\||>|II)\\s*([0-9\-]+)","\g<1></note> <note n='\g<2>'>",l)
       l = re.sub("\\s*(\|\||II)\\s*(</note>)","\g<2>",l)
       l = re.sub("\\b(\||I)\\b","</note> <note>",l)
       l = re.sub("(\||I) ","</note> <note>",l)
 # assume that patterns of the form [0-9]+,[ ]+[0-9]+ point to "PAGE,LINE" and should be aggregated.
       l = re.sub("([0-9]+),\s+([0-9]+)","\g<1>,\g<2>",l)
# assume for now that any floating number, number-number or number,number starts a new note
       l = re.sub("([ >])([0-9][0-9,\-]*) ","\g<1></note> <note n='float\g<2>'>",l)
       l = re.sub("\\b([ABCDEFGMNPQRSW]+|Ord|[wpqr])\\b","<ref>\g<1></ref>",l)
    if( innotes is 0):
      print(l)
    else:
      l = re.sub("[ ]*<note","\n<note",l)
      print(l,end="")
  if( innotes is 0 ):
        sys.stderr.write("nonotes " + fname + ' '  + l + "\n")
   
  print ("</note>")
  f.close()

f = open("basehead2.txt","r")
for l in f:
  print(l,end="")

while (arguments >= position):
    fname = sys.argv[position]
    flabel = re.sub("\.txt","",fname)

    m=re.search("697604807_([0-9]+)",fname)
    if(m):
     curpage = int(m.group(1))

     if( curpage > 130 and curpage < 196):
      #print ("parameter %i: %s" % (position, fname))
      print("<pb n=\"",flabel,"\"/>",sep="")
      dofile(fname)
    position = position + 1


print(" ")
print("</p></div></body></text></TEI>")
