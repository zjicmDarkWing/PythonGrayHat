__author__ = 'DarkWing'

from idaapi import *

class FuncCoverage(DBG_Hooks):
    def dbg_bpt(self,tis,ea):
        print "[*] Hit: 0x%08x" %ea
        return 1

debugger = FuncCoverage()
debugger.hook()

current_addr = ScreenEA()

for function in Functions(SegStart(current_addr),SegEnd(current_addr)):
    AddBpt(function)
    SetBptAddr(function,BPTATTR_FLAGS,0x0)

num_breakpoints = GetBptQty()

print "[*] Set %d breakpoints." %num_breakpoints
