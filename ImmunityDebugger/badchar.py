__author__ = 'miao'

from immlib import *

def main(args):
    imm = Debugger()

    bad_char_found = False

    address = int(args[0],16)

    shellcode = "<<COPY AND PASTE YOUR SHELLCODE HERE>>"
    shellcode_length = len(shellcode)

    debug_shellcode = imm.readMemory(address,shellcode_length)
    debug_shellcode = debug_shellcode.encode("HEX")

    imm.log("Address: 0x%08x" %address)
    imm.log("Shellcode Length : %d" %shellcode_length)

    imm.log("Attack Shellcode: %s" %shellcode[:shellcode_length])
    imm.log("In Memory Shellcode: %s" %debug_shellcode[:shellcode_length])

    count = 0
    while count <= shellcode_length:
        if debug_shellcode[count] != shellcode[count]:
            imm.log("Bad Char Detected at offset %d" %count)
            bad_char_found = True
            break

        count += 1

    if bad_char_found:
        imm.log("[*****] ")
        imm.log("Bad character found: %s" %debug_shellcode[count])
        imm.log("Bad character original: %s" %shellcode[count])
        imm.log("[*****] ")

    return "[*] !badchar finished,check Log window."
