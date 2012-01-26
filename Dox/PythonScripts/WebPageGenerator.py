#!/usr/bin/env python

# A python script to generate the VistA cross reference web page
# To run the script, please do
# python WebPageGenerator.py -l <logFileDir> -r <VistA-Repository-Dir> -o <outputDir>
# Make sure that all the css/html files under web directory are copied to outputDIr
#---------------------------------------------------------------------------
# Copyright 2011 The Open Source Electronic Health Record Agent
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import CallerGraphParser
import os
import os.path
import sys
import subprocess
import urllib
import string
import bisect
import argparse
import shutil
import csv

from datetime import datetime, date, time
from CrossReference import *
from LogManager import logger
import logging
from operator import itemgetter, attrgetter

MAX_DEPENDENCY_LIST_SIZE = 20 # Do not generate the graph if have more than 20 nodes
PROGRESS_METER = 1000
LOCAL_VARIABLE_SECTION_HEADER_LIST = ["Name &nbsp;(>>&nbsp;not killed explicitly)", '''Line Occurrences &nbsp;(* Changed, &nbsp;! Killed, &nbsp;~ Newed)''']
GLOBAL_VARIABLE_SECTION_HEADER_LIST = ["Name", '''Line Occurrences &nbsp;(* Changed, &nbsp;! Killed)''']
DEFAULT_VARIABLE_SECTION_HEADER_LIST = ["Name", "Line Occurrences"]
LINE_TAG_PER_LINE = 10
# constants for html page
GOOGLE_ANALYTICS_JS_CODE = """
<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-26757196-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
"""
TOP_INDEX_BAR_PART = """
<center>
<a href="index.html" class="qindex">Home</a>&nbsp;&nbsp;
<a href="packages.html" class="qindex">Package List</a>&nbsp;&nbsp;
<a href="routines.html" class="qindex">Routine Alphabetical List</a>&nbsp;&nbsp;
<a href="globals.html" class="qindex">Global Alphabetical List</a>&nbsp;&nbsp;
<a href="Packages_Namespace_Mapping.html" class="qindex">Package-Namespace Mapping</a>&nbsp;&nbsp;
<BR>
</center>
"""
COMMON_HEADER_PART = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><head>
<meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1">
<title>OSEHRA VistA Code Documentation</title>
<link href="DoxygenStyle.css" rel="stylesheet" type="text/css">
"""
HEADER_END = """
</head>
"""
DEFAULT_BODY_PART = """
<body bgcolor="#ffffff">
"""
SOURCE_CODE_BODY_PART = """
<body bgcolor="#ffffff" onload="prettyPrint()">
"""
CODE_PRETTY_JS_CODE = """
<link href="code_pretty_scripts/prettify.css" type="text/css" rel="stylesheet" />
<script type="text/javascript" src="code_pretty_scripts/prettify.js"></script>
<script type="text/javascript" src="code_pretty_scripts/lang-mumps.js"></script>
"""
INDEX_HTML_PAGE_HEADER = """
<div class="header">
  <div class="headertitle">
  </div>
 <h1>VistA Cross Reference Documentation (Beta)</h1>
