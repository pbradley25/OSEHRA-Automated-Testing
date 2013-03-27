'''
Created on Mar 25, 2013
@author: pbradley
This test automates the process of creating and comparing global output files between
refactored code and non-refactored code.

The pre-requsits of this script include:
1. The two namespaces exist in Cache
2. The ctest function tests have been executed

This script will do the following:
a. run D ^ZGO in each namespace and save the outputs in a /results subdirectory
b. use Ownership.csv to create a list of files to compare
c. perform diff compare on file list and place results in /results directory

To run this script from /OSEHRA-Automated-Testing (example):

>python Testing/Functional/RAS/lib/glb_cmp_test_01.py -l debug VISTA vistabin REFVISTA refvistabin ownership.csv 3130326

'''
import csv
import difflib
import time
import sys
import logging
sys.path = ['./Testing/Functional/RAS/lib'] + ['./Python/vista'] + sys.path
from Actions import Actions
import os, errno
import argparse
import datetime

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}


def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def connect_VistA(testname, result_dir, namespace):
    # Connect to VistA
    logging.debug('Connect_VistA' + ', Namespace: ' + namespace)
    from OSEHRAHelper import ConnectToMUMPS, PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + timeStamped(testname + '.txt'), instance='', namespace=namespace)
    if VistA.type == 'cache':
        try:
            VistA.ZN(namespace)
        except IndexError, no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA

def zgo_rem_time(filename, today):
    f = open(filename)
    lines = f.readlines();
    f.close()
    f = open(filename, 'w')
    key = today + '.'
    for line in lines:
        index = line.find(key)
        if index >= 0:
            index = index + 7
            i = index + 1
            while i < len(line) and line[i].isdigit():
                i = i + 1
            if i > index + 1:
                newline = line[:index] + line[i:]
            else:
                newline = line
        else:
            newline = line
        f.write("%s" % newline)
    f.close()

def main():
    usage = "usage: %prog [options] arg arg arg arg arg"
    parser = argparse.ArgumentParser()
    parser.add_argument('namespace1', help='Namespace 1')
    parser.add_argument('bin1dir', help='Name of namespace1 bin directory')
    parser.add_argument('namespace2', help='Namespace 2')
    parser.add_argument('bin2dir', help='Name of namespace2 bin directory')
    parser.add_argument('oshipfile', help='Ownership File')
    parser.add_argument('today', help='VistA Date')
    parser.add_argument('-l', '--logging-level', help='Logging level')
    parser.add_argument('-f', '--logging-file', help='Logging file name')
    args = parser.parse_args()
    logging_level = LOGGING_LEVELS.get(args.logging_level, logging.NOTSET)
    logging.basicConfig(level=logging_level,
                      filename=args.logging_file,
                      format='%(asctime)s %(levelname)s: %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
    # Create zgo 1 directory
    try:
        # os.chdir(args.bin1dir)
        zgo1dir = os.path.join(os.getcwd(), args.bin1dir, 'results', 'zgoA')
        os.makedirs(zgo1dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    # Create zgo 2 directory
    try:
        zgo2dir = os.path.join(os.getcwd(), args.bin2dir, 'results', 'zgoA')
        os.makedirs(zgo2dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

    try:
        fnamelist = []

        # run cmake and ctest for each namespace
        os.chdir(args.bin1dir)
        os.system('cmake -P ImportRG.cmake')
        os.system('ctest -R RAS_')
        time.sleep(10)
        os.chdir('../' + args.bin2dir)
        os.system('cmake -P ImportRG.cmake')
        os.system('ctest -R RAS_')
        os.chdir('../')

        # Do D ^ZGO for each namespace
        VistA1 = connect_VistA('zgo1log.txt', os.getcwd(), args.namespace1)
        foo1 = Actions(VistA1)
        foo1.zgo(zgo1dir + '\\')
        VistA2 = connect_VistA('zgo2log.txt', os.getcwd(), args.namespace2)
        foo2 = Actions(VistA2)
        foo2.zgo(zgo2dir + '\\')

        # Open Ownership.csv and create file list
        logging.debug('START DIFF')
        f = open(args.oshipfile, 'rt')
        reader = csv.reader(f)
        for row in reader:
            if row[4].upper() == 'REGISTRATION' or  row[4].upper() == 'SCHEDULING':
                fnamelist.append(row[0] + '+' + row[1] + '.zwr')
        f.close()

        # loop on list and perform diff
        for afile in fnamelist:
            file1 = os.path.join(args.bin1dir, 'results', 'zgoA', afile)
            file2 = os.path.join(args.bin2dir, 'results', 'zgoA', afile)
            if os.path.isfile(file1):
                zgo_rem_time(file1, args.today)
            else:
                os.system('echo ' + '\"' + file1 + '\"' + '\" does not exist\" ' + ' >> glbcmpresult.txt')
            if os.path.isfile(file2):
                zgo_rem_time(file2, args.today)
            else:
                os.system('echo ' + '\"' + file2 + '\"' + '\" does not exist\" ' + ' >> glbcmpresult.txt')
            if os.path.isfile(file1) and os.path.isfile(file2):
                os.system('echo ' + '\"' + file1 + ' vs ' + file2 + '\"' + '>> glbcmpresult.txt')
                os.system('diff ' + '\"' + file1 + '\"' + ' \"' + file2 + '\"' + '>> glbcmpresult.txt')


    except Exception, e:
        logging.error('*****exception*********' + str(e))
    finally:
        logging.debug('finished')

if __name__ == '__main__':
  main()


