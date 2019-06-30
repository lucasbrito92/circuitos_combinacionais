import re
import time
import itertools
import numpy as np
from tt import BooleanExpression, TruthTable, to_primitives
from prettytable import PrettyTable


def translate_circuit(data):
    """ From the description of a circuit with failure, the aim
    circuit reads p0/p1 as a working gate, whereas failure version
    of circuit, not. return: both circuits, ttable from expr """

    table_fails = []
    for line in range(len(data)):

        """ test if exists p0 and p1, p1 not p0, p0 not p1 """
        if (data[line].find('p0') != -1) and (data[line].find('p1') != -1):
            expr_fails = data[line].replace('p0', '0')
            expr_fails = expr_fails.replace('p1', '1')

            in_out_expr = expr_fails.split('=')
            table_fails = TruthTable(in_out_expr[1])

            data.append(expr_fails)

        if (data[line].find('p1') != -1) and (data[line].find('p0') < 0):
            expr_fails = data[line].replace('p1', '1')

            in_out_expr = expr_fails.split('=')
            table_fails = TruthTable(in_out_expr[1])

            data.append(expr_fails)

        if (data[line].find('p0') != -1) and (data[line].find('p1') < 0):
            expr_fails = data[line].replace('p0', '0')

            in_out_expr = expr_fails.split('=')
            table_fails = TruthTable(in_out_expr[1])

            data.append(expr_fails)

    return data, table_fails


def find_occurrences(s, ch):
    """ Return positions of char occurrences in a given string """
    return [i for i, letter in enumerate(s) if letter == ch]


def diag_fail_circuit(logic_exp, table_fails):

    newtime = time.time()
    outputs = []
    for line in logic_exp:

        data = line.split('=')
        outputs.append(data[0])
        data.pop(0)

        expr = data[0].replace('p0', 'Z')
        expr = expr.replace('p1', 'Z')
        newexpr = BooleanExpression(expr)

        with open('diag53.txt', 'w') as myfile:
            myfile.write(
                "Circuit Analysis: {} \n\n".format(outputs[0]+'='+data[0]))
            for s in newexpr.symbols:
                ocrr = find_occurrences(expr, s)
                for o in ocrr:
                    templist = list(''.join(expr))
                    templist[o] = '1'
                    finalExpr = ''.join(templist)
                    tempTruth = TruthTable(finalExpr)

                    if (len(table_fails.results) == (len(tempTruth.results))):
                        if table_fails.equivalent_to(tempTruth):
                            finalExpr = finalExpr.replace('Z', 'XX')
                            finalExpr = finalExpr.replace('1', 'PortaPresaEm1')
                            myfile.write(
                                "-> Possible fail: {}\n".format(finalExpr))

                    print("Expr: {}\n {} \n Fail: {}\n".format(
                        finalExpr, tempTruth, table_fails))

                    templist = list(''.join(expr))
                    templist[o] = '0'
                    finalExpr = ''.join(templist)
                    tempTruth = TruthTable(finalExpr)

                    if (len(table_fails.results) == (len(tempTruth.results))):
                        if table_fails.equivalent_to(tempTruth):
                            finalExpr = finalExpr.replace('Z', 'XX')
                            finalExpr = finalExpr.replace('0', 'PortaPresaEm0')
                            myfile.write(
                                "-> Possible fail: {}\n".format(finalExpr))

                    print("Expr: {}\n {} \n Fail: {}\n".format(
                        finalExpr, tempTruth, table_fails))

            myfile.write("\n\nTime elapsed: {} secs.".format(
                time.time() - newtime))
            myfile.close()

    # print(outputs)


if __name__ == "__main__":

    start_time = time.time()
    results, inputs, outputs, matrix, pts = [], [], [], [], []

    with open("input53.txt", 'r') as myfile:
        data = myfile.read().strip()
        myfile.close()
    data = data.split('\n')
    originalData = data.copy()

    new_data, table = translate_circuit(data)

    """ S=(var <op> var) -> [S][var <op> var] """
    for line in range(len(new_data)):
        new_data[line] = new_data[line].split('=')
        outputs.append(new_data[line][0])
        new_data[line].pop(0)

    """ evaluate boolean expression and store in vec """
    for line in range(len(new_data)):
        inputs.append(BooleanExpression(new_data[line][0]).symbols)
        results.append(TruthTable(str(new_data[line][0])).results)

    for i in range(len(results)):

        # generate 0 1 matrix to assign to variables
        out = np.matrix(list(itertools.product(
            [0, 1], repeat=len(inputs[i]))), dtype='int')

        _matrix = np.array(np.column_stack((out, results[i])))
        matrix.append(_matrix)

        p = PrettyTable()
        p.field_names = np.hstack((inputs[i], outputs[i]))

        for line in _matrix:
            p.add_row(line)

        # all permutations of true table with in+out vars size
        pts.append(p)

    with open('output53.txt', 'w') as myfile:
        for i in range(len(pts)):
            myfile.write("Circuit Analysis\n\nLogic Exp: {0}\n\nTruth Table:\n{1}\n\n#\n\n".format(
                str(outputs[i])+'='+str(new_data[i][0]), pts[i]))
        myfile.write("\n\nTime Elapsed: {0} secs\n\n".format(
            time.time() - start_time))
        myfile.close()

    """ at this point we have a working table and another one with fail 
    and we need to diagonose possible logic gates with errors """

    if len(table.results):
        diag_fail_circuit(originalData, table)
    else:
        print("There are no failures to diagnose.")
