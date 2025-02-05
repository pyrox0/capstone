#!/usr/bin/env python

# Capstone Python bindings, by Peace-Maker <peacemakerctf@gmail.com>

from capstone import *
from capstone.wasm import *
from xprint import to_hex

WASM_CODE = b"\x20\x00\x20\x01\x41\x20\x10\xc9\x01\x45\x0b"

all_tests = (
    (CS_ARCH_WASM, 0, WASM_CODE, "WASM"),
)


def print_insn_detail(insn):
    # print address, mnemonic and operands
    print("0x%x:\t%s\t%s" % (insn.address, insn.mnemonic, insn.op_str))

    # "data" instruction generated by SKIPDATA option has no detail
    if insn.id == 0:
        return

    if len(insn.groups) > 0:
        print("\tGroups: ", end="")
        for group in insn.groups:
            print("%s " % insn.group_name(group), end="")
        print()

    if len(insn.operands) > 0:
        print("\tOperand count: %u" % len(insn.operands))
        c = 0
        for i in insn.operands:
            if i.type == WASM_OP_INT7:
                print("\t\tOperand[%u] type: int7" % c)
                print("\t\tOperand[%u] value: %d" % (c, i.int7))
            elif i.type == WASM_OP_VARUINT32:
                print("\t\tOperand[%u] type: varuint32" % c)
                print("\t\tOperand[%u] value: %#x" % (c, i.varuint32))
            elif i.type == WASM_OP_VARUINT64:
                print("\t\tOperand[%u] type: varuint64" % c)
                print("\t\tOperand[%u] value: %#x" % (c, i.varuint64))
            elif i.type == WASM_OP_UINT32:
                print("\t\tOperand[%u] type: uint32" % c)
                print("\t\tOperand[%u] value: %#x" % (c, i.uint32))
            elif i.type == WASM_OP_UINT64:
                print("\t\tOperand[%u] type: uint64" % c)
                print("\t\tOperand[%u] value: %#x" % (c, i.uint64))
            elif i.type == WASM_OP_IMM:
                print("\t\tOperand[%u] type: imm" % c)
                print("\t\tOperand[%u] value: %#x %#x" % (c, i.immediate[0], i.immediate[1]))
            elif i.type == WASM_OP_BRTABLE:
                print("\t\tOperand[%u] type: brtable" % c)
                print("\t\tOperand[%u] value: length=%#x, address=%#x, default_target=%#x" % (c, i.brtable.length, i.brtable.address, i.brtable.default_target))
            print("\t\tOperand[%u] size: %u" % (c, i.size))
            c += 1
        


# ## Test class Cs
def test_class():
    for (arch, mode, code, comment) in all_tests:
        print("*" * 16)
        print("Platform: %s" % comment)
        print("Code: %s" % to_hex(code))
        print("Disasm:")

        try:
            md = Cs(arch, mode)
            md.detail = True
            for insn in md.disasm(code, 0xffff):
                print_insn_detail(insn)
                print()
            print("0x%x:\n" % (insn.address + insn.size))
        except CsError as e:
            print("ERROR: %s" % e)


if __name__ == '__main__':
    test_class()