</div>
"""
INDEX_HTML_PAGE_OSEHRA_IMAGE_PART = """
<br/>
<center>
<div class="content">
<a href="http://www.osehra.org"><img src="http://www.osehra.org/sites/default/files/commons_osehra_logo.png" style="border-width:0" alt="OSEHRA" /></a>
</div>
</center>
<br/>
"""
INDEX_HTML_PAGE_INTRODUCTION_PART = """
<h2><a class ="anchor" id="intro"></a>Introduction</h2>
<p>Welcome to VistA Cross Reference Documentation Page. This documentation is generated with the results of XINDEX utility running against the VistA code base pulled from the <a href="http://code.osehra.org"/>repository</a>. This documentation provides direct dependency information among packages, as well as direct call graph information and source code for individual routines.
<br/>
<h2><a class ="anchor" id="howto"></a>How to use this documentation</h2>
To view information related to a specified package like dependency graph and list, please click "Package List" link at the top of this page and click the package you are interested in. To view information related to a specified routine/global, you can either find the routine/global via "Routine Alphabetical List"/"Global Alphabetical List" link or under the individual package page.
<br/>
<br/>
"""
#===============================================================================
#
#===============================================================================
class GraphvizCallGraphRoutineVisit(CallerGraphParser.RoutineVisit):
    def visitRoutine(self, routine, outputDir):
        pass
#        generateRoutineDependencyGraph(routine, outputDir)
#===============================================================================
#
#===============================================================================
class GraphvizCallerGraphRoutineVisit(CallerGraphParser.RoutineVisit):
    def visitRoutine(self, routine, outputDir):
        pass
#        generateRoutineDependencyGraph(routine, outputDir, False)

#===============================================================================
#
#===============================================================================
class GraphvizPackageDependencyVisit(CallerGraphParser.PackageVisit):
    def visitPackage(self, package, outputDir):
        generatePackageDependencyGraph(package, outputDir, True)
#===============================================================================
#
#===============================================================================
class GraphvizPackageDependentVisit(CallerGraphParser.PackageVisit):
    def visitPackage(self, package, outputDir):
        generatePackageDependencyGraph(package, outputDir, False)
#===============================================================================
#
#===============================================================================
class CplusRoutineVisit(CallerGraphParser.RoutineVisit):
    def visitRoutine(self, routine, outputDir):
        calledRoutines = routine.getCalledRoutines()
        if not calledRoutines or len(calledRoutines) == 0:
            logger.warn("No called Routines found! for package:%s" % routineName)
            return
        routineName = routine.getName()
        if not routine.getPackage():
            logger.error("ERROR: package: %s does not belongs to a package" % routineName)
            return

        packageName = routine.getPackage().getName()
        try:
            dirName = os.path.join(outputDir, packageName)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
        except OSError, e:
            logger.error("Error making dir %s : Error: %s" % (dirName, e))
            return

        outputFile = open(os.path.join(dirName, routineName), 'w')
        outputFile.write(("/*! \\namespace %s \n") % (packageName))
        outputFile.write("*/\n")
        outputFile.write("namespace %s {" % packageName)

        outputFile.write("/* Global Vars: */\n")
        for var in routine.getGlobalVariables():
            outputFile.write(" int %s;\n" % var)
        outputFile.write("\n")
        outputFile.write("/* Naked Globals: */\n")
        for var in routine.getNakeGlobals:
            outputFile.write(" int %s;\n" % var)
        outputFile.write("\n")
        outputFile.write("/* Marked Items: */\n")
        for var in routine.getMarkedItems():
            outputFile.write(" int %s;\n" % var)
        outputFile.write("\n")
        outputFile.write("/*! \callgraph\n")
        outputFile.write("*/\n")
        outputFile.write ("void " + self.name + "(){\n")

        outputFile.write("/* Local Vars: */\n")
        for var in routine.getLocalVariables():
            outputFile.write(" int %s; \n" % var)


        outputFile.write("/* Called Routines: */\n")
        for var in calledRoutines:
            outputFile.write("  %s ();\n" % var)
        outputFile.write("}\n")
        outputFile.write("}// end of namespace")
        outputFile.close()

# utility functions
def getGlobalHtmlFileNameByName(globalName):
    return urllib.quote("Global_%s.html" %
                        normalizeGlobalName(globalName))
def getGlobalHtmlFileName(globalVar):
    return urllib.quote("Global_%s.html" %
                        normalizeGlobalName(globalVar.getName()))
def getRoutineHtmlFileName(routineName):
    return urllib.quote(getRoutineHtmlFileNameUnquoted(routineName))
def getRoutineHtmlFileNameUnquoted(routineName):
    return "Routine_%s.html" % routineName
def getPackageHtmlFileName(packageName):
    return urllib.quote("Package_%s.html" %
                        normalizePackageName(packageName))
def getRoutineHypeLinkByName(routineName):
    return "<a href=\"%s\">%s</a>" % (getRoutineHtmlFileName(routineName),
                                      routineName);
def getGlobalHypeLinkByName(globalName):
    return "<a href=\"%s\">%s</a>" % (getGlobalHtmlFileNameByName(globalName),
                                      globalName);
def getPackageHyperLinkByName(packageName):
    return "<a href=\"%s\">%s</a>" % (getPackageHtmlFileName(packageName),
                                      packageName);
def normalizePackageName(packageName):
    newName = packageName.replace(' ', '_')
    return newName.replace('-', "_")

def normalizeGlobalName(globalName):
    return globalName.replace('^', '').replace('%', '_').replace('.', '_').replace("(", '_').replace('"', '_').replace(' ', '_')

def getRoutineSourceCodeFileByName(routineName,
                                   packageName,
                                   sourceDir):
    return os.path.join(sourceDir, "Packages" +
                        os.path.sep + packageName +
                        os.path.sep + "Routines" +
                        os.path.sep +
                        routineName + ".m")
def getRoutineSourceHtmlFileNameUnquoted(routineName):
    return "Routine_%s_source.html" % routineName
def getRoutineSourceHtmlFileName(routineName):
    return urllib.quote(getRoutineSourceHtmlFileNameUnquoted(routineName))
# generate index bar based on input list
def generateIndexBar(outputFile, inputList, archList=None):
    if (not inputList) or len(inputList) == 0:
        return
    hasArchList = archList and len(archList) == len(inputList)
    outputFile.write("<div class=\"qindex\">\n")
    for i in range(len(inputList) - 1):
        if hasArchList:
            archName = archList[i]
        else:
            archName = inputList[i]
        outputFile.write("<a class=\"qindex\" href=\"#%s\">%s</a>&nbsp;|&nbsp;\n" % (archName,
                                                                                     inputList[i]))
    if hasArchList:
        archName = archList[-1]
    else:
        archName = inputList[-1]
    outputFile.write("<a class=\"qindex\" href=\"#%s\">%s</a></div>\n" % (archName,
                                                                          inputList[-1]))
# generate Indexed Page Table Row
def generateIndexedTableRow(outputFile, inputList, httpLinkFunction,
                            nameFunc=None, indexSet=set(char for char in string.uppercase)):
    if not inputList or len(inputList) == 0:
        return
    outputFile.write("<tr>")
    for item in inputList:
        if len(item) == 1 and item in indexSet:
            outputFile.write("<td><a name=\"%s\"></a>" % item)
            outputFile.write("<table border=\"0\" cellspacing=\"0\" cellpadding=\"0\">")
            outputFile.write("<tr><td><div class=\"ah\">&nbsp;&nbsp;%s&nbsp;&nbsp;</div></td></tr>" % item)
            outputFile.write("</table></td>")
            indexSet.remove(item)
        else:
            displayName = item
            if nameFunc:
                displayName = nameFunc(item)
            outputFile.write("<td><a class=\"el\" href=\"%s\">%s</a>&nbsp;&nbsp;&nbsp;</td>" %
                             (httpLinkFunction(item),
                              displayName))
    outputFile.write("</tr>\n")
def generateIndexedPackageTableRow(outputFile, inputList,
                                   nameFunc=None, indexSet=set(char for char in string.uppercase)):
    generateIndexedTableRow(outputFile, inputList, getPackageHtmlFileName,
                            nameFunc, indexSet)
def generateIndexedRoutineTableRow(outputFile, inputList,
                                   nameFunc=None, indexSet=set(char for char in string.uppercase)):
    generateIndexedTableRow(outputFile, inputList, getRoutineHtmlFileName,
                            nameFunc, indexSet)
def generateIndexedGlobalTableRow(outputFile, inputList,
                                  nameFunc=None, indexSet=set(char for char in string.uppercase)):
    generateIndexedTableRow(outputFile, inputList, getGlobalHtmlFileNameByName,
                            nameFunc, indexSet)
def getPackageDependencyHtmlFile(packageName, depPackageName):
    firstName = normalizePackageName(packageName)
    secondName = normalizePackageName(depPackageName)
    if firstName < secondName:
        temp = firstName
        firstName = secondName
        secondName = temp
    return "Package_%s-%s_detail.html" % (firstName, secondName)
def getPackagePackageDependencyHyperLink(packageName,
                                         depPackageName,
                                         name,
                                         dependency=True):
    if dependency:
        edgeLinkArch = packageName
    else:
        edgeLinkArch = depPackageName
    return "<a href=\"%s#%s\">%s</a>" % (getPackageDependencyHtmlFile(packageName,
                                                                      depPackageName),
                                         edgeLinkArch,
                                         name)
def writeTableHeader(headerList, outputFile):
    outputFile.write("<tr>\n")
    for header in headerList:
        outputFile.write("<th class=\"IndexKey\">%s</th>\n" % header)
    outputFile.write("</tr>\n")
def writeTableData(itemRow, outputFile):
    outputFile.write("<tr>\n")
    index = 0;
    for data in itemRow:
        if index == 0:
            key = "IndexKey"
        else:
            key = "IndexValue"
        outputFile.write("<td class=\"%s\">%s</td>\n" % (key, data))
        index += 1
    outputFile.write("</tr>\n")
def writeGenericTablizedData(headerList, itemList, outputFile):
    outputFile.write("<table>\n")
    if headerList and len(headerList) > 0:
        writeTableHeader(headerList, outputFile)
    if itemList and len(itemList) > 0:
        for itemRow in itemList:
            writeTableData(itemRow, outputFile)
    outputFile.write("</table>\n")
def writeSectionHeader(headerName, archName, outputFile):
    outputFile.write("<h2 align=\"left\"><a name=\"%s\">%s</a></h2>\n" % (archName,
                                                                       headerName))
def writeSubSectionHeader(headerName, outputFile):
    outputFile.write("<h3 align=\"left\">%s</h3>\n" % (headerName))
# class to generate the web page based on input
class WebPageGenerator:
    def __init__(self, crossReference, outDir, repDir, docRepDir, gitPath):
        self._crossRef = crossReference
        self._allPackages = crossReference.getAllPackages()
        self._allRoutines = crossReference.getAllRoutines()
        self._allGlobals = crossReference.getAllGlobals()
        self._outDir = outDir
        self._repDir = repDir
        self._docRepDir = docRepDir
        self._gitPath = gitPath
        self._header = []
        self._footer = []
        self._source_header = []
        self._hasDot = False
        self._dotPath = ""
        self.__initWebTemplateFile__()

    def __initWebTemplateFile__(self):
        #load _header and _footer in the memory
        self.__generateHtmlPageHeader__(True)
        self.__generateHtmlPageHeader__(False)
        webDir = os.path.join(self._docRepDir, "Web")
        footer = open(os.path.join(webDir, "footer.html"), 'r')
        for line in footer:
            self._footer.append(line)
        footer.close()
    def setDotPath(self, dotPath):
        self._hasDot = True
        self._dotPath = dotPath
    def __includeHeader__(self, outputFile):
        for line in self._header:
            outputFile.write(line)
    def __includeFooter__(self, outputFile):
        for line in self._footer:
            outputFile.write(line)
    def __inlcudeSourceHeader__(self, outputFile):
        for line in self._source_header:
            outputFile.write(line)
#===============================================================================
# Template method to generate the web pages
#===============================================================================
    def generateWebPage(self):
        self.generateIndexHtmlPage()
        self.generatePackageNamespaceGlobalMappingPage()
        if self._hasDot and self._dotPath:
            self.generatePackageDependenciesGraph()
            self.generatePackageDependentsGraph()
        self.generateGlobalNameIndexPage()
        self.generateGlobalFileNoIndexPage()
        self.generateIndividualGlobalPage()
        self.generateRoutineIndexPage()
        self.generatePackageIndexPage()
        self.generatePackagePackageInteractionDetail()
        self.generateIndividualPackagePage()
        if self._hasDot and self._dotPath:
            self.generateRoutineCallGraph()
            self.generateRoutineCallerGraph()
        self.generateAllSourceCodePage(False)
        self.generateAllIndividualRoutinePage()
#===============================================================================
# Method to generate the index.html page
#===============================================================================
    def generateIndexHtmlPage(self):
        outputFile = open(os.path.join(self._outDir, "index.html"), 'wb')
        outputFile.write(COMMON_HEADER_PART)
        outputFile.write(GOOGLE_ANALYTICS_JS_CODE)
        outputFile.write(HEADER_END)
        outputFile.write(DEFAULT_BODY_PART)
        outputFile.write(INDEX_HTML_PAGE_HEADER)
        outputFile.write(TOP_INDEX_BAR_PART)
        outputFile.write(INDEX_HTML_PAGE_OSEHRA_IMAGE_PART)
        outputFile.write(INDEX_HTML_PAGE_INTRODUCTION_PART)
        self.__generateGitRepositoryKey__(outputFile)
        self.__includeFooter__(outputFile)
    def __generateGitRepositoryKey__(self, outputFile):
        sha1Key = self.__getGitRepositLatestSha1Key__()
        outputFile.write("""<h6><a class ="anchor" id="howto"></a>Note:Repository SHA1 key:%s</h6>\n""" % sha1Key)
    def __getGitRepositLatestSha1Key__(self):
        gitCommand = os.path.join(self._gitPath, "git") + " rev-parse --verify HEAD"
        os.chdir(self._repDir)
        logger.debug("git Command is %s" % gitCommand)
        result = subprocess.check_output(gitCommand)
        return result.strip()
    def __generateHtmlPageHeader__(self, isSource = False):
        if isSource:
            output = self._source_header
        else:
            output = self._header
        output.append(COMMON_HEADER_PART)
        if isSource:
            output.append(CODE_PRETTY_JS_CODE)
        output.append(GOOGLE_ANALYTICS_JS_CODE)
        output.append(HEADER_END)
        if isSource:
            output.append(SOURCE_CODE_BODY_PART)
        else:
            output.append(DEFAULT_BODY_PART)
        output.append(TOP_INDEX_BAR_PART)
#===============================================================================
# Method to generate Package Namespace Mapping page
#===============================================================================
    def generatePackageNamespaceGlobalMappingPage(self):
        outputFile = open(os.path.join(self._outDir, "Packages_Namespace_Mapping.html"), 'wb')
        self.__includeHeader__(outputFile)
        outputFile.write("<div><h1>%s</h1></div>\n" % "Package Namespace Mapping")
#        writeSectionHeader("Package Namespace Mapping", "Package Namespace Mapping", outputFile)
        # print the table header
        outputFile.write("<table>\n")
        writeTableHeader(["PackageName",
                          "Namespaces",
                          "Additional Globals"],
                         outputFile)
        allPackage = sorted(self._allPackages.keys())
        for packageName in allPackage:
            package = self._allPackages[packageName]
            namespaces = package.getNamespaces()
            globalNamespaces = package.getGlobalNamespace()
            totalCol = max(len(namespaces),
                           len(globalNamespaces))
            for index in range(totalCol):
                outputFile.write("<tr>")
                # write the package name
                if index == 0:
                    outputFile.write("<td class=\"IndexKey\">%s</td>" % getPackageHyperLinkByName(packageName))
                else:
                    outputFile.write("<td class=\"IndexKey\"></td>")
                # write the namespace
                if index <= len(namespaces) - 1:
                    outputFile.write("<td class=\"IndexValue\">%s</td>" % namespaces[index])
                else:
                    outputFile.write("<td class=\"IndexValue\"></td>")
                # write the additional globals
                if index <= len(globalNamespaces) - 1:
                    outputFile.write("<td class=\"IndexValue\">%s</td>" % globalNamespaces[index])
                else:
                    outputFile.write("<td class=\"IndexValue\"></td>")
                outputFile.write("</tr>\n")
        outputFile.write("</table>\n")
        outputFile.write("<BR>\n")
        self.__includeFooter__(outputFile)
        outputFile.close()
#===============================================================================
#
#===============================================================================
    def generateGlobalNameIndexPage(self):
        outputFile = open(os.path.join(self._outDir, "globals.html"), 'w')
        self.__includeHeader__(outputFile)
        outputFile.write("<div class=\"_header\">\n")
        outputFile.write("<div class=\"headertitle\">")
        outputFile.write("<h1>Global Index List</h1>\n</div>\n</div>")
        generateIndexBar(outputFile, string.uppercase)
        outputFile.write("<div class=\"contents\">\n")
        sortedGlobals = [] # a list of list
        for globalVar in self._allGlobals.itervalues():
            sortedName = globalVar.getName()[1:] # get rid of ^
            if sortedName.startswith('%'): # get rid of %
                sortedName = sortedName[1:]
            sortedGlobals.append([sortedName, globalVar.getName()])
        sortedGlobals = sorted(sortedGlobals,
                             key=lambda item: item[0])
        for letter in string.uppercase:
            bisect.insort_left(sortedGlobals, [letter, letter])
        totalGlobals = len(sortedGlobals)
        totalCol = 4
        numPerCol = totalGlobals / totalCol + 1
        outputFile.write("<table align=\"center\" width=\"95%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n")
        for i in range(numPerCol):
            itemsPerRow = [];
            for j in range(totalCol):
                if (i + numPerCol * j) < totalGlobals:
                    itemsPerRow.append(sortedGlobals[i + numPerCol * j][1]);
            generateIndexedGlobalTableRow(outputFile, itemsPerRow)
        outputFile.write("</table>\n</div>\n")
        generateIndexBar(outputFile, string.uppercase)
        self.__includeFooter__(outputFile)
        outputFile.close()
#===============================================================================
#
#===============================================================================
    def generateGlobalFileNoIndexPage(self):
        pass
#===============================================================================
#
#===============================================================================
    def generateIndividualGlobalPage(self):
        logger.info("Start generating individual globals......")
        indexList = ["Info", "Accessed By Routines"]
        for package in self._allPackages.itervalues():
            if isUnknownPackage(package.getName()):
                continue
            for (globalName, globalVar) in package.getAllGlobals().iteritems():
                outputFile = open(os.path.join(self._outDir,
                                               getGlobalHtmlFileNameByName(globalName)), 'w')
                # write the same _header file
                self.__includeHeader__(outputFile)
                # generated the qindex bar
                generateIndexBar(outputFile, indexList)
                outputFile.write("<div class=\"_header\">\n")
                outputFile.write("<div class=\"headertitle\">")
                outputFile.write(("<h4>Package: %s</h4>\n</div>\n</div>"
                                   % getPackageHyperLinkByName(package.getName())))
                outputFile.write("<h1>Global: %s</h1>\n</div>\n</div><br/>\n" % globalName)
                writeSectionHeader("Information", "Info", outputFile)
                infoHeader = ["FileMan FileNo", "FileMan Filename", "Package"]
                itemList = [[globalVar.getFileNo(),
                          globalVar.getDescription(),
                          getPackageHyperLinkByName(package.getName())]]
                writeGenericTablizedData(infoHeader, itemList, outputFile)
                writeSectionHeader("Accessed By Routines", "Accessed By Routines", outputFile)
                self.generateGlobalDependentsSection(globalVar, outputFile, True)
                outputFile.write("<br/>\n")
                # generated the index bar at the bottom
                generateIndexBar(outputFile, indexList)
                self.__includeFooter__(outputFile)
                outputFile.close()
        logger.info("End of generating individual globals......")
#===============================================================================
#
#===============================================================================
    def generateGlobalDependentsSection(self, globalVar,
                                        outputFile,
                                        isDependents=True):
        depRoutines = globalVar.getAllReferencedRoutines()
        sortedPackage = sorted(sorted(depRoutines.keys()),
                           key=lambda item: len(depRoutines[item]),
                           reverse=True)
        infoHeader = ["Package", "Total", "Routines"]
        itemList = []
        for package in sortedPackage:
            routineSet = depRoutines[package]
            itemRow = []
            itemRow.append(getPackageHyperLinkByName(package.getName()))
            itemRow.append(len(routineSet))
            routineData = ""
            index = 0
            for routine in sorted(routineSet):
                routineData += ("<a class=\"e1\" href=\"%s\">%s" %
                             (getRoutineHtmlFileName(routine.getName()),
                              routine.getName()))
                if (index + 1) % 8 == 0:
                    routineData += "</a><BR>"
                else:
                    routineData += "</a>&nbsp;&nbsp;&nbsp;&nbsp;"
                index += 1
            itemRow.append(routineData)
            itemList.append(itemRow)
        writeGenericTablizedData(infoHeader, itemList, outputFile)
#===============================================================================
#method to generate the interactive detail list page between any two packages
#===============================================================================
    def generatePackagePackageInteractionDetail(self):
        packDepDict = dict()
        for package in self._allPackages.itervalues():
            if isUnknownPackage(package.getName()):
                continue
            for depPack in package.getPackageRoutineDependencies().iterkeys():
                if isUnknownPackage(package.getName()):
                    continue
                fileName = getPackageDependencyHtmlFile(package.getName(),
                                                        depPack.getName())
                if fileName not in packDepDict:
                    packDepDict[fileName] = (package, depPack)
            for depPack in package.getPackageGlobalDependencies().iterkeys():
                if isUnknownPackage(package.getName()):
                    continue
                fileName = getPackageDependencyHtmlFile(package.getName(),
                                                        depPack.getName())
                if fileName not in packDepDict:
                    packDepDict[fileName] = (package, depPack)
        for (key, value) in packDepDict.iteritems():
            self.generatePackageInteractionDetailPage(key, value[0], value[1])

#===============================================================================
# method to generate caller/called routine detail dict
#===============================================================================
    def generatePackageRoutineDetailDict(self, package, depPackage, depDict):
        depRoutinesDict = dict()
        for routine in depDict[depPackage]:
            details = routine.getCalledRoutines()[depPackage]
            for depRoutine in details.iterkeys():
                if depRoutine not in depRoutinesDict:
                    depRoutinesDict[depRoutine] = []
                depRoutinesDict[depRoutine].append(routine)
        return depRoutinesDict
#===============================================================================
# method to generate the detail of package
#===============================================================================
    def generatePackageRoutineDependencyDetailPage(self, package, depPackage, outputFile):
        packageHyperLink = getPackageHyperLinkByName(package.getName())
        depPackageHyperLink = getPackageHyperLinkByName(depPackage.getName())
        # generate section header
        writeSectionHeader("%s-->%s :" % (packageHyperLink, depPackageHyperLink),
                           package.getName(), outputFile)
        routineDepDict = package.getPackageRoutineDependencies()
        globalDepDict = package.getPackageGlobalDependencies()
        callerRoutines = set()
        calledRoutines = set()
        referredRoutines = set()
        referredGlobals = set()
        if routineDepDict and depPackage in routineDepDict:
            callerRoutines = routineDepDict[depPackage][0]
            calledRoutines = routineDepDict[depPackage][1]
        if globalDepDict and depPackage in globalDepDict:
            referredRoutines = globalDepDict[depPackage][0]
            referredGlobals = globalDepDict[depPackage][1]
        totalCalledHtml = "<span class=\"comment\">%d</span>" % len(callerRoutines)
        totalCallerHtml = "<span class=\"comment\">%d</span>" % len(calledRoutines)
        totalReferredRoutineHtml = "<span class=\"comment\">%d</span>" % len(referredRoutines)
        totalReferredGlobalHtml = "<span class=\"comment\">%d</span>" % len(referredGlobals)
        summaryHeader = "Summary:<BR> Total %s routine(s) in %s called total %s routine(s) in %s" % (totalCalledHtml,
                                                                                               packageHyperLink,
                                                                                               totalCallerHtml,
                                                                                               depPackageHyperLink)
        summaryHeader += "<BR> Total %s routine(s) in %s accessed total %s global(s) in %s" % (totalReferredRoutineHtml,
                                                                                             packageHyperLink,
                                                                                             totalReferredGlobalHtml,
                                                                                             depPackageHyperLink)
        writeSubSectionHeader(summaryHeader, outputFile)
        # print out the routine details
        if len(callerRoutines) > 0:
            writeSubSectionHeader("Caller Routines List in %s : %s" % (packageHyperLink,
                                                                       totalCalledHtml),
                                                                       outputFile)
            self.generateTablizedItemList(sorted(callerRoutines), outputFile,
                                          getRoutineHtmlFileName, self.getRoutineDisplayName)
        if len(calledRoutines) > 0:
            writeSubSectionHeader("Called Routines List in %s : %s" % (depPackageHyperLink,
                                                                       totalCallerHtml),
                                                                       outputFile)
            self.generateTablizedItemList(sorted(calledRoutines), outputFile,
                                          getRoutineHtmlFileName, self.getRoutineDisplayName)
        if len(referredRoutines) > 0:
            writeSubSectionHeader("Referred Routines List in %s : %s" % (packageHyperLink,
                                                                       totalReferredRoutineHtml),
                                                                       outputFile)
            self.generateTablizedItemList(sorted(referredRoutines), outputFile,
                                          getRoutineHtmlFileName, self.getRoutineDisplayName)
        if len(referredGlobals) > 0:
            writeSubSectionHeader("Referenced Global List in %s : %s" % (depPackageHyperLink,
                                                                       totalReferredGlobalHtml),
                                                                       outputFile)
            self.generateTablizedItemList(sorted(referredGlobals), outputFile,
                                          getGlobalHtmlFileName)
        outputFile.write("<br/>\n")
#===============================================================================
# method to generate the individual package/package interaction detail page
#===============================================================================
    def generatePackageInteractionDetailPage(self, fileName, package, depPackage):
        outputFile = open(os.path.join(self._outDir, fileName), 'w')
        self.__includeHeader__(outputFile)
        packageHyperLink = getPackageHyperLinkByName(package.getName())
        depPackageHyperLink = getPackageHyperLinkByName(depPackage.getName())
        #generate the index bar
        inputList = ["%s-->%s" % (package.getName(), depPackage.getName()),
                   "%s-->%s" % (depPackage.getName(), package.getName())]
        archList = [package.getName(), depPackage.getName()]
        generateIndexBar(outputFile, inputList, archList)
        outputFile.write("<div><h1>%s and %s Interaction Details</h1></div>\n" %
                         (packageHyperLink, depPackageHyperLink))
        #generate the summary part.
        self.generatePackageRoutineDependencyDetailPage(package, depPackage, outputFile)
        self.generatePackageRoutineDependencyDetailPage(depPackage, package, outputFile)
        generateIndexBar(outputFile, inputList, archList)
        self.__includeFooter__(outputFile)
        outputFile.close()

#===============================================================================
# Method to parse the source code and generate source code page or just extract comments
#===============================================================================
    def __generateSourceCodePageByName__(self, sourceCodeName, routine, justComment):
        if not routine:
            logger.error("Routine can not be None")
            return
        package = routine.getPackage()
        if not package:
            logger.error("Routine %s does not belong to a package" % routine)
            return
        packageName = package.getName()
        routineName = routine.getName()
        sourcePath = getRoutineSourceCodeFileByName(sourceCodeName,
                                                    packageName,
                                                    self._repDir)
        if not os.path.exists(sourcePath):
            logger.error("Souce file:[%s] does not exit\n" % sourcePath)
            return
        sourceFile = open(sourcePath, 'r')
        if not justComment:
            outputFile = open(os.path.join(self._outDir,
                                         getRoutineSourceHtmlFileNameUnquoted(sourceCodeName)), 'wb')
            self.__inlcudeSourceHeader__(outputFile)
            outputFile.write("<div><h1>%s.m</h1></div>\n" % sourceCodeName)
            outputFile.write("<a href=\"%s\">Go to the documentation of this file.</a>" %
                             getRoutineHtmlFileName(routineName))
            outputFile.write("<xmp class=\"prettyprint lang-mumps linenums:1\">\n")
        lineNo = 0
        for line in sourceFile:
            if lineNo <= 1:
                routine.addComment(line)
            if justComment and lineNo > 1:
                break
            if not justComment:
                outputFile.write(line)
            lineNo += 1
        sourceFile.close()
        if not justComment:
            outputFile.write("</xmp>\n")
            self.__includeFooter__(outputFile)
            outputFile.close()
#===============================================================================
# Method to generate individual source code page for Platform Dependent Routines
#===============================================================================
    def __generatePlatformDependentRoutineSourcePage__(self, genericRoutine, justComment):
        assert genericRoutine
        assert isinstance(genericRoutine, PlatformDependentGenericRoutine)
        assert self._crossRef.isPlatformGenericRoutineByName(genericRoutine.getName())
        allRoutines = genericRoutine.getAllPlatformDepRoutines()
        for routineInfo in allRoutines.itervalues():
            routine = routineInfo[0]
            sourceCodeName = routine.getOriginalName()
            self.__generateSourceCodePageByName__(sourceCodeName, routine, justComment)
#===============================================================================
# Method to generate individual source code page
# sourceDir should be VistA-FOIA git repository
#===============================================================================
    def generateAllSourceCodePage(self, justComment=True):
        for packageName in self._allPackages.iterkeys():
            if isUnknownPackage(packageName):
                continue
            for (routineName, routine) in self._allPackages[packageName].getAllRoutines().iteritems():
                if self._crossRef.isPlatformGenericRoutineByName(routineName):
                    self.__generatePlatformDependentRoutineSourcePage__(routine, justComment)
                    continue
                # check for platform dependent routine
                if not self._crossRef.routineHasSourceCodeByName(routineName):
                    logger.debug("Routine:%s does not have source code" % routineName)
                    continue
                sourceCodeName = routine.getOriginalName()
                self.__generateSourceCodePageByName__(sourceCodeName, routine, justComment)
#===============================================================================
# utility method to show routine name
#===============================================================================
    def getRoutineDisplayNameByName(self, routineName):
        if self._crossRef.isPlatformGenericRoutineByName(routineName):
            return "%s&sup1" % routineName # superscript 1
        if not self._crossRef.routineHasSourceCodeByName(routineName):
            return "%s&sup2" % routineName # superscript 2
        return routineName
    def getRoutineDisplayName(self, routine):
        return self.getRoutineDisplayNameByName(routine.getName())
#===============================================================================
# Method to generate routine Index page
#===============================================================================
    def generateRoutineIndexPage(self):
        outputFile = open(os.path.join(self._outDir, "routines.html"), 'w')
        self.__includeHeader__(outputFile)
        outputFile.write("<div class=\"_header\">\n")
        outputFile.write("<div class=\"headertitle\">")
        outputFile.write("<h1>Routine Index List</h1>\n</div>\n</div>")
        indexList = [char for char in string.uppercase]
        indexList.insert(0, "%")
        indexSet = sorted(set(indexList))
        generateIndexBar(outputFile, indexList)
        outputFile.write("<div class=\"contents\">\n")
        sortedRoutines = []
        for routine in self._allRoutines.itervalues():
            # ignore the routines from UNKNOWN Package
            if isUnknownPackage(routine.getPackage().getName()):
                continue
            sortedRoutines.append(routine.getName())
        sortedRoutines = sorted(sortedRoutines)
        for letter in indexList:
            bisect.insort_left(sortedRoutines, letter)
        totalRoutines = len(sortedRoutines)
        totalCol = 4
        numPerCol = totalRoutines / totalCol + 1
        outputFile.write("<table align=\"center\" width=\"95%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n")
        for i in range(numPerCol):
            itemsPerRow = [];
            for j in range(totalCol):
                if (i + numPerCol * j) < totalRoutines:
                    item = sortedRoutines[i + numPerCol * j]
                    itemsPerRow.append(item);
            generateIndexedRoutineTableRow(outputFile, itemsPerRow,
                                           self.getRoutineDisplayNameByName,
                                           indexSet)
        outputFile.write("</table>\n</div>\n")
        generateIndexBar(outputFile, indexList)
        self.__includeFooter__(outputFile)
        outputFile.close()
    #===============================================================================
    # Return a dict with package as key, a list of 4 as value
    #===============================================================================
    def __mergePackageDependenciesList__(self, package, isDependencies=True):
        routineDepDict = dict()
        if isDependencies:
            routineDeps = package.getPackageRoutineDependencies()
            globalDeps = package.getPackageGlobalDependencies()
        else:
            routineDeps = package.getPackageRoutineDependents()
            globalDeps = package.getPackageGlobalDependents()
        for (package, depTuple) in routineDeps.iteritems():
            if package not in routineDepDict:
                routineDepDict[package] = [0, 0, 0, 0]
            routineDepDict[package][0] = len(depTuple[0])
            routineDepDict[package][1] = len(depTuple[1])
        for (package, depTuple) in globalDeps.iteritems():
            if package not in routineDepDict:
                routineDepDict[package] = [0, 0, 0, 0]
            routineDepDict[package][2] = len(depTuple[0])
            routineDepDict[package][3] = len(depTuple[1])
        return routineDepDict
    #===============================================================================
    ## Method to generate the package dependency/dependent graph
    #===============================================================================
    def generatePackageDependencyGraph(self, package, dependencyList=True):
        depPackagesDict = None
        if dependencyList:
            depPackagesDict = package.getPackageRoutineDependencies()
            packageSuffix = "_dependency"
        else:
            depPackagesDict = package.getPackageRoutineDependents()
            packageSuffix = "_dependent"
        packageName = package.getName()
        normalizedName = normalizePackageName(packageName)
        totalPackage = 0
        if depPackagesDict:
            totalPackage = len(depPackagesDict)
        if  (totalPackage == 0) or (totalPackage > MAX_DEPENDENCY_LIST_SIZE):
            logger.info("Nothing to do exiting... Package: %s Total: %d " %
                         (packageName, totalPackage))
            return
        try:
            dirName = os.path.join(self._outDir, packageName)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
        except OSError, e:
            logger.error("Error making dir %s : Error: %s" % (dirName, e))
            return
        output = open(os.path.join(dirName, normalizedName + packageSuffix + ".dot"), 'w')
        output.write("digraph %s {\n" % (normalizedName + packageSuffix))
        output.write("\tnode [shape=box fontsize=14];\n") # set the node shape to be box
        output.write("\tnodesep=0.35;\n") # set the node sep to be 0.35
        output.write("\transsep=0.55;\n") # set the rank sep to be 0.75
        output.write("\tedge [fontsize=14];\n") # set the edge label and size props
        output.write("\t%s [style=filled fillcolor=orange label=\"%s\"];\n" % (normalizedName,
                                                                               packageName))
        # merge the routine and package list
        depPackageMerged = self.__mergePackageDependenciesList__(package, dependencyList)
        # sort by the sum of the total # of routines
        depPackages = sorted(depPackageMerged.keys(),
                           key=lambda item: sum(depPackageMerged[item][0:3:2]),
                           reverse=True)
        for depPackage in depPackages:
            depPackageName = depPackage.getName()
            normalizedDepPackName = normalizePackageName(depPackageName)
            output.write("\t%s [label=\"%s\" URL=\"%s\"];\n" % (normalizedDepPackName,
                                                                depPackageName,
                                                                getPackageHtmlFileName(depPackageName)))
    #            output.write("\t%s->%s [label=\"depends\"];\n" % (normalizedName, normalizePackageName(depPackageName.getName())))
            depMetricsList = depPackageMerged[depPackage]
            edgeWeight = depMetricsList[0] + depMetricsList[2]
            edgeLinkURL = getPackageDependencyHtmlFile(normalizedName, normalizedDepPackName)
            edgeStartNode = normalizedName
            edgeEndNode = normalizedDepPackName
            edgeLinkArch = packageName
            toolTipStartPackage = packageName
            toolTipEndPackage = depPackageName
            if not dependencyList:
                edgeStartNode = normalizedDepPackName
                edgeEndNode = normalizedName
                edgeLinkArch = depPackageName
                toolTipStartPackage = depPackageName
                toolTipEndPackage = toolTipEndPackage
            # default for routine only
            edgeToolTip = "Total %d routines in %s called total %d routines in %s" % (depMetricsList[0],
                                                                         toolTipStartPackage,
                                                                         depMetricsList[1],
                                                                         toolTipEndPackage)
            edgeLabel = "%s(R)" % (depMetricsList[0])
            edgeStyle = "solid"
            if depMetricsList[0] > 0 and depMetricsList[2] > 0:
                edgeLabel = "%d(R)\\n%d(G)" % (depMetricsList[0], depMetricsList[2])
                edgeToolTip += " Total %d routines in %s accessed total %d globals in %s" % (depMetricsList[2],
                                                                                   toolTipStartPackage,
                                                                                   depMetricsList[3],
                                                                                   toolTipEndPackage)
                edgeStyle = "bold"
            elif depMetricsList[2] > 0:
                edgeLabel = "%s(G)" % (depMetricsList[2])
                edgeToolTip = " Total %d routines in %s accessed total %d globals in %s" % (depMetricsList[2],
                                                                                  toolTipStartPackage,
                                                                                  depMetricsList[3],
                                                                                  toolTipEndPackage)
                edgeStyle = "dashed"
            output.write("\t%s->%s [label=\"%s\" weight=%d URL=\"%s#%s\" style=\"%s\" labeltooltip=\"%s\" edgetooltip=\"%s\"];\n" % (edgeStartNode,
                                                     edgeEndNode,
                                                     edgeLabel,
                                                     edgeWeight,
                                                     edgeLinkURL,
                                                     edgeLinkArch,
                                                     edgeStyle,
                                                     edgeToolTip,
                                                     edgeToolTip))
        output.write("}\n")
        output.close()
        # use dot tools to generated the image and client side mapping
        outputName = os.path.join(dirName, normalizedName + packageSuffix + ".gif")
        outputmap = os.path.join(dirName, normalizedName + packageSuffix + ".cmapx")
        inputName = os.path.join(dirName, normalizedName + packageSuffix + ".dot")
        # this is to generated the image in gif format and also cmapx (client side map) to make sure link
        # embeded in the graph is clickable
        command = "%s -Tgif -o\"%s\" -Tcmapx -o\"%s\" \"%s\"" % (os.path.join(self._dotPath, "dot"),
                                                               outputName,
                                                               outputmap,
                                                               inputName)
        retCode = subprocess.call(command)
        if retCode != 0:
            logger.error("calling dot with command[%s] returns %d" % (command, retCode))
#===============================================================================
#
#===============================================================================
    def generateRoutineCallGraph(self, isCalled=True):
        logger.info("Start generating call graph......")
        for package in self._allPackages.itervalues():
            if isUnknownPackage(package.getName()):
                continue
            routines = package.getAllRoutines()
            for routine in routines.itervalues():
                isPlatformGenericRoutine = self._crossRef.isPlatformGenericRoutineByName(routine.getName())
                if isCalled and isPlatformGenericRoutine:
                    self.generatePlatformGenericDependencyGraph(routine, isCalled)
                else:
                    self.generateRoutineDependencyGraph(routine, isCalled)
        logger.info("End of generating call graph......")
#===============================================================================
# Method to generate routine caller graph for platform dependent routines
#===============================================================================
    def generatePlatformGenericDependencyGraph(self, genericRoutine, isDependency):
        assert genericRoutine
        assert isinstance(genericRoutine, PlatformDependentGenericRoutine)
        if not isDependency:
            return
        platformRoutines = genericRoutine.getAllPlatformDepRoutines()
        for routineInfo in platformRoutines.itervalues():
            self.generateRoutineDependencyGraph(routineInfo[0], isDependency)
#===============================================================================
#
#===============================================================================
    def generateRoutineCallerGraph(self):
        self.generateRoutineCallGraph(False)
#===============================================================================
## generate all dot file and use dot to generated the image file format
#===============================================================================
    def generateRoutineDependencyGraph(self, routine, isDependency=True):
        if (not routine.getPackage()
            or isUnknownPackage(routine.getPackage().getName())):
            return
        routineName = routine.getName()
        packageName = routine.getPackage().getName()
        if isDependency:
            depRoutines = routine.getCalledRoutines()
            routineSuffix = "_called"
            totalDep = routine.getTotalCalled()
        else:
            depRoutines = routine.getCallerRoutines()
            routineSuffix = "_caller"
            totalDep = routine.getTotalCaller()
        #do not generate graph if no dep routines, totalDep routines > max_dependency_list
        # or only have unknown routines
        if (not depRoutines
            or len(depRoutines) == 0
            or  totalDep > MAX_DEPENDENCY_LIST_SIZE
            or len(depRoutines) == 1 and Package(UNKNOWN_PACKAGE) in depRoutines):
            logger.debug("No called Routines found! for routine:%s package:%s" % (routineName, packageName))
            return
        try:
            dirName = os.path.join(self._outDir, packageName)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
        except OSError, e:
            logger.error("Error making dir %s : Error: %s" % (dirName, e))
            return
        output = open(os.path.join(dirName, routineName + routineSuffix + ".dot"), 'wb')
        output.write("digraph \"%s\" {\n" % (routineName + routineSuffix))
        output.write("\tnode [shape=box fontsize=14];\n") # set the node shape to be box
        output.write("\tnodesep=0.45;\n") # set the node sep to be 0.15
        output.write("\transsep=0.45;\n") # set the rank sep to be 0.75
#        output.write("\tedge [fontsize=12];\n") # set the edge label and size props
        if routine.getPackage() not in depRoutines:
            output.write("\tsubgraph \"cluster_%s\"{\n" % (routine.getPackage()))
            output.write("\t\t\"%s\" [style=filled fillcolor=orange];\n" % routineName)
            output.write("\t}\n")
        for (package, callDict) in depRoutines.iteritems():
            if isUnknownPackage(str(package)):
                continue
            output.write("\tsubgraph \"cluster_%s\"{\n" % (package))
            for routine in callDict.keys():
                output.write("\t\t\"%s\" [URL=\"%s\"];\n" % (routine,
                                                         getRoutineHtmlFileName(routine)))
                if str(package) == packageName:
                    output.write("\t\t\"%s\" [style=filled fillcolor=orange];\n" % routineName)
            output.write("\t\tlabel=\"%s\";\n" % package)
            output.write("\t}\n")
            for (routine, tags) in callDict.iteritems():
                if isDependency:
                    output.write("\t\t\"%s\"->\"%s\"" % (routineName, routine))
                else:
                    output.write("\t\t\"%s\"->\"%s\"" % (routine, routineName))
                output.write(";\n")
        output.write("}\n")
        output.close()
        outputName = os.path.join(dirName, routineName + routineSuffix + ".gif")
        outputmap = os.path.join(dirName, routineName + routineSuffix + ".cmapx")
        inputName = os.path.join(dirName, routineName + routineSuffix + ".dot")
        # this is to generated the image in gif format and also cmapx (client side map) to make sure link
        # embeded in the graph is clickable
        # @TODO this should be able to run in parallel
        command = "%s -Tgif -o\"%s\" -Tcmapx -o\"%s\" \"%s\"" % (os.path.join(self._dotPath, "dot"),
                                                               outputName,
                                                               outputmap,
                                                               inputName)
        retCode = subprocess.call(command)
        if retCode != 0:
            logger.error("calling dot with command[%s] returns %d" % (command, retCode))
#===============================================================================
#
#===============================================================================
    def generatePackageDependenciesGraph(self, isDependency=True):
        # generate all dot file and use dot to generated the image file format
        if isDependency:
            name = "dependencies"
        else:
            name = "dependents"
        logger.info("Start generating package %s......" % name)
        logger.info("Total Packages: %d" % len(self._allPackages))
        for package in self._allPackages.values():
            if isUnknownPackage(package.getName()):
                continue
            self.generatePackageDependencyGraph(package, isDependency)
        logger.info("End of generating package %s......" % name)
#===============================================================================
#
#===============================================================================
    def generatePackageDependentsGraph(self):
        self.generatePackageDependenciesGraph(False)
#===============================================================================
#
#===============================================================================
    def generatePackageIndexPage(self):
        outputFile = open(os.path.join(self._outDir, "packages.html"), 'w')
        self.__includeHeader__(outputFile)
        #write the _header
        outputFile.write("<div class=\"_header\">\n")
        outputFile.write("<div class=\"headertitle\">")
        outputFile.write("<h1>Package List</h1>\n</div>\n</div>")
        generateIndexBar(outputFile, string.uppercase)
        outputFile.write("<div class=\"contents\">\n")
        #generated the table
        totalNumPackages = len(self._allPackages) + len(string.uppercase)
        totalCol = 3
        # list in three columns
        numPerCol = totalNumPackages / totalCol + 1
        sortedPackages = sorted(self._allPackages.keys())
        for letter in string.uppercase:
            bisect.insort_left(sortedPackages, letter)
        # write the table first
        outputFile.write("<table align=\"center\" width=\"95%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n")
        for i in range(numPerCol):
            itemsPerRow = [];
            for j in range(totalCol):
                if (i + numPerCol * j) < totalNumPackages:
                    itemsPerRow.append(sortedPackages[i + j * numPerCol]);
            generateIndexedPackageTableRow(outputFile, itemsPerRow)
        outputFile.write("</table>\n</div>\n")
        generateIndexBar(outputFile, string.uppercase)
        self.__includeFooter__(outputFile)
        outputFile.close()
#=======================================================================
# Method to generate package dependency/dependent section infp
#=======================================================================
    def generatePackageDependencySection(self, packageName, outputFile, isDependencyList=True):
        if isDependencyList:
            sectionGraphHeader = "Dependency Graph"
            sectionListHeder = "Package Dependency List"
            packageSuffix = "_dependency"
        else:
            sectionGraphHeader = "Dependent Graph"
            sectionListHeder = "Package Dependent List"
            packageSuffix = "_dependent"
        fileNamePrefix = normalizePackageName(packageName) + packageSuffix
        # write the image of the dependency graph
        writeSectionHeader(sectionGraphHeader, sectionGraphHeader, outputFile)
        try:
            cmapFile = open(os.path.join(self._outDir, packageName + "/" + fileNamePrefix + ".cmapx"), 'r')
            outputFile.write("<div class=\"contents\">\n")
            outputFile.write("<img src=\"%s\" border=\"0\" alt=\"Call Graph\" usemap=\"#%s\"/>\n"
                       % (packageName + "/" + fileNamePrefix + ".gif", fileNamePrefix))
            #append the content of map outputFile
            for line in cmapFile:
                outputFile.write(line)
            outputFile.write("</div>\n")
        except IOError:
            pass
        # write the list of the package dependency list
        package = self._allPackages[packageName]
        depPackagesByRoutineDict = dict()
        depPackagesByGlobalDict = dict()
        if isDependencyList:
            depPackagesByRoutineDict = package.getPackageRoutineDependencies()
            depPackagesByGlobalDict = package.getPackageGlobalDependencies()
        else:
            depPackagesByRoutineDict = package.getPackageRoutineDependents()
            depPackagesByGlobalDict = package.getPackageGlobalDependents()
        #sort the packages by total # of routines
        depPackagesMerged = self.__mergePackageDependenciesList__(package,
                                                            isDependencyList)
        depPackages = sorted(depPackagesMerged.keys(),
                           key=lambda item: sum(depPackagesMerged[item][0:3:2]),
                           reverse=True)
        totalPackages = 0
        if depPackages:
            totalPackages = len(depPackages)
        writeSectionHeader("%s Total: %d " % (sectionListHeder, totalPackages),
                           sectionListHeder,
                           outputFile)
        outputFile.write("<h4>Format:&nbsp;&nbsp;package[# of caller routines(R):# of global accessing routines(G)]</h4><BR>\n")
        if totalPackages > 0:
            outputFile.write("<div class=\"contents\"><table>\n")
            numOfCol = 6
            numOfRow = totalPackages / numOfCol + 1
            for index in range(numOfRow):
                outputFile.write("<tr>")
                for j in range(numOfCol):
                    if (index * numOfCol + j) < totalPackages:
                        depPackage = depPackages[index * numOfCol + j]
                        depPackageName = depPackage.getName()
                        depMetricsList = depPackagesMerged[depPackage]
                        linkName = "%d(R):%d(G)" % (depMetricsList[0], depMetricsList[2])
                        depHyperLink = getPackagePackageDependencyHyperLink(packageName,
                                                                          depPackageName,
                                                                          linkName,
                                                                          isDependencyList)
                        outputFile.write("<td class=\"indexkey\"><a class=\"e1\" href=\"%s\">%s</a> [%s]&nbsp;&nbsp;&nbsp</td>"
                                   % (getPackageHtmlFileName(depPackageName), depPackageName, depHyperLink))
                outputFile.write("</tr>\n")
            outputFile.write("</table></div>\n")
#===============================================================================
# method to generate a tablized representation of routines
#===============================================================================
    def generateTablizedItemList(self, sortedItemList, outputFile, htmlMappingFunc,
                                 nameFunc=None, totalCol=8, isUnknownPkg=False):
        totalNumRoutine = 0
        if sortedItemList:
            totalNumRoutine = len(sortedItemList)
        numOfRow = totalNumRoutine / totalCol + 1
        if totalNumRoutine > 0:
            outputFile.write("<div class=\"contents\"><table>\n")
            for index in range(numOfRow):
                outputFile.write("<tr>")
                for i in range(totalCol):
                    position = index * totalCol + i
                    if position < totalNumRoutine:
                        displayName = sortedItemList[position]
                        if nameFunc: displayName = nameFunc(displayName)
                        if not isUnknownPkg:
                            outputFile.write("<td class=\"indexkey\"><a class=\"e1\" href=\"%s\">%s</a>&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                                       % (htmlMappingFunc(sortedItemList[position]),
                                          displayName))
                        else:
                            outputFile.write("<td class=\"indexkey\">%s&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                                       % displayName)
                outputFile.write("</tr>\n")
            outputFile.write("</table>\n</div>\n<br/>")
#===============================================================================
# method to generate individual package page
#===============================================================================
    def generateIndividualPackagePage(self):
        indexList = ["Doc", "Dependency Graph", "Package Dependency List", "Dependent Graph", "Package Dependent List", "All Globals", "All Routines"]
        for packageName in self._allPackages.iterkeys():
            isUnknownPkg = isUnknownPackage(packageName)
            package = self._allPackages[packageName]
            outputFile = open(os.path.join(self._outDir, getPackageHtmlFileName(packageName)), 'w')
            #write the _header part
            self.__includeHeader__(outputFile)
            generateIndexBar(outputFile, indexList)
            outputFile.write("<div class=\"_header\">\n")
            outputFile.write("<div class=\"headertitle\">")
            outputFile.write("<h1>Package: %s</h1>\n</div>\n</div>" % packageName)
            # link to VA documentation
            writeSectionHeader("Documentation", "Doc", outputFile)
            if len(package.getDocLink()) > 0:
                outputFile.write("<p><h4>VA documentation in the <a href=\"%s\">VistA Documentation Library</a>" % package.getDocLink())
                if len(package.getDocMirrorLink()) > 0:
                    outputFile.write("&nbsp;or&nbsp;<a href=\"%s\">OSEHRA Mirror site</a></h4>\n" % package.getDocMirrorLink())
                else:
                    outputFile.write("</h4>\n")
            else:
                outputFile.write("<p><h4><a href=\"http://www.va.gov/vdl/\">VA documentation in the VistA Documentation Library</a></h4>\n")
            self.generatePackageDependencySection(packageName, outputFile, True)
            self.generatePackageDependencySection(packageName, outputFile, False)
            totalNumGlobals = len(package.getAllGlobals())
            writeSectionHeader("All Globals Total: %d" % totalNumGlobals,
                               "All Globals",
                               outputFile)
            sortedGlobals = sorted(package.getAllGlobals().keys())
            self.generateTablizedItemList(sortedGlobals, outputFile,
                                          getGlobalHtmlFileNameByName)
            sortedRoutines = sorted(package.getAllRoutines().keys())
            totalNumRoutine = len(sortedRoutines)
            writeSectionHeader("All Routines Total: %d" % totalNumRoutine,
                               "All Routines",
                               outputFile)
            self.generateTablizedItemList(sortedRoutines, outputFile,
                                          getRoutineHtmlFileName,
                                          self.getRoutineDisplayNameByName,
                                          8, isUnknownPkg)
            generateIndexBar(outputFile, indexList)
            self.__includeFooter__(outputFile)
            outputFile.close()
#===============================================================================
# method to generate Routine Dependency and Dependents page
#===============================================================================
    def generateRoutineDependencySection(self, routine, outputFile, dependencyList=True):
        routineName = routine.getName()
        packageName = routine.getPackage().getName()
        if dependencyList:
            depRoutines = routine.getCalledRoutines()
            sectionGraphHeader = "Call Graph"
            sectionListHeader = "Called Routines"
            tableHeaderText = "Called Routines"
            routineSuffix = "_called"
            totalNum = routine.getTotalCalled()
        else:
            depRoutines = routine.getCallerRoutines()
            sectionGraphHeader = "Caller Graph"
            sectionListHeader = "Caller Routines"
            routineSuffix = "_caller"
            tableHeaderText = "Caller Routines"
            totalNum = routine.getTotalCaller()
        fileNamePrefix = routineName + routineSuffix
        writeSectionHeader(sectionGraphHeader, sectionGraphHeader, outputFile)
        if totalNum > 0:
            # write the image of the caller graph
            try:
                fileName = os.path.join(self._outDir, packageName + "/" + fileNamePrefix + ".cmapx")
                cmapFile = open(os.path.join(self._outDir, packageName + "/" + fileNamePrefix + ".cmapx"), 'r')
                outputFile.write("<div class=\"contents\">\n")
                outputFile.write("<img src=\"%s\" border=\"0\" alt=\"%s\" usemap=\"#%s\"/>\n"
                           % (urllib.quote(packageName + "/" + fileNamePrefix + ".gif"),
                              sectionGraphHeader,
                              fileNamePrefix))
                #append the content of map outputFile
                for line in cmapFile:
                    outputFile.write(line)
                outputFile.write("</div>\n")
            except IOError:
                pass
            writeSectionHeader("%s Total: %d" % (sectionListHeader, totalNum),
                               sectionListHeader,
                               outputFile)
            outputFile.write("<div class=\"contents\"><table>\n")
            outputFile.write("<tr><th class=\"indexkey\">Package</th>")
            outputFile.write("<th class=\"indexvalue\">Total</th>")
            outputFile.write("<th class=\"indexvalue\">%s</th></tr>\n" % tableHeaderText)
            # sort the key by Total # of routines
            sortedDepRoutines = sorted(sorted(depRoutines.keys()),
                                     key=lambda item: len(depRoutines[item]),
                                     reverse=True)
            for depPackage in sortedDepRoutines:
                isUnknownPkg = isUnknownPackage(str(depPackage))
                if not isUnknownPkg:
                    routinePackageLink = getPackageHyperLinkByName(depPackage.getName())
                else:
                    routinePackageLink = depPackage
                routineNameLink = ""
                index = 0
                for depRoutine in sorted(depRoutines[depPackage].keys()):
                    if isUnknownPkg:
                        routineNameLink += depRoutine.getName()
                    else:
                        if dependencyList: # append tag information for called routines
#                            allTags = filter(len, depRoutines[depPackage][depRoutine].iterkeys())
                            allTags = depRoutines[depPackage][depRoutine].keys()
                            sortedTags = sorted(allTags)
                            # format the tag
                            tagString = ""
                            if len(sortedTags) > 1:
                                tagString = "("
                            idx = 0
                            for tag in sortedTags:
                                if idx > 0:
                                    tagString += ","
                                idx += 1
                                tagString += tag
                            if len(sortedTags) > 1:
                                tagString += ")"
                            routineNameLink += tagString + "^"
                        routineNameLink += getRoutineHypeLinkByName(depRoutine.getName())
                    routineNameLink += "&nbsp;&nbsp;"
                    if (index + 1) % 8 == 0:
                        routineNameLink += "<BR>"
                    index += 1
                outputFile.write("<tr><td class=\"indexkey\">%s</td><td class=\"indexvalue\">%d</td><td class=\"indexvalue\">%s</td></tr>\n"
                           % (routinePackageLink, len(depRoutines[depPackage]), routineNameLink))
            outputFile.write("</table>\n</div>\n")
#===============================================================================
# Method to generate routine variables sections such as Local Variables, Global Variables
#===============================================================================
    def generateRoutineVariableSection(self, outputFile, sectionTitle, headerList, variables,
                                       converFunc):
        writeSectionHeader(sectionTitle, sectionTitle, outputFile)
        outputList = converFunc(variables)
        writeGenericTablizedData(headerList, outputList, outputFile)
    def __convertVariableToTableData__(self, variables, isGlobal = False):
        output = []
        allVars = sorted(variables.iterkeys())
        for varName in allVars:
            var = variables[varName]
            if isGlobal and varName in self._allGlobals:
                varName = getGlobalHypeLinkByName(varName)
            lineOccurencesString = self.__generateLineOccurencesString__(var.getLineOffsets())
            output.append(((var.getPrefix()+varName).strip(), lineOccurencesString))
        return output
    def __generateLineOccurencesString__(self, lineOccurences):
        lineOccurencesString = ""
        index = 0
        for offset in lineOccurences:
            if index > 0:
                lineOccurencesString += ",&nbsp;"
            lineOccurencesString += offset
            if (index + 1) % LINE_TAG_PER_LINE == 0:
                lineOccurencesString +="<BR>"
            index += 1
        return lineOccurencesString
    def __convertGlobalVarToTableData__(self, variables):
        return self.__convertVariableToTableData__(variables, True)
    def __convertNakedGlobaToTableData__(self, variables):
        return self.__convertVariableToTableData__(variables, False)
    def __convertMarkedItemToTableData__(self, variables):
        return self.__convertVariableToTableData__(variables, False)
    def __convertLableReferenceToTableData__(self, variables):
        return self.__convertVariableToTableData__(variables, False)
    def __convertExternalReferenceToTableData__(self, variables):
        output = []
        allVars = sorted(variables.iterkeys(), key = itemgetter(0,1))
        for nameTag in allVars:
            lineOccurencesString = self.__generateLineOccurencesString__(variables[nameTag])
            output.append((nameTag[1]+"^"+getRoutineHypeLinkByName(nameTag[0]),
                           lineOccurencesString))
        return output
#===============================================================================
# Method to generate individual routine page
#===============================================================================
    def __generateIndividualRoutinePage__(self, routine, platform=None):
        assert routine
        indexList = ["Info", "Source", "Call Graph", "Called Routines",
                     "Caller Graph", "Caller Routines", "Global Variables", "External References",
                     "Label References", "Naked Globals", "Local Variables", "Marked Items"]
        routineName = routine.getName()
        package = routine.getPackage()
        outputFile = open(os.path.join(self._outDir,
                                       getRoutineHtmlFileNameUnquoted(routineName)), 'w')
        self.__includeHeader__(outputFile)
        # generated the qindex bar
        generateIndexBar(outputFile, indexList)
        outputFile.write("<div class=\"_header\">\n")
        outputFile.write("<div class=\"headertitle\">")
        outputFile.write("<h4>Package: %s</h4>\n</div>\n</div>" % getPackageHyperLinkByName(package.getName()))
        routineHeader = "Routine: %s " % routineName
        if platform:
            routineHeader += "Platform: %s" % platform
        outputFile.write("<h1>%s</h1>\n</div>\n</div><br/>\n" % routineHeader)
        writeSectionHeader("Information", "Info", outputFile)
        for comment in routine.getComment():
            outputFile.write("<p><span class=\"information\">%s</span></p>\n" % comment)
        writeSectionHeader("Source Code", "Source", outputFile)
        if routine.hasSourceCode():
            outputFile.write("<p><span class=\"information\">Source file &lt;<a class=\"el\" href=\"%s\">%s.m</a>&gt;</span></p>\n" %
                             (getRoutineSourceHtmlFileName(routine.getOriginalName()),
                              routine.getOriginalName()))
        else:
            outputFile.write("<p><span class=\"information\">Source file not available</span></p>\n")
        self.generateRoutineDependencySection(routine, outputFile, True)
        self.generateRoutineDependencySection(routine, outputFile, False)
        self.generateRoutineVariableSection(outputFile,
                                            "Global Variables",
                                            GLOBAL_VARIABLE_SECTION_HEADER_LIST,
                                            routine.getGlobalVariables(),
                                            self.__convertGlobalVarToTableData__)
        self.generateRoutineVariableSection(outputFile,
                                            "External References",
                                            DEFAULT_VARIABLE_SECTION_HEADER_LIST,
                                            routine.getExternalReference(),
                                            self.__convertExternalReferenceToTableData__)
        self.generateRoutineVariableSection(outputFile,
                                            "Label References",
                                            DEFAULT_VARIABLE_SECTION_HEADER_LIST,
                                            routine.getLabelReferences(),
                                            self.__convertLableReferenceToTableData__)
        self.generateRoutineVariableSection(outputFile,
                                            "Naked Globals",
                                            DEFAULT_VARIABLE_SECTION_HEADER_LIST,
                                            routine.getNakedGlobals(),
                                            self.__convertNakedGlobaToTableData__)
        self.generateRoutineVariableSection(outputFile,
                                            "Local Variables",
                                            LOCAL_VARIABLE_SECTION_HEADER_LIST,
                                            routine.getLocalVariables(),
                                            self.__convertVariableToTableData__)
        self.generateRoutineVariableSection(outputFile,
                                            "Marked Items",
                                            DEFAULT_VARIABLE_SECTION_HEADER_LIST,
                                            routine.getMarkedItems(),
                                            self.__convertMarkedItemToTableData__)
        outputFile.write("<br/>\n")
        # generated the index bar at the bottom
        generateIndexBar(outputFile, indexList)
        self.__includeFooter__(outputFile)
        outputFile.close()
#===============================================================================
# Method to generate page for platform-dependent generic routine page
#===============================================================================
    def __generatePlatformDepentGenericRoutinePage__(self, genericRoutine):
        assert genericRoutine
        assert isinstance(genericRoutine, PlatformDependentGenericRoutine)
        # generated the subpage for each platform routines
        platformDepRoutines = genericRoutine.getAllPlatformDepRoutines()
        for routineInfo in platformDepRoutines.itervalues():
            self.__generateIndividualRoutinePage__(routineInfo[0], routineInfo[1])
        indexList = ["Platform Dependent Routines", "Caller Graph", "Caller Routines"]
        routineName = genericRoutine.getName()
        package = genericRoutine.getPackage()
        outputFile = open(os.path.join(self._outDir,
                                       getRoutineHtmlFileNameUnquoted(routineName)), 'w')
        self.__includeHeader__(outputFile)
        # generated the qindex bar
        generateIndexBar(outputFile, indexList)
        outputFile.write("<div class=\"_header\">\n")
        outputFile.write("<div class=\"headertitle\">")
        outputFile.write("<h4>Package: %s</h4>\n</div>\n</div>" % getPackageHyperLinkByName(package.getName()))
        outputFile.write("<h1>Routine: %s</h1>\n</div>\n</div><br/>\n" % routineName)
        writeSectionHeader("Platform Dependent Routines", "DepRoutines", outputFile)
        # output the Platform part.
        tableRowList = []
        for routineInfo in platformDepRoutines.itervalues():
            tableRowList.append([getRoutineHypeLinkByName(routineInfo[0].getName()), routineInfo[1]])
        writeGenericTablizedData(["Routine", "Platform"], tableRowList, outputFile)
        self.generateRoutineDependencySection(genericRoutine, outputFile, False)
        outputFile.write("<br/>\n")
        # generated the index bar at the bottom
        generateIndexBar(outputFile, indexList)
        self.__includeFooter__(outputFile)
        outputFile.close()
#===============================================================================
# Method to generate all individual routine pages
#===============================================================================
    def generateAllIndividualRoutinePage(self):
        logger.info("Start generating all individual Routines......")
        totalNoRoutines = len(self._allRoutines)
        routineIndex = 0
        for package in self._allPackages.itervalues():
            if isUnknownPackage(package.getName()):
                continue
            for routine in package.getAllRoutines().itervalues():
                if (routineIndex + 1) % PROGRESS_METER == 0:
                    logger.info("Processing %d of total %d" % (routineIndex, totalNoRoutines))
                routineIndex += 1
                # handle the special case for platform dependent routine
                if self._crossRef.isPlatformGenericRoutineByName(routine.getName()):
                    self.__generatePlatformDepentGenericRoutinePage__(routine)
                else:
                    self.__generateIndividualRoutinePage__(routine)
        logger.info("End of generating individual routines......")

def testGenerateIndexBar(inputList, outputFile):
    outputFile = open(outputFile, 'w')
    outputFile.write("<html><head>Test</head><body>\n")
    generateIndexBar(outputFile, inputList)
    outputFile.write("</body></html>")
    outputFile.close()

#test to play around the Dot
def testDotCall(outputDir):
    packageName = "Nursing Service"
    routineName = "NURA6F1"
    dirName = os.path.join(outputDir, packageName);
    outputName = os.path.join(dirName, routineName + ".svg")
    inputName = os.path.join(dirName, routineName + ".dot")
    command = "dot -Tsvg -o \"%s\" \"%s\"" % (outputName, inputName)
    logger.info ("command is [%s]" % command)
    retCode = subprocess.call(command)
    logger.info ("calling dot returns %d" % retCode)

# Get the lastest git SHA1 Key from git repository
def testGetGitLastRev(GitRepoDir, gitPath):
    gitCommand = gitPath + "git rev-parse --verify HEAD"
    os.chdir(GitRepoDir)
    result = subprocess.check_output(gitCommand)
    print result.strip()

# test parsing package.csv file from VistA-FOIA release
def testPackageCsvParser(packageFile):
    csvFile = open(packageFile, 'rb')
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(csvFile.read(1024))
    csvFile.seek(0)
    hasHeader = sniffer.has_header(csvFile.read(1024))
    logger.info ("hasHeader: %s" % hasHeader)
    csvFile.seek(0)
    reader = csv.reader(csvFile, dialect)
    for line in reader:
        print line

# some testing constants
PACKAGE_CSV_FILE = "c:/users/jason.li/git/VistA-FOIA/Packages.csv"
GIT_PATH = "c:/Program Files (x86)/Git/bin/"
VISTA_FOIA_GIT_REP = "c:/users/jason.li/git/VistA-FOIA"
DEFAULT_OUTPUT_FILE_DIR = "c:/temp/VistA/"
# constants
DEFAULT_OUTPUT_LOG_FILE_NAME = "WebPageGen.log"

import tempfile
def getTempLogFile():
    return os.path.join(tempfile.gettempdir(), DEFAULT_OUTPUT_LOG_FILE_NAME)

def initLogging(outputFileName):
    logger.setLevel(logging.DEBUG)
    fileHandle = logging.FileHandler(outputFileName, 'w')
    fileHandle.setLevel(logging.DEBUG)
    formatStr = '%(asctime)s %(levelname)s %(message)s'
    formatter = logging.Formatter(formatStr)
    fileHandle.setFormatter(formatter)
    #set up the stream handle (console)
    consoleHandle = logging.StreamHandler()
    consoleHandle.setLevel(logging.INFO)
    consoleFormatter = logging.Formatter(formatStr)
    consoleHandle.setFormatter(consoleFormatter)
    logger.addHandler(fileHandle)
    logger.addHandler(consoleHandle)
#===============================================================================
# main
#===============================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='VistA Routine information Finder')
    parser.add_argument('-l', required=True, dest='logFileDir',
                        help='Input XINDEX log files directory, nomally under'
                             '${CMAKE_BUILD_DIR}/Docs/CallerGraph/')
    parser.add_argument('-r', required=True, dest='repositDir',
                        help='VistA Git Repository Directory')
    parser.add_argument('-b', required=True, dest="docRepositDir",
                        help="doc Repository directory contains code generating the documentation")
    parser.add_argument('-o', required=True, dest='outputDir',
                        help='Output Web Page dirctory')
    parser.add_argument('-git', required=True, dest='gitPath',
                        help='Path to the folder containing git excecutable')
    parser.add_argument('-dot', required=False, dest='hasDot', default="False", action='store_true',
                        help='is Dot installed')
    parser.add_argument('-dotpath', required=False, dest='dotPath',
                        help='path to the folder containing dot excecutable')
    parser.add_argument('-Log', required=False, dest='outputLogFileName',
                        help='the output Logging file')
    result = vars(parser.parse_args());
    if not result['outputLogFileName']:
        outputLogFile = getTempLogFile()
    else:
        outputLogFile = result['outputLogFileName']
    initLogging(outputLogFile)
    logger.debug (result)
    logParser = CallerGraphParser.CallerGraphLogFileParser()
    logger.info ("Starting parsing package/routine....")
    logger.info ("The log file is: %s" % outputLogFile)
    packagesDir = os.path.join(result['repositDir'], "Packages")
    logParser.parsePercentRoutineMappingFile(os.path.join(result['docRepositDir'],
                                                          "PercentRoutineMapping.csv"))
    logParser.parsePackagesFile(os.path.join(result['repositDir'],
                                             "Packages.csv"))
    logParser.parsePlatformDependentRoutineFile(os.path.join(result['docRepositDir'],
                                                                 "PlatformDependentRoutine.csv"))
    logParser.findGlobalsBySourceV2(packagesDir, "*/Globals/*.zwr")
    routineFilePattern = "*/Routines/*.m"
    logParser.findPackagesAndRoutinesBySource(packagesDir, routineFilePattern)
    logParser.parsePackageDocumentationLink(os.path.join(result['docRepositDir'], "PackageToVDL.csv"))
    logger.info ("End parsing package/routine....")
    logger.info ("Starting parsing caller graph log file....")

    callLogPattern = "*.log"
    logParser.parseAllCallerGraphLog(result['logFileDir'], callLogPattern)
    logger.info ("Starting generating web pages....")
    webPageGen = WebPageGenerator(logParser.getCrossReference(),
                                result['outputDir'],
                                result['repositDir'],
                                result['docRepositDir'],
                                result['gitPath'])
    if result['hasDot'] and result['dotPath']:
        webPageGen.setDotPath(result['dotPath'])
    webPageGen.generateWebPage()
    logger.info ("End of generating web pages....")