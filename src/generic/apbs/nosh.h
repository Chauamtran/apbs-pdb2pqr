/* ///////////////////////////////////////////////////////////////////////////
/// APBS -- Adaptive Poisson-Boltzmann Solver
///
///  Nathan A. Baker (nbaker@wasabi.ucsd.edu)
///  Dept. of Chemistry and Biochemistry
///  Dept. of Mathematics, Scientific Computing Group
///  University of California, San Diego 
///
///  Additional contributing authors listed in the code documentation.
///
/// Copyright � 1999. The Regents of the University of California (Regents).
/// All Rights Reserved. 
/// 
/// Permission to use, copy, modify, and distribute this software and its
/// documentation for educational, research, and not-for-profit purposes,
/// without fee and without a signed licensing agreement, is hereby granted,
/// provided that the above copyright notice, this paragraph and the
/// following two paragraphs appear in all copies, modifications, and
/// distributions.
/// 
/// IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
/// SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
/// ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
/// REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.  
/// 
/// REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
/// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
/// PARTICULAR PURPOSE.  THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
/// ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS".  REGENTS HAS NO OBLIGATION
/// TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
/// MODIFICATIONS. 
//////////////////////////////////////////////////////////////////////////// 
/// rcsid="$Id$"
//////////////////////////////////////////////////////////////////////////// */

/* ///////////////////////////////////////////////////////////////////////////
// File:     nosh.h    
//
// Purpose:  No shell class (i.e., fixed format input files)
//
// Author:   Nathan Baker
/////////////////////////////////////////////////////////////////////////// */

#ifndef _NOSH_H_
#define _NOSH_H_

#define NOSH_MAXMOL 20
#define NOSH_MAXMGPARM 20
#define NOSH_MAXFEMPARM 20
#define NOSH_MAXCALC 20
#define NOSH_MAXPRINT 20
#define NOSH_MAXPOP 20

#include "apbs/apbs.h"
#include "maloc/maloc.h"
#include "apbs/femparm.h"
#include "apbs/mgparm.h"

/* ///////////////////////////////////////////////////////////////////////////
// Class NOsh: Definition
/////////////////////////////////////////////////////////////////////////// */

typedef struct NOsh {

    MGparm *mgparm[NOSH_MAXMGPARM];           /* Parameter objects for MG 
                                               * types of calculations */
    FEMparm *femparm[NOSH_MAXFEMPARM];        /* Parameter objects for FEM 
                                               * types of calculations */
    int ncalc;                                /* The number of calculations to 
                                               * be done */
    int imgcalc, ifemcalc, nmgcalc, nfemcalc; /* Counters for the various MG 
                                               * and FEM calculations */
    int calctype[NOSH_MAXCALC];               /* The list of calculations: 0 =>
                                               * multigrid and 1 => FEM */
    int nmol;                                 /* Number of molecules */
    char molpath[NOSH_MAXMOL][VMAX_ARGLEN];  /* Paths to mol files */
    int nprint;                               /* How many print sections? */
    int printwhat[NOSH_MAXPRINT];
                                              /* What do we print (0=>energy) */
    int printnarg[NOSH_MAXPRINT];             /* How many arguments in energy 
                                               * list */
    int printcalc[NOSH_MAXPRINT][NOSH_MAXPOP];/* Calculation id */
    int printop[NOSH_MAXPRINT][NOSH_MAXPOP];  /* Operation id (0 = add, 1 = 
                                               * subtract) */
  int parsed;                                 /* Have we parsed an input file
                                               * yet? */

} NOsh;

/* ///////////////////////////////////////////////////////////////////////////
// Class NOsh: Non-inlineable methods (mcsh.c)
/////////////////////////////////////////////////////////////////////////// */

VEXTERNC NOsh* NOsh_ctor();
VEXTERNC int   NOsh_ctor2(NOsh *thee);
VEXTERNC void  NOsh_dtor(NOsh **thee);
VEXTERNC void  NOsh_dtor2(NOsh *thee);
VEXTERNC int   NOsh_parse(NOsh *thee, Vio *sock);

#endif 

