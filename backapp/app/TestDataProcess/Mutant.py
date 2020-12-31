class Mutant:
    # 可达特征
    NUMCOVERED = "nc"
    NUMTESTSCOVER = "numtc"
    NUM_ASSERT = "numAssert"
    CLASS_ASSERT = "classAssert"
    # 复杂度特征
    # method
    MMCOMP = "mmCOMP"
    MMNOCL = "mmNOCL"
    MMNOS = "mmNOS"
    MMHLTH = "mmHLTH"
    MMHVOV = "mmHVOC"
    MMHEFF = "mmHEFF"
    MMHBUG = "mmHBUG"
    MMCREF = "mmCREF"
    MMXMET = "mmXMET"
    MMLMET = "mmLMET"
    MMNLOC = "mmNLOC"
    MMNOC = "mmNOC"
    MMNOA = "mmNOA"
    MMMOD = "mmMOD"
    MMHDIF = "mmHDIF"
    MMVDEC = "mmVDEC"
    MMEXCT = "mmEXCT"
    MMEXCR = "mmEXCR"
    MMCAST = "mmCAST"
    MMTDN = "mmTDN"
    MMHVOL = "mmHVOL"
    MMNAND = "mmNAND"
    MMVREF = "mmVREF"
    MMNOPR = "mmNOPR"
    MMMDN = "mmMDN"
    MMNEXP = "mmNEXP"
    MMLOOP = "mmLOOP"
    # class
    CCNOMETHODS = "ccNoMethods"
    CCLCOM = "ccLCOM"
    CCAVCC = "ccAVCC"
    CCNOS = "ccNOS"
    CCHBUG = "ccHBUG"
    CCHEFF = "ccHEFF"
    CCUWCS = "ccUWCS"
    CCINST = "ccINST"
    CCPACK = "ccPACK"
    CCRFC = "ccRFC"
    CCCBO = "ccCBO"
    CCMI = "ccMI"
    CCCCML = "ccCCML"
    CCNLOC = "ccNLOC"
    CCRVF = "ccRVF"
    CCFIN = "ccF-IN"
    CCDIT = "ccDIT"
    CCMINC = "ccMINC"
    CCSR = "ccS-R"
    CCRR = "ccR-R"
    CCCOH = "ccCOH"
    CCLMC = "ccLMC"
    CCLCOM2 = "ccLCOM2"
    CCMAXCC = "ccMAXCC"
    CCHVOL = "ccHVOL"
    CCHIER = "ccHIER"
    CCNQU = "ccNQU"
    CCFOUT = "ccFOUT"
    CCSUPERCLASS = "ccSuperclass"
    CCSIX = "ccSIX"
    CCEXT = "ccEXT"
    CCNSUP = "ccNSUP"
    CCTCC = "ccTCC"
    CCNSUB = "ccNSUB"
    CCMPC = "ccMPC"
    CCNCO = "ccNCO"
    CCINTR = "ccINTR"
    CCCCOM = "ccCCOM"
    CCHLTH = "ccHLTH"
    CCMOD = "ccMOD"
    # package
    PPNOCLASSES = "ppNoClasses"
    PPNOS = "ppNOS"
    PPAVCC = "ppAVCC"
    PPHBUG = "ppHBUG"
    PPHEFF = "ppHEFF"
    PPHLTH = "ppHLTH"
    PPHVOL = "ppHVOL"
    PPMI = "ppMI"
    PPCCML = "ppCCML"
    PPNLOC = "ppNLOC"
    PPRVF = "ppRVF"
    PPTCC = "ppTCC"
    PPCCOM = "ppCCOM"
    PPINST = "ppINST"
    PPDIST = "ppDIST"
    PPFIN = "ppFIN"
    PPNOMETHODS = "ppNoMethods"
    PPMINC = "ppMINC"
    PPABST = "ppABST"
    PPMAXCC = "ppMAXCC"
    PPFOUT = "ppFOUT"
    # 充分特征
    OPERATOR = "operator"
    METHODRETURN = "method-return"
    FULLCLASS = "fullclass"
    FULLMETHOD = "fullmethod"
    ISKILLED = "isKilled"
    KILLTEST = "KillTest"
    ROWNUM = "rowNumber"
    KEY = "key"
    #所有特征
    FEATURES = [NUMCOVERED,NUMTESTSCOVER, NUM_ASSERT, CLASS_ASSERT,
                MMCOMP, MMNOCL, MMNOS, MMHLTH, MMHVOV, MMHEFF, MMHBUG, MMCREF,MMXMET, MMLMET, MMNLOC, MMNOC,MMNOA, MMMOD,
                MMHDIF, MMVDEC, MMEXCT, MMEXCR, MMCAST, MMTDN, MMHVOL, MMNAND, MMVREF, MMNOPR, MMMDN,MMNEXP, MMLOOP,
                CCNOMETHODS, CCLCOM, CCAVCC, CCNOS, CCHBUG,CCHEFF, CCUWCS, CCINST, CCPACK, CCRFC, CCCBO, CCMI, CCCCML,
                CCNLOC, CCRVF, CCFIN, CCDIT, CCMINC, CCSR,CCRR, CCCOH, CCLMC, CCLCOM2, CCMAXCC, CCHVOL, CCHIER, CCNQU,
                CCFOUT, CCSUPERCLASS, CCSIX, CCEXT, CCNSUP, CCTCC, CCNSUB, CCMPC, CCNCO, CCINTR, CCCCOM, CCHLTH, CCMOD,
                PPNOCLASSES, PPNOS, PPAVCC, PPHBUG, PPHEFF, PPHLTH, PPHVOL,PPMI, PPCCML, PPNLOC, PPRVF, PPTCC, PPCCOM,
                PPINST, PPDIST, PPFIN, PPNOMETHODS, PPMINC, PPABST, PPMAXCC,PPFOUT,
                OPERATOR, METHODRETURN, ISKILLED, KILLTEST, ROWNUM, FULLCLASS, FULLMETHOD, KEY]

    def __init__(self, fullname=None,lineNumber=None,javaFileName=None,methodName=None,status=None):
        self.fullname=fullname
        self.lineNumber=lineNumber
        self.javaFileName=javaFileName
        self.methodName=methodName
        self.status=status
    
    def toString(self):
        return self.fullname+":"+self.methodName+":"+self.lineNumber

mutant=Mutant()
