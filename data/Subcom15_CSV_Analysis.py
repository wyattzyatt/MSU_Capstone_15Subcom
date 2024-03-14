import csv

def checkDuplicates(file):
    seen = set()
    duplicates = []

    with open(file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] in seen:
                duplicates.append(row)
            else:
                seen.add(row[0])

    return duplicates

def netDuplicates(motherFile, daughterFile):
    motherDuplicates = []
    daughterDuplicates = []
    try: motherDuplicates = checkDuplicates(motherFile)
    except: pass
    try: daughterDuplicates = checkDuplicates(daughterFile)
    except: pass
    
    allDuplicates = motherDuplicates + daughterDuplicates

    with open('duplicateCheck.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(allDuplicates)
    
    return allDuplicates

def compare_csv(motherFile, daughterFile):
    mother_data = {}
    error_count = 0
    total_count = 0

    with open(motherFile, 'r') as mother_csv, open(daughterFile, 'r') as daughter_csv:
        mother_reader = csv.reader(mother_csv)
        daughter_reader = csv.reader(daughter_csv)

        with open(f"Error.csv", 'w', newline='') as csvfile:
            fileError = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            with open(f"Timing.csv", 'w', newline='') as csvfile:
                fileTiming = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for mother_row, daughter_row in zip(mother_reader, daughter_reader):
                    total_count += 1
                    mother_value = mother_row[2]
                    daughter_value = daughter_row[2]
                    fileTiming.writerow([f"R:{total_count}","Daughter:", daughter_row[2],daughter_row[3],daughter_row[4],"Mother:", mother_row[2],mother_row[3],mother_row[4],f"Transmission time:", float(daughter_row[4])-float(mother_row[4])])

                    if mother_value != daughter_value:
                        error_count += 1
                        print(f"Row {total_count}: Daughter '{daughter_value}' != Mother '{mother_value}'")
                        fileError.writerow(["Row:",total_count,"Daughter:", daughter_value,"Mother:", mother_value])

    error_rate = (error_count / total_count) * 100 if total_count != 0 else 0
    print(f"Total rows: {total_count}")
    print(f"Error count: {error_count}")
    print(f"Error rate: {error_rate:.2f}%")
    
    return error_rate


testType = 0
if testType == 0:
    motherFile = "Mother_4.19.52.csv"
    daughterFile = "Daughter_4.19.4.csv"
    error_rate = compare_csv(motherFile, daughterFile)
elif testType == 1:
    motherCommands = "MotherCommands.csv"
    daughterCommmands = "DaughterCommands.csv"
    duplicates = netDuplicates(motherCommands, daughterCommmands)
    print(duplicates)
elif testType == 2:
    motherFile = "Mother_4.19.52.csv"
    daughterFile = "Daughter_4.19.4.csv"
    error_rate = compare_csv(motherFile, daughterFile)
    
    motherCommands = "MotherCommands.csv"
    daughterCommmands = "DaughterCommands.csv"
    duplicates = netDuplicates(motherCommands, daughterCommmands)
    
# print("Error rate:", error_rate)
