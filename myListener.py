from AutolevListener import AutolevListener

import sys
from antlr4 import *
from antlr4.InputStream import InputStream

#       Mathematical Entities
# Constants ✓
# Variables ✓
# Imaginary ✓
# MotionVariables ✓
# Specifieds ✓
# Expression reconstruction
# Assignments
# Math commands and expressions
# Reserved names and constants (T, Pi etc)
# Matrices

def writeConstants(self, ctx):
    l1 = list(filter(lambda x: self.sign[x] == "o",self.varList))
    l2 = list(filter(lambda x: self.sign[x] == "+",self.varList))
    l3 = list(filter(lambda x: self.sign[x] == "-",self.varList))
    if(l1):
        a = ", ".join(l1)+"="+"sm.symbols(" + "'" + \
        " ".join(l1) + "', real=True)\n"
        self.file.write(a)
    if(l2):
        a = ", ".join(l2)+"="+"sm.symbols(" + "'" + \
        " ".join(l2) + "', real=True, nonnegative=True)\n"
        self.file.write(a)
    if(l3):
        a = ", ".join(l3)+"="+"sm.symbols(" + "'" + \
        " ".join(l3) + "', real=True, nonpositive=True)\n"
        self.file.write(a)
    self.varList = []
def processConstants(self, ctx):

    # Process constant declarations of the type: Constants F = 3, g = 9.81
    if(ctx.getChildCount()==3):
        # Check whether the value is a float or an int
        if "." in ctx.getChild(2).getText():
            a = float(ctx.getChild(2).getText())
        else: a = int(ctx.getChild(2).getText())

        # Populate the symbol table
        self.symbol_table[str(ctx.ID().getText())] = (str(ctx.ID().getText()).lower(), a)

        # Set the type
        self.type[str(ctx.ID().getText())] = "constants"

    else: # Constants declarations of the type: Constants A, B
        if ctx.getChildCount()==1 or (ctx.getChildCount()>1 and ctx.getChild(1).getText() != "{"):
            #symbol table
            self.symbol_table[str(ctx.ID().getText())] = str(ctx.ID().getText()).lower()
            #type
            self.type[str(ctx.ID().getText())] = "constants"

    # Process constant declarations of the type: Constants C+, D-
    if ctx.getChildCount()==2:
        if(ctx.getChild(1).getText()=="+"):
            self.sign[str(ctx.ID().getText()).lower()] = "+"    
        elif(ctx.getChild(1).getText()=="-"):
            self.sign[str(ctx.ID().getText()).lower()] = "-"
    else:
        if ctx.getChildCount()==1 or (ctx.getChildCount()>1 and ctx.getChild(1).getText() != "{"):
            self.sign[str(ctx.ID().getText()).lower()] = "o"

    # Process constant declarations of the type: Constants K{4}, a{1:2, 1:2}, b{1:2}
    if(ctx.getChildCount()>2 and ctx.getChild(1).getText() == "{"):
        if ctx.getChild(3).getText() == ":":
            num1 = int(ctx.getChild(2).getText())
            num2 = int(ctx.getChild(4).getText()) + 1
        else:
            num1 = 1
            num2 = int(ctx.getChild(2).getText()) + 1
            
        if ctx.getChild(3).getText() == ":":
            if ctx.getChildCount()==10:
                num3 = int(ctx.getChild(6).getText())
                num4 = int(ctx.getChild(8).getText())+1
                for i in range(num1, num2):
                    for j in range(num3, num4):
                        # symbol_table
                        self.symbol_table[str(ctx.ID().getText()) + str(i) + str(j)] = \
                        str(ctx.ID().getText() + str(i) + str(j)).lower()
                        #type
                        self.type[str(ctx.ID().getText()) + str(i) + str(j)] = "constants"
                        # varList
                        self.varList.append(str(ctx.ID().getText()).lower() + str(i) + str(j))
                        # sign
                        self.sign[str(ctx.ID().getText()).lower() + str(i) + str(j)] = "o"
            for i in range(num1, num2):
                # symbol_table
                self.symbol_table[str(ctx.ID().getText()) + str(i)] = \
                str(ctx.ID().getText() + str(i)).lower()
                #type
                self.type[str(ctx.ID().getText()) + str(i)] = "constants"
                # varList
                self.varList.append(str(ctx.ID().getText()).lower() + str(i))
                # sign
                self.sign[str(ctx.ID().getText()).lower() + str(i)] = "o"

        else:
            for i in range(num1, num2):
                # symbol_table
                self.symbol_table[str(ctx.ID().getText()) + str(i)] = \
                str(ctx.ID().getText() + str(i)).lower()
                #type
                self.type[str(ctx.ID().getText()) + str(i)] = "constants"
                # varList
                self.varList.append(str(ctx.ID().getText()).lower() + str(i))
                # sign
                self.sign[str(ctx.ID().getText()).lower() + str(i)] = "o"
    if ctx.getChildCount()==1 or (ctx.getChildCount()>1 and ctx.getChild(1).getText() != "{"):
        self.varList.append(str(ctx.ID().getText()).lower())
