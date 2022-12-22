from math import ceil
from aoc_python.common.utils import get_day_n_input
from aoc_python.d20.decrypt import decrypt
# from functools import cache

TEST_DATA = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines()

def main():
    data = TEST_DATA
    # data = get_day_n_input(21)
    lookup_table = {k: _parse_job(v) for k,v in [line.split(":") for line in data]}
    print(get_root(lookup_table))
    print(get_needed_human_shout(lookup_table))

from operator import mul, add, sub, floordiv
op_table = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": floordiv,
}

inverse_op_table = {
    "+": "-",
    "-": "+",
    "*": "/",
    "/": "*",
}

def has_child(monkey, target, table):
    if monkey == target:
        return {monkey: True}
    if len(table[monkey]) == 1:
        return {monkey: False}

    tokens = table[monkey]
    arg1, _, arg2 = tokens

    try:
        int(arg1)
        left = {}
    except ValueError:
        left = has_child(arg1, target, table)

    try:
        int(arg2)
        right = {}
    except ValueError:
        right = has_child(arg2, target, table)

    # left = has_child(arg1, target, table)
    # right = has_child(arg2, target, table)
    res = left | right
    # res = {**left, **right}
    res[monkey] = res[arg1] or res[arg2]
    return res


def get_needed_human_shout(lookup_table):
    cache = {}
    operation_seq = []
    def get_val(monkey, has_child):
        # if monkey == "humn":
            # print("HUMAN:", lookup_table[monkey])
            # breakpoint()
        if monkey in cache:
            return cache[monkey]

        tokens = lookup_table[monkey]
        if len(tokens) == 1:
            if not monkey == "humn":
                cache[monkey] = int(tokens[0])
            return int(tokens[0])

        ancestor = None
        arg1, op, arg2 = tokens
        try:
            arg1 = int(arg1)
        except ValueError:
            val = get_val(arg1, has_child)
            if has_child[arg1]:
                ancestor = "arg1"
            else:
                cache[arg1] = val
            arg1 = val

        try:
            arg2 = int(arg2)
        except ValueError:
            val = get_val(arg2, has_child)
            if has_child[arg2]:
                ancestor = "arg2"
            else:
                cache[arg2] = val
            arg2 = val
        
        # print(f"{arg1} {op} {arg2}")
        operation_seq.append((arg1, op, arg2, ancestor))
        return op_table[op](arg1, arg2)

    has_child_table = has_child("root", "humn", lookup_table)
    val = get_val("root", has_child_table)
    operation_seq = []
    val = get_val("root", has_child_table)

    # print("VAL:", val)
    target = 0
    for x in reversed(operation_seq):
        print("target:", target)
        print("line:", x)
        # breakpoint()
        arg1, op, arg2, ancestor = x
        target = op_table[inverse_op_table[op]](target, arg2 if ancestor == "arg1" else arg1)
        # arg1, op, arg2, ancestor = x
        # if op == "+":
        #     target -= arg2 if ancestor == "arg1" else arg1
        # elif op == "-":
        #     target += arg2 if ancestor == "arg1" else arg1
        # elif op == "*":
        #     target //= arg2 if ancestor == "arg1" else arg1
        #     target_old = target
        #     target = ceil(target)
        #     if target != target_old:
        #         RuntimeError("Oops")

        # elif op == "/":
        #     if ancestor == "arg1":
        #         target *= arg2 if ancestor == "arg1" else arg1
        #     else:
        #         raise RuntimeError("OOPS")
        # else:
        #     raise RuntimeError("OOPS")

    return target



def get_root(lookup_table):
    def get_val(monkey):
        tokens = lookup_table[monkey]
        if len(tokens) == 1:
            return int(tokens[0])

        arg1, op, arg2 = tokens
        try:
            arg1 = int(arg1)
        except ValueError:
            arg1 = get_val(arg1)

        try:
            arg2 = int(arg2)
        except ValueError:
            arg2 = get_val(arg2)
        
        return op_table[op](arg1, arg2)
    
    return get_val("root")

def _parse_job(s: str):
    tokens = s.strip().split(" ")
    return tokens

main()
