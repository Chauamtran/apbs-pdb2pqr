""" Python APBS Driver File
    
    This module allows a user to run APBS through Python. Use this module if
    you wish to include APBS in a Python-based application.

    The module mimics the main.c driver that is used in the C version of APBS.
    The functions which are called are located in apbslib.py, which is 
    automatically generated by SWIG to wrap each APBS function.  See the APBS
    documentation for more information about each function.

    Todd Dolinsky (todd@ccb.wustl.edu)
    Nathan Baker (baker@biochem.wustl.edu)
    Washington University in St. Louis

	APBS -- Adaptive Poisson-Boltzmann Solver

	  Nathan A. Baker (baker@biochem.wustl.edu)
	  Dept. Biochemistry and Molecular Biophysics
	  Center for Computational Biology
	  Washington University in St. Louis

	  Additional contributing authors listed in the code documentation.

	Copyright (c) 2002-2009, Washington University in St. Louis.
	Portions Copyright (c) 2002-2009.  Nathan A. Baker
	Portions Copyright (c) 1999-2002.  The Regents of the University of California.
	Portions Copyright (c) 1995.  Michael Holst

	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met: 

	* Redistributions of source code must retain the above copyright notice, this
	list of conditions and the following disclaimer.  

	* Redistributions in binary form must reproduce the above copyright notice,
	this list of conditions and the following disclaimer in the documentation
	and/or other materials provided with the distribution.

	* Neither the name of Washington University in St. Louis nor the names of its
	contributors may be used to endorse or promote products derived from this
	software without specific prior written permission.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
	"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
	LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
	A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
	CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
	EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
	PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
	PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
	LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
	NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""" 

from apbslib import *
import sys, time
import string
from sys import stdout, stderr

__author__ = "Todd Dolinsky, Nathan Baker"
__date__ = "July 2007"
__version__ = "1.1.0"

Python_kb = 1.3806581e-23
Python_Na = 6.0221367e+23
NOSH_MAXMOL = 20
NOSH_MAXCALC = 20

class APBSError(Exception):
    """ APBSError class

        The APBSError class inherits off the Exception module and returns
        a string defining the nature of the error. 
    """
    
    def __init__(self, value):
        """
            Initialize with error message

            Parameters
                value:  Error Message (string)
        """
        self.value = value
        
    def __str__(self):
        """
            Return the error message
        """
        return `self.value`

def getHeader():
    """ Get header information about APBS
        Returns (header)
            header: Information about APBS
    """

    header = "\n\n\
    ----------------------------------------------------------------------\n\
    Adaptive Poisson-Boltzmann Solver (APBS)\n\
    Version 1.1.0\n\
    \n\
    APBS -- Adaptive Poisson-Boltzmann Solver\n\
    \n\
    Nathan A. Baker (baker@biochem.wustl.edu)\n\
    Dept. Biochemistry and Molecular Biophysics\n\
    Center for Computational Biology\n\
    Washington University in St. Louis\n\
    \n\
    Additional contributing authors listed in the code documentation.\n\
    \n\
    Copyright (c) 2002-2009, Washington University in St. Louis.\n\
    Portions Copyright (c) 2002-2009.  Nathan A. Baker\n\
    Portions Copyright (c) 1999-2002.  The Regents of the University of California.\n\
    Portions Copyright (c) 1995.  Michael Holst\n\
    \n\
    All rights reserved.\n\
    \n\
    Redistribution and use in source and binary forms, with or without\n\
    modification, are permitted provided that the following conditions are met:\n\
    \n\
    * Redistributions of source code must retain the above copyright notice, this\n\
      list of conditions and the following disclaimer.\n\
    \n\
    * Redistributions in binary form must reproduce the above copyright notice,\n\
      this list of conditions and the following disclaimer in the documentation\n\
      and/or other materials provided with the distribution.\n\
    \n\
    * Neither the name of Washington University in St. Louis nor the names of its\n\
      contributors may be used to endorse or promote products derived from this\n\
      software without specific prior written permission.\n\
    \n\
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n\
    \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n\
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR\n\
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR\n\
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,\n\
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,\n\
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR\n\
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF\n\
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING\n\
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n\
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\
    ----------------------------------------------------------------------\n\
    \n\n"

    return header

