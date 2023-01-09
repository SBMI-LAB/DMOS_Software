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
    
    baseAddress = "0123456789abcdefghijklmnopqrstuv"
    
    

    def decodeAddress(self, strAddress):
        base = 32
        
        if len(strAddress) != base:
            print("Address length error")
            return -1
        
        address = []
        for H in strAddress:
            address.append( self.baseAddress.index(H) )
        
        numbers = []
        for k in range(0,base):
            numbers.append(k)
        n=base
        
        Nm = 0
        
        
        
        for i in range(1,n+1):
            
            if numbers[0] == address[0]:
                numbers.remove(numbers[0])
                address.remove(address[0])
            else:
                nadd = address[0]
                ind = numbers.index(nadd)
                
                factor = math.factorial(n-i) * (ind)
                Nm += factor
                
                numbers.remove(nadd)
                address.remove(nadd)
                
        return Nm
    

    def encodeAddress(self,number):
        bnumber=format(number, '#044b')[2:]
                       
        base = 32
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
                perNum += self.baseAddress[numbers[j]]
                numbers.remove(numbers[j])
#                Nm =  abs(math.remainder(Nm, math.factorial (n-i)))
#                Nm =  math.remainder(Nm, math.factorial (n-i))
                Nm = Nm % math.factorial (n-i)
            else:
                try:
                    perNum += self.baseAddress[numbers[j]]
                    numbers.remove(numbers[j])
                except:
                    None
        
#        print(bnumber)        
        return perNum
    
        
    
    def loadDomains(self):
        
        workbook = xlrd.open_workbook("Domains32.xlsx")

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


OutFile = open("Templates32.txt", "w")

for k in range(64):
    temp, addr = tgen.buildTemplate(k, "NoExtra")  #Use "NoExtra" for shorter sequences# 
    OutFile.write(str(k)+": " + addr+"\n"+temp+"\n")


OutFile.close()





### Test addresses
# for k in range(64):
#     addrStr = tgen.encodeAddress(k)
    
#     deAdd = tgen.decodeAddress(addrStr)
    
#     if deAdd == k:
#         print('Ok')
#     else:
#         print('fail')
