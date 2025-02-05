#!/usr/bin/env python

# Capstone Python bindings
# BPF tests by david942j <david942j@gmail.com>, 2019

from capstone import *
from capstone.bpf import *
from xprint import to_hex, to_x, to_x_32


CBPF_CODE = b"\x94\x09\x00\x00\x37\x13\x03\x00\x87\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x16\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00"
EBPF_CODE = b"\x97\x09\x00\x00\x37\x13\x03\x00\xdc\x02\x00\x00\x20\x00\x00\x00\x30\x00\x00\x00\x00\x00\x00\x00\xdb\x3a\x00\x01\x00\x00\x00\x00\x84\x02\x00\x00\x00\x00\x00\x00\x6d\x33\x17\x02\x00\x00\x00\x00"

all_tests = (
        (CS_ARCH_BPF, CS_MODE_LITTLE_ENDIAN | CS_MODE_BPF_CLASSIC, CBPF_CODE, "cBPF Le", None),
        (CS_ARCH_BPF, CS_MODE_LITTLE_ENDIAN | CS_MODE_BPF_EXTENDED, EBPF_CODE, "eBPF Le", None),
        )

ext_name = {}
ext_name[BPF_EXT_LEN] = '#len'

def print_insn_detail(insn):
    # print address, mnemonic and operands
    print("0x%x:\t%s\t%s" % (insn.address, insn.mnemonic, insn.op_str))

    # "data" instruction generated by SKIPDATA option has no detail
    if insn.id == 0:
        return

    if len(insn.groups) > 0:
        print('\tGroups: ' + ' '.join(map(lambda g: insn.group_name(g), insn.groups)))

    print("\tOperand count: %u" % len(insn.operands))
    for c, op in enumerate(insn.operands):
        print("\t\toperands[%u].type: " % c, end='')
        if op.type == BPF_OP_REG:
            print("REG = " + insn.reg_name(op.reg))
        elif op.type == BPF_OP_IMM:
            print("IMM = 0x" + to_x(op.imm))
        elif op.type == BPF_OP_OFF:
            print("OFF = +0x" + to_x_32(op.off))
        elif op.type == BPF_OP_MEM:
            print("MEM")
            if op.mem.base != 0:
                print("\t\t\toperands[%u].mem.base: REG = %s" \
                    % (c, insn.reg_name(op.mem.base)))
            print("\t\t\toperands[%u].mem.disp: 0x%s" \
                % (c, to_x_32(op.mem.disp)))
        elif op.type == BPF_OP_MMEM:
            print("MMEM = 0x" + to_x_32(op.mmem))
        elif op.type == BPF_OP_MSH:
            print("MSH = 4*([0x%s]&0xf)" % to_x_32(op.msh))
        elif op.type == BPF_OP_EXT:
            print("EXT = " + ext_name[op.ext])

    (regs_read, regs_write) = insn.regs_access()

    if len(regs_read) > 0:
        print("\tRegisters read:", end="")
        for r in regs_read:
            print(" %s" % insn.reg_name(r), end="")
        print("")

    if len(regs_write) > 0:
        print("\tRegisters modified:", end="")
        for r in regs_write:
            print(" %s" % insn.reg_name(r), end="")
        print("")

def test_class():

    for (arch, mode, code, comment, syntax) in all_tests:
        print("*" * 16)
        print("Platform: %s" % comment)
        print("Code: %s" % to_hex(code))
        print("Disasm:")

        try:
            md = Cs(arch, mode)
            if syntax is not None:
                md.syntax = syntax
            md.detail = True
            for insn in md.disasm(code, 0x0):
                print_insn_detail(insn)
                print ()
        except CsError as e:
            print("ERROR: %s" % e)


if __name__ == '__main__':
    test_class()