def writeVariables(self, ctx):
    for i in range(self.maxDegree+1):
        if i==0:
            j = ""
            t = ""
        else:
            j = str(i)
            t = ", "
        l = []
        for k in list(filter(lambda x: self.sign[x] == i,self.varList)):
            if i==0: l.append(k)
            if i==1: l.append(k[:-1])
            if i>1:  l.append(k[:-2])
        a = ", ".join(list(filter(lambda x: self.sign[x] == i,self.varList)))+" = "+"me.dynamicsymbols(" + "'" + \
        " ".join(l) + "'"+ t + j+")\n"
        l = []
        self.file.write(a)
    self.maxDegree = 0
    self.varList = []
def processVariables(self, ctx):
    # Process variables of the type: Variables qA, qB
    if(ctx.getChildCount()==1):
        self.maxDegree = 0
        # symbolTable
        self.symbol_table[str(ctx.ID().getText())] = \
        str(ctx.ID().getText()).lower()
        # type
        if self.tree_property[ctx.parentCtx.getChild(0)].lower() == "variables":
            self.type[str(ctx.ID().getText())] = "variables"
        elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables":
            self.type[str(ctx.ID().getText())] = "motionvariables"
        elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables'":
            self.type[str(ctx.ID().getText())] = "motionvariables'"
        elif self.tree_property[ctx.parentCtx.getChild(0)].lower() in ["specifieds","specified"]:
            self.type[str(ctx.ID().getText())] = "specified"
        
        # varList
        self.varList.append(str(ctx.ID().getText()).lower())
        # sign (here the order of the derivative)
        self.sign[str(ctx.ID().getText()).lower()] = 0
    
    # Process variables of the type: Variables x', y''
    elif(ctx.getChildCount()>1 and ctx.getChild(1).getText() != "{"):
        if(ctx.getChildCount() - 1) > self.maxDegree:
            self.maxDegree = ctx.getChildCount() - 1
        for i in range(ctx.getChildCount()):
            if i==0:
                 j = ""
            elif i==1:
                 j = "d"
            else:
                j = "d" + str(i)
            
            self.sign[str(ctx.ID().getText()).lower() + str(j)] = i
            
            # symbolTable
            self.symbol_table[str(ctx.ID().getText()) + "'"*i] = \
            str(ctx.ID().getText()).lower() + str(j)
            # type
            if self.tree_property[ctx.parentCtx.getChild(0)].lower() == "variables":
                self.type[str(ctx.ID().getText()) + "'"*i] = "variables"
            elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables":
                self.type[str(ctx.ID().getText()) + "'"*i] = "motionvariables"
            elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables'":
                self.type[str(ctx.ID().getText()) + "'"*i] = "motionvariables'"
            elif self.tree_property[ctx.parentCtx.getChild(0)].lower() in ["specifieds","specified"]:
                self.type[str(ctx.ID().getText())] = "specified"
            # varList
            self.varList.append(str(ctx.ID().getText()).lower() + str(j))
    

    elif ctx.getChildCount()>1 and ctx.getChild(1).getText() == "{":
        # Process variables of the type: Variales y{3}', y{2}''
        if ctx.getChildCount() > 4 and ctx.getChild(4).getText() == "'":

            dashCount = ctx.getChildCount() - 4
            if(dashCount) > self.maxDegree:
                self.maxDegree = dashCount

            for i in range(dashCount+1):
                if i==0:
                    j = ""
                elif i==1:
                    j = "d"
                else:
                    j = "d" + str(i)
                num = int(ctx.getChild(2).getText())
                for z in range(1, num+1):
                    self.sign[str(ctx.ID().getText()).lower() + str(z) + str(j)] = i
                    # symbolTable
                    self.symbol_table[str(ctx.ID().getText()) + str(z) + "'"*i] = \
                    str(ctx.ID().getText()).lower() + str(z) + str(j)
                    # type
                    if self.tree_property[ctx.parentCtx.getChild(0)].lower() == "variables":
                        self.type[str(ctx.ID().getText()) + str(z) + "'"*i] = "variables"
                    elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables":
                        self.type[str(ctx.ID().getText()) + str(z) + "'"*i] = "motionvariables"
                    elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables'":
                        self.type[str(ctx.ID().getText()) + str(z) + "'"*i] = "motionvariables'"
                    elif self.tree_property[ctx.parentCtx.getChild(0)].lower() in ["specifieds","specified"]:
                        self.type[str(ctx.ID().getText())] = "specified"
                    # varList
                    self.varList.append(str(ctx.ID().getText()).lower() + str(z) + str(j))
            if(dashCount) > self.maxDegree:
                self.maxDegree = dashCount

        # Process variables of the type: Variales x{3}, y{2}
        else:
            self.maxDegree = 0
            num = int(ctx.getChild(2).getText())
            for i in range(1, num+1):
                self.symbol_table[str(ctx.ID().getText()) + str(i)] = \
                str(ctx.ID().getText()).lower() + str(i)
                 # type
                if self.tree_property[ctx.parentCtx.getChild(0)].lower() == "variables":
                    self.type[str(ctx.ID().getText()) + str(i)] = "variables"
                elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables":
                    self.type[str(ctx.ID().getText()) + str(i)] = "motionvariables"
                elif self.tree_property[ctx.parentCtx.getChild(0)].lower() == "motionvariables'":
                    self.type[str(ctx.ID().getText()) + str(i)] = "motionvariables'"
                elif self.tree_property[ctx.parentCtx.getChild(0)].lower() in ["specifieds","specified"]:
                    self.type[str(ctx.ID().getText())] = "specified"
                # varList
                self.varList.append(str(ctx.ID().getText()).lower() + str(i))
                #sign
                self.sign[str(ctx.ID().getText()).lower() + str(i)] = 0
