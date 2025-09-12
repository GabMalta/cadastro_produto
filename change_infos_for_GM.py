from excel_pandas import change_infos_for_GM


names = [
    ("SOFT LISO D547", "D547", "SOFT LISO", ["0,5", 1, 2, 3, 4, 5, 6, 7, 10], 0, True),
    ("HELANQUINHA SEGUNDA PELE D177", "D177", "FORRO SEGUNDA PELE", [2, 3, 4, 5, 6, 7, 10, 15, 30], 0, True),
    ("SHANTUNG LISO A1424", "A1424", "SHANTUNG", [2, 3, 4, 5, 6, 7, 10, 15, 30], 0, True),
    ("SUEDE LISA - SUEDE DE MALHA D247", "D247", "SUEDE DE MALHA", [2, 3, 4, 5, 6, 7, 10, 15, 30], 0, True),
    ("SUEDE ESTAMPADA PERSONAGENS A1917", "A1917", "SUEDE PERSONAGENS", [2, 3, 4, 5, 6, 7, 10], 0, True),
    ("SUPLEX DE POLIESTER D425", "D425", "SUPLEX POLIESTER", [3, 4, 5, 6, 7, 10], 0, True),
    ("TACTEL LISO D74", "D74", "TACTEL LISO", [2, 3, 4, 5, 6, 7, 10, 15, 30, 50], 0, True),
]

change_infos_for_GM(names)
