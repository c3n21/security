from typing import List, Tuple, Any
import sys

frequencies_ita = [
("a",0.1174),
("b",0.092),
("c",0.0450),
("d",0.0373),
("e",0.1179),
("f",0.0095),
("g",0.0164),
("h",0.0154),
("i",0.1128),
("l",0.0651),
("m",0.0251),
("n",0.0688),
("o",0.0983),
("p",0.0305),
("q",0.0051),
("r",0.0637),
("s",0.0498),
("t",0.0562),
("u",0.0301),
("v",0.0210),
("z",0.0049 )
]

frequencies_ita.sort(reverse=True, key=lambda x: x[1])

def find_frequencies(text: str) -> dict[str, int]:
    frequencies = {}
    for c in text:
        if frequencies.get(c) is None:
            frequencies[c] = 1
        else:
            frequencies[c] += 1

    return frequencies

def relative_frequencies(l: List[Tuple[str, int]]) -> List[Tuple[str, float]]:
    total = sum([x[1] for x in l])
    result = []
    print(f"total = {total}")
    for tuple in l:
        result.append((tuple[0], (tuple[1]/total)*100))
        
    result.sort(reverse=True, key=lambda x: x[1])
    return result

def substitute(text: str, substitute: dict[str,str]) -> str:
    substituted_text = ""
    for c in text:
        new_c = substitute.get(c)
        if new_c is None:
            substituted_text += c
        else:
            substituted_text += substitute[c]

    return substituted_text

def create_substitution_table(l1: List[Tuple[str, int]], l2: List[Tuple[str,int]]) -> dict[str,str]:
    result = {}
    for a,b in zip(l1, l2):
        result[a[0]] = b[0]
    return result

def caesar(encrypted_text: str, offset: int) -> str:
    decrypted = ""

    for c in encrypted_text:
        decrypted += chr(ord(c) + offset)

    return decrypted

def print_pretty(l: List[Any]) -> None:
    for entry in l:
        print(f"{entry}")

if __name__ == '__main__':
    ignore_nonalpha = True
    extra = []#[" ", "\n"]

    for filename in sys.argv[1:]:
        print(f"Processing {filename}")
        with(open(filename, "r") as file):
            encrypted_text = file.read()
            frequencies_table = find_frequencies(encrypted_text)

            if ignore_nonalpha:
                for c in extra:
                    frequencies_table.pop(c, None)

                new_frequencies_table = {}
                for item in frequencies_table.items():
                    if item[0].isalpha():
                        new_frequencies_table[item[0]] = item[1]

                frequencies_table = new_frequencies_table


            frequencies_table = list(frequencies_table.items())
            frequencies_table.sort(reverse=True, key=lambda x: x[1]) # sort by frequencies

            substitution_table = create_substitution_table(frequencies_table, frequencies_ita)

            fix = [
                ("b", "n"),
                ("c", "d"),
                ("d", "u"),
                ("g", "h"),
                ("h", "f"),
                ("m", "v"),
                ("n", "r"),
#                ("r", "m"),
                ("u", "m"),
                ("v", "g"),
                ("s", "c"),
                ("r", "s"),
                ("f", "b"),
                ("z", "q"),
                ("q", "z"),
            ]

            new_substitution_table = {}
            for s, t in fix:
                for item in list(substitution_table.items()):
                    if new_substitution_table.get(item[0]) is None:
                        if item[1] == s:
                            new_substitution_table[item[0]] = t

            for a,b in list(substitution_table.items()):
                if new_substitution_table.get(a) is None:
                    new_substitution_table[a] = b
#            l1 = list(new_substitution_table.items())
#            l1.sort(key=lambda x: x[0])
#
#            l2 = list(substitution_table.items())
#            l2.sort(key=lambda x: x[0])
#            print(f"new = {l1}")
#            print(f"old = {l2}")
#            input()
            substitution_table = new_substitution_table

            print_pretty(list(substitution_table.items()))
            with(open(f"{filename}_decrypted", "w") as new_file):
                new_file.write(substitute(encrypted_text, substitution_table))
