__author__ = 'miao'

import struct
import random
from immlib import *

class ioctl_hook(LogBpHook):
    def __init__(self):
        self.imm = Debugger()
        delf.logfile = "C:\ioctl_log.txt"
        LogBpHook.__init__(self)

    def run(self,regs):
        in_buf = ""

        ioctl_code = self.imm.readLong(regs["ESP"]+8)

        inbuffer_size = self.imm.readMemory(regs["ESP"]+0x10,4)
        inbuffer_size = struct.unpack( "<L", inbuffer_size )[0]

        inbuffer_ptr = self.imm.readMemory(regs["ESP"]+0xC,4)
        inbuffer_ptr  = int(struct.unpack("<L", inbuffer_ptr)[0])

        in_buffer = str(self.imm.readMemory(inbuffer_ptr,inbuffer_size).encode("HEX"))
        mutated_buffer = self.mutate(inbuffer_size)

        self.imm.writeMemory(inbuffer_ptr, mutated_buffer)

        self.save_test_case(ioctl_code,in_buffer,mutated_buffer)

    def mutate(self,inbuffer_size):
        counter = 0
        mutated_buffer = ""

        while counter < inbuffer_size:
            mutated_buffer += struct.pack("H", random.randint(0, 255))[0]
            counter += 1

        return mutated_buffer

    def save_test_case(self,ioctl_code,in_buffer,mutated_buffer):
        message  = "*****\n"
        message += "IOCTL Code:      0x%08x\n" % ioctl_code
        message += "Original Buffer: %s\n" % in_buffer
        message += "Mutated Buffer:  %s\n" % mutated_buffer.encode("HEX")
        message += "*****\n\n"

        fd = open(self.logfile, "a")
        fd.write(message)
        fd.close()

def main():
    imm = Debugger()

    deviceiocontrol = imm.getAddress("kernel32.DeviceIoControl")

    ioctl_hooker = ioctl_hook()
    ioctl_hooker.add( "%08x" % deviceiocontrol, deviceiocontrol )

    return "[*] IOCTL Fuzzer Ready for Action!"
