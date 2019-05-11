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


def print_file(truth):

    with open(filename+'_result.txt', 'w') as f:
        # printa rotulo das variaveis
        for line_head in header:
            for v in line_head:
                f.write(v)
                f.write(" ")

        # printar valores da tabela
        for line_truth in truth:
            for v in line_truth:
                if type(v) == bool:
                    f.write("{}".format(int(v)))
                    f.write(" ")
                else:
                    f.write(v)
                    f.write(" ")
                    f.write("\n")
            f.write("\n")

    f.close()


def translate(type):

    if type == "presaEm1":
        return True
    else:
        return False


""" def b_search(A):

    if A in blacklist:
        return blacklist[A]
    else:
        return search(A) """


""" def insert_failures_in(perm_entries, table):

    # processando falhas [...]
    new = {}
    for op in perm_entries:
        gates.update({line_gate[2]: operate(
            b_search(line_gate[-2]), line_gate[1], b_search(line_gate[-1]))})

    for line in perm_entries:
        for line_gate in gates_aux:
            gates.update({line_gate[2]: operate(
                b_search(line_gate[-2]), line_gate[1], b_search(line_gate[-1]))})

    values = merge_line(ent, gates, "v")
    truth.append(values)

    return truth """


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

    # gera permutações das entradas e aplica nas func logicas da tabela
    perm_entries = list(itertools.product([False, True], repeat=int(n_ent[1])))
    table = generate_truth_table(perm_entries)
    
    # cria tabela e escreve no arquivo
    tt = PrettyTable()
    tt.field_names = header

    for line in table:
        tam = int(len(header))
        index = line[:tam]
        tt.add_row(index)
    
    table_txt = tt.get_string()
    with open(filename+'_output.txt','w') as file:
        file.write(table_txt)

    # inserir dic de entradas e saidas imutaveis ou "presas"
    # nesse caso, fazer permutações do n de entradas e saidas e falhas

    # gerar combinações de entradas com um valor fixo
    perm_entries_fails = list(itertools.product([False, True], repeat=int(n_ent[1])))

    v_aux = tuple(True)
    for line in perm_entries_fails:
        values = list(line)
        _v =  list(v_aux) + values[1:]

    """ filename_fail = filename+"_fail"
    f = open(filename+"_fail.txt", "r")
    n_fails = f.readline().split(",")
    truth, fails_aux = [], []

    for x in f:
        fails = x.split(",")
        fails[-1] = fails[-1].split("\n")[0]
        fails_aux.append(fails)

    f.close() """

    # fazer uma matriz de de portas por falhas

    # melhor construir um dict blacklist e consutar a partir dele

    # blacklist = {}

    # possible_failures_list=list(itertools.product([False, True], repeat = int(n_fails)))

    # inserindo falhas especificadas [...]
    # for fail_line in fails_aux:
    #    blacklist.update({str(fail_line[0]): translate(fail_line[1])})

    # função para gerar tabela com falhas de acordo com o arquivo de especificações
    # failure_table = insert_failures_in(perm_entries, table)

    # fazer função para diagnosticar falhas
    print("well done")
