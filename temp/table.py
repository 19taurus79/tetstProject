from prettytable import PrettyTable

hat = ["Номенклатура", "Серия", "Бух", "Склад"]
table = PrettyTable(hat)
ans = {
    "nomenclature": "Редонік АНТИСТРЕС АМІНО, 10л",
    "nomenclature_series": "07.06.2023",
    "buh": 880,
    "skl": 880,
}
req = []
ans = {
    "nomenclature": "Редонік АНТИСТРЕС АМІНО, 10л",
    "nomenclature_series": "07.06.2023",
    "buh": 880,
    "skl": 880,
}
# for i in range(len(ans.values())):
nom = ans.get("nomenclature")
req.append(nom)
ser = ans.get("nomenclature_series")
req.append(ser)
buh = ans.get("buh")
req.append(buh)
skl = ans.get("skl")
req.append(skl)
# req.append(f"{nom} партия {ser} бух {buh} склад {skl}")
table.add_row(req)

if __name__ == "__main__":
    print(table)
