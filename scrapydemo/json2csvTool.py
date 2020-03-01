import re



def columnGenerator(col, json):
    if col in json:
        return json[col]
    return ""



if __name__ == '__main__':


    import csv, json, sys

    # if you are not using utf-8 files, remove the next line
    # check if you pass the input file and output file
    fileOutput = "infojson2csv.csv"

    lines = [line.rstrip() for line in open("spiders/info_result.json") if line.startswith("{")]
    companylist = []
    outputFile = open(fileOutput, 'w')  # load csv file
    output = csv.writer(outputFile)  # create a csv.write

    fields = ['Title', 'Organization_name', 'Type', 'Traded as', 'ISIN', 'Industry', 'Predecessors', 'Headquarters'
              , 'Area served', 'Key people', 'Products', 'Revenue', 'Operating income', 'Net income', 'Total assets',
              'Total equity', 'Number of employees', 'Parent', 'Subsidiaries', 'Website']

    output.writerow(fields)
    for i in range(len(lines)):
        line_str = lines[i]
        if(line_str.endswith(',')):
            line_str = line_str[:-1]
        jsonLine = json.loads(line_str)
        output.writerow([columnGenerator(i, jsonLine) for i in fields])  # values row