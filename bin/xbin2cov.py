#!/usr/bin/env python
# Programmer : zhuxp
# Date: 
# Last-modified: 12-30-2012, 14:12:21 CST
VERSION="0.1"
import os,sys,argparse
from xplib.Annotation import Bed
from xplib import TableIO
import signal
signal.signal(signal.SIGPIPE,signal.SIG_DFL)
import gzip
import time
from xplib.Struct import binindex as b
'''
Read the genome annatation file
count them in different size bin windows
input a bin structure
output coverage total nt for each bin
'''
def ParseArg():
    ''' This Function Parse the Argument '''
    p=argparse.ArgumentParser( description = 'Example: %(prog)s -h', epilog='Library dependency : xplib')
    p.add_argument('-v','--version',action='version',version='%(prog)s '+VERSION)
    p.add_argument('-i','--input',dest="input",default="stdin",type=str,help="input file DEFAULT: STDIN")
    p.add_argument('-I','--input_format',dest="format",default="bed",type=str,help="input file format")
    p.add_argument('-o','--output',dest="output",type=str,default="stdout",help="output file DEFAULT: STDOUT")
    p.add_argument('-g','--genome',dest="genome",type=str,default=None,help="chromosome sizes file")
    return p.parse_args()

def Main():
    '''
    IO TEMPLATE
    '''
    global args,out
    args=ParseArg()
    if args.output=="stdout":
        out=sys.stdout
    else:
        try:
            out=open(args.output,"w")
        except IOError:
            print >>sys.stderr,"can't open file ",args.output,"to write. Using stdout instead"
            out=sys.stdout
    if args.input=="stdin":
        fin=sys.stdin
    else:
        try:
            x=args.input.split(".")
            if x[-1]=="gz":
                fin=gzip.open(args.input,"r")
            else:
                fin=open(args.input,"r")
        except IOError:
            print >>sys.stderr,"can't read file",args.input
            fin=sys.stdin
    '''
    END OF IO TEMPLATE 
    '''
    if args.genome is not None:
        chr_sizes={}
        for x in TableIO.parse(args.genome):
            chr_sizes[x[0]]=int(x[1])
    bins=b()
    print >>out,"# This data was generated by program ",sys.argv[0]," (version: %s)"%VERSION,
    print >>out,"in bam2x ( https://github.com/nimezhu/bam2x )"
    print >>out,"# Date: ",time.asctime()
    print >>out,"# The command line is :"
    print >>out,"#","\t".join(sys.argv)
    print >>out,"chr\tstart\tstop\tbinindex\tcoverage\tcoverage_nt\tbinlevel\tbinsize " 
    header=False
    if (args.format=="metabed"): header=True

    for i,x in enumerate(TableIO.parse(fin,args.format,header=header)):
        if i%1000==0:
            print >>sys.stderr,"reading %d entries\r"%i,
        bins.append(x)
    c=b.bin2cov(bins)
    for chr in sorted(c.keys()):
        for i,x in enumerate(c[chr]):
            (start,end)=b.bin2range(i)
            if args.genome is not None:
                if start > chr_sizes[chr]:
                    continue
                if end > chr_sizes[chr]:
                    end=chr_sizes[chr]
            print >>out,chr,"\t",start,"\t",end,"\t",i,"\t",float(x)/(end-start),"\t",x,"\t",b.bin2level(i),"\t",end-start





    
if __name__=="__main__":
    Main()