def writeImaginary(self, ctx):
    a = ", ".join(self.varList)+"="+"sm.symbols(" + "'" + \
        " ".join(self.varList) + "')\n"
    b = ", ".join(self.varList)+"="+"sm.I\n"
    self.file.write(a+b)
    self.varList = []
def processImaginary(self, ctx):
    # symbol_table
    self.symbol_table[str(ctx.ID().getText())] = \
    str(ctx.ID().getText()).lower()
    # type
    self.type[str(ctx.ID().getText())] = "imaginary"
    # varList
    self.varList.append(str(ctx.ID().getText()).lower())

class myListener(AutolevListener):
    def __init__(self):
        # Used for tree annotation. Especially useful for expr reconstruction.
        self.tree_property = {}

        # Stores the declared variables, constants etc in the format
        # {"<Autolev symbol>": "<SymPy symbol>"}.
        self.symbol_table = {}

        # Used to store nonpositive, nonnegative etc for constants and number of "'"s
        # in variables.
        self.sign = {}

        # Simple used as a store to pass around variables between the 'process' and 'write'
        # methods.
        self.varList = []

        # Stores the type of a declared variable (constants, variables, specifieds etc)
        self.type = {}

        # The output file to which the SymPy code will be written to.
        self.file = open("output1.txt", "w")
        self.file.write("import sympy.physics.mechanics as me\nimport sympy as sm\n\n")

        # Just a store for the max degree variable in a line.
        self.maxDegree = 0

    def getValue(self, node):
        return self.tree_property[node]

    def setValue(self, node, value):
        self.tree_property[node] = value

    def getSymbolTable(self):
        return self.symbol_table

    def enterVarDecl(self, ctx):
        pass
    def exitVarDecl(self, ctx):
        """This method looks at the leftmost child to determine the type of the
        declaration and then calls the appropriate write method.
        The processing for these is done beforehand in the process methods
        as exitVarDecl2 is called before exitVarDecl (have a look at the parse trees)."""

        if (self.tree_property[ctx.getChild(0)]).lower() == "constants":
            writeConstants(self, ctx)
        elif (self.tree_property[ctx.getChild(0)]).lower() in \
        ["variables", "motionvariables", "motionvariables'", "specifieds", "specified"]:
            writeVariables(self, ctx)
        elif (self.tree_property[ctx.getChild(0)]).lower() == "imaginary":
            writeImaginary(self, ctx)

    def enterVarType(self, ctx):
        pass
    def exitVarType(self ,ctx):
        self.tree_property[ctx] = ctx.getChild(0).getText()
    def enterVarDecl2(self, ctx):
        pass
    def exitVarDecl2(self, ctx):
        """This method calls the appropriate process methods. These methods process the
        variables and store appropriate information in the class lists and dictionaries.
        This information is then used to write to the output file in the write methods."""
        if (self.tree_property[ctx.parentCtx.getChild(0)]).lower() == "constants":
            processConstants(self, ctx)
        elif (self.tree_property[ctx.parentCtx.getChild(0)]).lower() in \
        ["variables", "motionvariables", "motionvariables'", "specifieds", "specified"]:
            processVariables(self, ctx)
        elif (self.tree_property[ctx.parentCtx.getChild(0)]).lower() == "imaginary":
            processImaginary(self, ctx)