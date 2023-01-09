# -*- coding: utf-8 -*-

import xlrd
import math


class DMOS_TemplateGen:

    domains = []

    initiator = ""
    terminator = ""
    
    extraBefore = ""
    extraAfter = ""
    
    addExtra = False
    
    extraFlag = False
    
    baseAddress = "0123456789abcdef"
    
    
    

    def encodeAddress(self,number):
        bnumber=format(number, '#044b')[2:]
                       
        base = 16
        numbers = []
        for k in range(0,base):
            numbers.append(k)
        n=base
        Nm = number
        S= []
        perNum = ""
        for i in range(1,n+1):
            j = math.floor( Nm / math.factorial(n-i) )
            
            # Kn =  math.remainder(Nm, math.factorial (n-i))
            Kn =  Nm % math.factorial (n-i)
#            print (i, j, n-i, math.factorial(n-i), Kn, Nm)
            if j > 0:
                perNum += hex(numbers[j])[2:]
                numbers.remove(numbers[j])
#                Nm =  abs(math.remainder(Nm, math.factorial (n-i)))
#                Nm =  math.remainder(Nm, math.factorial (n-i))
                Nm = Nm % math.factorial (n-i)
            else:
                perNum += hex(numbers[j])[2:]
                numbers.remove(numbers[j])
        
#        print(bnumber)        
        return perNum
    
        
    
    def loadDomains(self):
        
        workbook = xlrd.open_workbook("Domains.xlsx")

        sh = workbook.sheet_by_name("Domains")
        for rownum in range(0,sh.nrows):
            row_valaues = sh.row_values(rownum)
            self.domains.append(row_valaues[0])
                
        sh = workbook.sheet_by_name("Primers")
        row_values = sh.row_values(1)
        self.initiator = row_values[0]
        self.terminator= row_values[1]
        
        sh = workbook.sheet_by_name("Extra")
        row_values = sh.row_values(1)
        self.extraBefore = row_values[0]
        self.extraAfter= row_values[1]
    
    
    def concatExtra(self, Template):
        
        if self.addExtra:
            if self.extraFlag:
                Template.append(self.extraBefore)
                self.extraFlag = False
            else:
                Template.append(self.extraAfter)
                self.extraFlag = True
    
    
    def buildTemplate(self,address, extra = "Extra"):
        
        if extra == "Extra":
            self.addExtra = True
            self.extraFlag = True
        else:
            self.addExtra = False
        
        addr = self.encodeAddress(address)        
        print(addr)

        
        ## Encoding address
        
        Template = []
        
        
        self.concatExtra(Template) ## Add extra  nucleotides
        Template.append(self.initiator)
        self.concatExtra(Template) ## Add extra  nucleotides
        
        
        for c in addr:
            ind = self.baseAddress.index(c)
            self.concatExtra(Template) ## Add extra  nucleotides
            Template.append( self.domains[ind] )
            self.concatExtra(Template) ## Add extra  nucleotides
            
        self.concatExtra(Template) ## Add extra  nucleotides    
        Template.append(self.terminator)
        self.concatExtra(Template) ## Add extra  nucleotides
        
        Template = ''.join(Template)
        
        return Template, addr
            
        
        
        


tgen = DMOS_TemplateGen()
tgen.loadDomains()


OutFile = open("Templates.txt", "w")

for k in range(32):
    temp, addr = tgen.buildTemplate(k, "NoExtra")  #Use "NoExtra" for shorter sequences# 
    OutFile.write(str(k)+": " + addr+"\n"+temp+"\n")


OutFile.close()


