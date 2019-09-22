#!/usr/bin/python
import sys
import copy


def symbol_table(file):
    stack = [{}]

    try:
        file = open(file, 'r')

        for line in file:

            # for automarker
            if line.endswith('\n'):
                line = line[:-1]

            use = False
            # symbol table is equal to top of stack (starts empty)
            s_table = stack[-1]

            # start of a scope: top of stack must include table with declared variables inside of scope
            if "beginscope" in line:
                # needs to be a deep copy to work
                s_table = copy.deepcopy(s_table)
                stack.append(s_table)

            # gives a variable a value + adds this relationship to symbol table
            elif "define" in line:
                _, var, val = line.split(" ")
                # adds variable and associated value to symbol table (use dict as hash map)
                s_table[var] = val

            # if a variable is being used inside of a scope
            elif "use" in line:
                _, var = line.split(" ")

                # if symbol has been defined
                if var in s_table:
                    # value is equal to its associated defined variable
                    val = s_table[var]
                else:
                    # if no variable exists within the scope, val is undefined
                    val = "undefined"

                print("use " + var + " = " + val)
                use = True

            # end of scope: symbol table with declared variable, value relationships for relevant scope deleted
            elif "endscope" in line:
                stack.pop()

            if not use:
                print(line)

    except IOError as e:
        print(e)
    finally:
        file.close()


if __name__ == '__main__':
    symbol_table(sys.argv[1])