def getUsage():
    """ Get usage information about running APBS via Python
        Returns (usage)
            usage: Text about running APBS via Python
    """
    
    usage = "\n\n\
    ----------------------------------------------------------------------\n\
    This driver program calculates electrostatic potentials, energies,\n\
    and forces using both multigrid methods.\n\
    It is invoked as:\n\n\
      python main.py apbs.in\n\
    ----------------------------------------------------------------------\n\n"

    return usage

def main():
    """ Main driver for testing.  Runs APBS on given input file """
    
    # Initialize the MALOC library
    startVio()

    # Initialize variables, arrays
    com = Vcom_ctor(1)
    rank = Vcom_rank(com)
    size = Vcom_size(com)
    mgparm = MGparm()
    pbeparm = PBEparm()
    mem = Vmem_ctor("Main")
    pbe = new_pbelist(NOSH_MAXMOL)
    pmg = new_pmglist(NOSH_MAXMOL)
    pmgp = new_pmgplist(NOSH_MAXMOL)
    realCenter = double_array(3)
    totEnergy = []
    nforce = int_array(NOSH_MAXCALC)
    atomforce = new_atomforcelist(NOSH_MAXCALC)
    
    # Start the main timer
    main_timer_start = time.clock()

    # Check invocation
    stdout.write(getHeader())
    if len(sys.argv) != 2:
        stderr.write("main:  Called with %d arguments!\n" % len(sys.argv))
        stderr.write(getUsage())
        raise APBSError, "Incorrect Usage!"

    # Parse the input file
    nosh = NOsh_ctor(rank, size)
    input_file = sys.argv[1]
    stdout.write("Parsing input file %s...\n" % input_file)
    if NOsh_parseInputFile(nosh, input_file) != 1:
        stderr.write("main:  Error while parsing input file.\n")
        raise APBSError, "Error while parsing input file!"

    # Load the molecules using loadMolecules routine
    # loadMolecule passing NULL as second arg instead of Vparam
    alist = new_valist(NOSH_MAXMOL)
    if loadMolecules(nosh,None,alist) != 1:
        stderr.write("main:  Error while loading molecules. \n")
        raise APBSError, "Error while loading molecules!"

    # Setup the calculations
    
    if NOsh_setupElecCalc(nosh, alist) != 1:
        stderr.write("main: Error while setting up calculations. \n")
        raise APBSError, "Error while setting up calculations!"

    # Load the necessary maps

    dielXMap = new_gridlist(NOSH_MAXMOL)
    dielYMap = new_gridlist(NOSH_MAXMOL)
    dielZMap = new_gridlist(NOSH_MAXMOL)
    if loadDielMaps(nosh, dielXMap, dielYMap, dielZMap) != 1:
        stderr.write("Error reading dielectric maps!\n")
        raise APBSError, "Error reading dielectric maps!"
    
    kappaMap = new_gridlist(NOSH_MAXMOL)
    if loadKappaMaps(nosh, kappaMap) != 1:
        stderr.write("Error reading kappa maps!\n")
        raise APBSError, "Error reading kappa maps!"

    chargeMap = new_gridlist(NOSH_MAXMOL)
    if loadChargeMaps(nosh, chargeMap) != 1:
        stderr.write("Error reading charge maps!\n")
        raise APBSError, "Error reading charge maps!"

    # Do the calculations

    stdout.write("Preparing to run %d PBE calculations. \n" % nosh.ncalc)

    for icalc in xrange(nosh.ncalc): totEnergy.append(0.0)

    for icalc in xrange(nosh.ncalc):
        stdout.write("---------------------------------------------\n")
        calc = NOsh_getCalc(nosh, icalc)
        mgparm = calc.mgparm
        pbeparm = calc.pbeparm
        if calc.calctype != 0:
            stderr.write("main:  Only multigrid calculations supported!\n")
            raise APBSError, "Only multigrid calculations supported!"

        for k in range(0, nosh.nelec):
            if NOsh_elec2calc(nosh,k) >= icalc:
                break

        name = NOsh_elecname(nosh, k)
        if name == "":
            stdout.write("CALCULATION #%d:  MULTIGRID\n" % (icalc+1))
        else:
            stdout.write("CALCULATION #%d (%s): MULTIGRID\n" % ((icalc+1),name))
        stdout.write("Setting up problem...\n")
	
        # Routine initMG
	
        if initMG(icalc, nosh, mgparm, pbeparm, realCenter, pbe, 
              alist, dielXMap, dielYMap, dielZMap, kappaMap, chargeMap, 
              pmgp, pmg) != 1:
            stderr.write("Error setting up MG calculation!\n")
            raise APBSError, "Error setting up MG calculation!"
	
        # Print problem parameters if desired (comment out if you want
        # to minimize output to stdout)
	
        printMGPARM(mgparm, realCenter)
        printPBEPARM(pbeparm)
      
        # Solve the problem : Routine solveMG
	
        thispmg = get_Vpmg(pmg,icalc)

        if solveMG(nosh, thispmg, mgparm.type) != 1:
            stderr.write("Error solving PDE! \n")
            raise APBSError, "Error Solving PDE!"

        # Set partition information : Routine setPartMG

        if setPartMG(nosh, mgparm, thispmg) != 1:
            stderr.write("Error setting partition info!\n")
            raise APBSError, "Error setting partition info!"
	
        # Get the energies - the energy for this calculation
        # (calculation number icalc) will be stored in the totEnergy array

        ret, totEnergy[icalc] = energyMG(nosh, icalc, thispmg, 0, \
                                         totEnergy[icalc], 0.0, 0.0, 0.0)
        
        # Calculate forces
        
        aforce = get_AtomForce(atomforce, icalc)
        wrap_forceMG(mem, nosh, pbeparm, mgparm, thispmg, aforce, alist, nforce, icalc)
          
        # Write out data from MG calculations : Routine writedataMG	
        writedataMG(rank, nosh, pbeparm, thispmg)
	
        # Write out matrix from MG calculations	
        writematMG(rank, nosh, pbeparm, thispmg)
    
    # Handle print statements - comment out if limiting output to stdout

    if nosh.nprint > 0:
        stdout.write("---------------------------------------------\n")
        stdout.write("PRINT STATEMENTS\n")
    for iprint in xrange(nosh.nprint):
        if NOsh_printWhat(nosh, iprint) == NPT_ENERGY:
            printEnergy(com, nosh, totEnergy, iprint)
        elif NOsh_printWhat(nosh, iprint) == NPT_FORCE:
            printForce(com, nosh, nforce, atomforce, iprint)
        else:
            stdout.write("Undefined PRINT keyword!\n")
            break
                
    stdout.write("----------------------------------------\n")
    stdout.write("CLEANING UP AND SHUTTING DOWN...\n")

    # Clean up APBS structures
    killForce(mem, nosh, nforce, atomforce)
    killEnergy()
    killMG(nosh, pbe, pmgp, pmg)
    killChargeMaps(nosh, chargeMap)
    killKappaMaps(nosh, kappaMap)
    killDielMaps(nosh, dielXMap, dielYMap, dielZMap)
    killMolecules(nosh, alist)
    
    delete_Nosh(nosh)

    # Clean up Python structures

    delete_double_array(realCenter)
    delete_int_array(nforce)
    delete_atomforcelist(atomforce)
    delete_valist(alist)
    delete_gridlist(dielXMap)
    delete_gridlist(dielYMap)
    delete_gridlist(dielZMap)
    delete_gridlist(kappaMap)
    delete_gridlist(chargeMap)
    delete_pmglist(pmg)
    delete_pmgplist(pmgp)
    delete_pbelist(pbe)
    
    
    # Clean up MALOC structures
    delete_Com(com)
    delete_Mem(mem)
    stdout.write("\n")
    stdout.write("Thanks for using APBS!\n\n")

    # Stop the main timer
    main_timer_stop = time.clock()
    stdout.write("Total execution time:  %1.6e sec\n" % (main_timer_stop - main_timer_start))

 
if __name__ == "__main__": main()
