import ast
import argparse
import re
from _ast import ImportFrom, Import, FunctionDef


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "import_from": [], "functions": []}

    def visit_FunctionDef(self, node: FunctionDef):
        self.stats["functions"].append(ast.unparse(node))

    def visit_Import(self, node: Import):
        self.stats["import"].append(ast.unparse(node))

    def visit_ImportFrom(self, node: ImportFrom):
        self.stats["import_from"].append(ast.unparse(node))


def normalization_file(file: str) -> str:
    with open(file, 'r', encoding='utf-8') as f:
        tmp_file = f.read()
    current_file = ast.parse(tmp_file)
    for node in ast.walk(current_file):
        if isinstance(node, ast.Name):
            node.id = 'y'
    abbreviated_file = ast.unparse(current_file)
    abbreviated_file = re.sub('#.*', '', abbreviated_file, len(file))
    abbreviated_file = re.sub("'''.*'''", '', abbreviated_file, len(file))
    return abbreviated_file


def levenstein(origin: str, plagiarism: str) -> int:
    length_origin, length_plagiarism = len(origin), len(plagiarism)
    if length_origin > length_plagiarism:
        origin, plagiarism = plagiarism, origin
        length_origin, m = length_plagiarism, length_origin
    current_row = range(length_origin + 1)
    for i in range(1, length_plagiarism + 1):
        previous_row = current_row
        current_row = [i] + [0] * length_origin
        for j in range(1, length_origin + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if origin[j - 1] != plagiarism[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[length_origin]


def min_distance_suitable_functions(origin: Analyzer, plagiarism: Analyzer, key: str) -> int:
    distance = 0
    for origin_el in origin.stats[key]:
        min_distance = 100000
        tmp = None
        for plag_el in plagiarism.stats[key]:
            current_distance = levenstein(origin_el, plag_el)
            if min_distance > current_distance:
                min_distance = current_distance
                tmp = plag_el
        plagiarism.stats[key].remove(tmp)
        distance += min_distance
    return distance


def main():
    parser = argparse.ArgumentParser(description='Checking for antiplagiarism')
    parser.add_argument('input', type=str, help='Input file with pairs to check')
    parser.add_argument('output', type=str, help='Output file for answers')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        check_list = list(f.readlines())
    ans_list = []
    for line in check_list:
        origin_path, plagiarism_path = line.split()
        origin = Analyzer()
        plagiarism = Analyzer()
        origin_normal_file = normalization_file(origin_path)
        plagiarism_normal_file = normalization_file(plagiarism_path)
        origin.visit(ast.parse(origin_normal_file))
        plagiarism.visit(ast.parse(plagiarism_normal_file))
        full_distance = 0
        for key in origin.stats.keys():
            full_distance += min_distance_suitable_functions(origin, plagiarism, key)
        ans_list.append(round(1 - full_distance / max(len(origin_normal_file), len(plagiarism_normal_file)), 2))
    with open(args.output, 'w') as f:
        for el in ans_list:
            f.write(str(el) + "\n")


if __name__ == '__main__':
    main()
