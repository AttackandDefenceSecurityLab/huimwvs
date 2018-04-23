str="Parameter: id (GET)\n    Type: boolean-based blind\n    Title: AND boolean-based blind - WHERE or HAVING clause\nParameter: id (GET)\n    Type: boolean-based blind\n    Title: AND boolean-based blind - WHERE or HAVING clause\n"
raws = str.split("\n")

for row in raws:
    #print para
    if "Parameter:" in row:
        para = row.split(": ")[1]
        print para
