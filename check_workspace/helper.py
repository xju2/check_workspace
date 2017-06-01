# -*- coding: utf-8 -*-

def get_mass(input_str):
    items = input_str.split(',')
    mass_str = 0
    for item in items:
        if "mH" in item:
            mass_str = item
            break

    if ":" in mass_str:
        return mass_str.split(':')[1]
    elif "=" in mass_str:
        return mass_str.split('=')[1]
    else:
        return mass_str


def tabulize_limit(file_name):
    out = ""
    out +="\\begin{table}[!htb]\n \t\\centering\n\t\\caption{}\n \t\\begin{tabular}{*{7}{c}}\n"
    out += "\tmH & -2~$\sigma$ & -1~$\sigma$ & median & 1~$\sigma$ & 2~$\sigma$ & observed \\\\ \\hline"
    out += '\n'
    indices = 1, 2
    with open(file_name) as f:
        for line in f:
            items = line[:-1].split()
            mass = get_mass(items[0])
            items[0] = mass
            new_list = [i for j,i in enumerate(items) if j not in indices]
            out += '\t'
            out += ' & '.join(new_list)
            out += ' \\\\ \n'
    out += '\\hline\n'
    out += "\t\\end{tabular}\n\\end{table}\n"

    print out
