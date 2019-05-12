import itertools
from prettytable import PrettyTable


def search(A):
    if A in gates:
        return gates[A]
    else:
        return ent[A]


def operate(A, op, B):
    if op == "and":
        return A and B
    if op == "or":
        return A or B
    if op == "xor":
        return A ^ B


def generate_truth_table(perm_entries):

    for line in perm_entries:
        # essa func seta valores true or false para as entradas
        for i in range(len(line)):
            ent_name = n_ent[-i-1].split("\n")[0]
            # inserir condição de consulta dos imutáveis
            ent.update({str(ent_name): line[-i-1]})

        for line_gate in gates_aux:
            # inserir condição de consulta dos imutáveis
            gates.update({line_gate[2]: operate(
                search(line_gate[-2]), line_gate[1], search(line_gate[-1]))})

        # merge dicts *only python > 3.5*
        line_table = {**ent, **gates}
        truth.append(list(line_table.values()))
        # print_file(truth)

    return truth


if __name__ == "__main__":

    filename = "circuito"
    f = open(filename+".txt", "r")

    truth, gates_aux = [], []
    ent, gates = {}, {}

    n_ent = f.readline().split(",")
    n_saidas = f.readline().split(",")
    n_gates = f.readline().split(",")

    # make header
    ent_id = n_ent[1]
    ent_1 = n_ent[int(ent_id)-1:]
    ent_1[-1] = ent_1[-1].split("\n")[0]

    saida_id = n_saidas[1]
    saida_1 = n_saidas[int(saida_id):]
    saida_1[-1] = saida_1[-1].split("\n")[0]

    header = ent_1 + saida_1

    for x in f:
        ga = x.split(",")
        ga[-1] = ga[-1].split("\n")[0]
        gates_aux.append(ga)

    f.close()

    # generates permutations of the inputs and applies in the functions of the table
    perm_entries = list(itertools.product([False, True], repeat=int(n_ent[1])))
    table = generate_truth_table(perm_entries)

    # create table and write to file
    tt = PrettyTable()
    tt.field_names = header

    for line in table:
        tam = int(len(header))
        index = line[:tam]
        tt.add_row(index)

    table_txt = tt.get_string()
    with open(filename+'_output.txt', 'w') as file:
        file.write(table_txt)

    print("well done")
