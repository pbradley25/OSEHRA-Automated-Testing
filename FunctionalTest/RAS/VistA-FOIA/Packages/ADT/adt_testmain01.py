'''
Created on November, 2012
@author: pbradley
This is the main test script that calls the underlying ADT functional tests
located in ADT_Suite001.
'''
import sys
import logging
sys.path = ['./RAS/lib'] + ['./dataFiles'] + ['../lib/vista'] + sys.path
import ADT_Suite001
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

def main():
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument('resultdir', help='Result Directory')
    parser.add_argument('-l', '--logging-level', help='Logging level')
    parser.add_argument('-f', '--logging-file', help='Logging file name')
    args = parser.parse_args()
    logging_level = LOGGING_LEVELS.get(args.logging_level, logging.NOTSET)
    logging.basicConfig(level=logging_level,
                      filename=args.logging_file,
                      format='%(asctime)s %(levelname)s: %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')

    if not os.path.isdir(args.resultdir):
      try:
         os.makedirs(args.resultdir)
      except OSError, e:
         if e.errno != errno.EEXIST:
             raise
    try:
        logging.debug('RESULTDIR: ' + args.resultdir)
        logging.debug('LOGGING:   ' + args.logging_level)
        resfile = args.resultdir + '/' + timeStamped('ADT_results.txt')
        if not os.path.isabs(args.resultdir):
            logging.error('EXCEPTION: Absolute Path Required for Result Directory')
            raise
        resultlog = file(resfile, 'w')
        ADT_Suite001.startmon(resultlog, args.resultdir)
        ADT_Suite001.setup_ward(resultlog, args.resultdir)
        ADT_Suite001.adt_test001(resultlog, args.resultdir)
        ADT_Suite001.adt_test002(resultlog, args.resultdir)
        ADT_Suite001.stopmon(resultlog, args.resultdir)
    except Exception, e:
        resultlog.write('\nADT TEST EXCEPTION ERROR:' + str(e))
        logging.error('*****ADT test exception*********' + str(e))
    finally:
        resultlog.write('finished')

if __name__ == '__main__':
  main()
