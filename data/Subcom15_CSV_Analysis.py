import csv

def checkDuplicates(file):
    seen = set()
    duplicates = []

    with open(file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] in seen:
                duplicates.append(row)
            if row[2] in seen:
                duplicates.append(row)
            else:
                seen.add(row[1])
                seen.add(row[2])

    return duplicates

def netDuplicates(motherFile, daughterFile):
    motherDuplicates = []
    daughterDuplicates = []
    try: motherDuplicates = checkDuplicates(motherFile)
    except: print("Didnt Open MotherFile")
    try: daughterDuplicates = checkDuplicates(daughterFile)
    except: print("Didnt Open DaughterFile")
    
    allDuplicates = motherDuplicates + daughterDuplicates

    with open('duplicateCheck.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(allDuplicates)
    
    return allDuplicates

def compare_csv(motherFile, daughterFile):
    mother_data = {}
    error1_count = 0
    error2_count = 0
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
                    fileTiming.writerow([f"Mother to Daughter{total_count}:", mother_row[6], daughter_row[10], float(daughter_row[12])-float(mother_row[8]),f"Daughter to Mother{total_count}:", daughter_row[6], mother_row[10], float(mother_row[12])-float(daughter_row[8])])

                    if(mother_row[0] != "Mother3"):
                        if mother_row[6] != daughter_row[10]:
                            error1_count += 1
                            print(f"Row {total_count}: Mother Sent: '{mother_row[6]}', Daughter Received: '{daughter_row[10]}'")
                            fileError.writerow(["Row:",total_count,"Daughter Received:", daughter_row[10],"Mother Sent:", mother_row[6]])
                        if mother_row[10] != daughter_row[6]:
                            error2_count += 1
                            print(f"Row {total_count}: Daughter Sent: '{daughter_row[6]}', Mother Received '{mother_row[10]}'")
                            fileError.writerow(["Row:",total_count,"Daughter Sent:", daughter_row[6],"Mother Received:", mother_row[10]])
                    else:
                        total_count -= 1

    error1_rate = (error1_count / total_count) * 100 if total_count != 0 else 0
    error2_rate = (error2_count / total_count) * 100 if total_count != 0 else 0
    print(f"Total rows: {total_count}")
    print(f"Mother to Daughter Error count: {error1_count}")
    print(f"Mother to Daughter Error rate: {error1_rate:.2f}%")
    print(f"Daughter to Mother Error count: {error2_count}")
    print(f"Daughter to Mother Error rate: {error2_rate:.2f}%")
    
    return 


testType = 0
if testType == 0:
    motherFile = "data/Mother_6.10.26.csv"
    daughterFile = "data/Daughter_6.10.8.csv"
    error_rate = compare_csv(motherFile, daughterFile)
elif testType == 1:
    motherCommands = "data/Test8Commands.csv"
    daughterCommmands = "data/Test9Commands.csv"
    duplicates = netDuplicates(motherCommands, daughterCommmands)
    print(duplicates)
elif testType == 2:
    motherFile = "Mother_4.19.52.csv"
    daughterFile = "Daughter_4.19.4.csv"
    error_rate = compare_csv(motherFile, daughterFile)
    
    motherCommands = "MotherCommands.csv"
    daughterCommmands = "DaughterCommands.csv"
    duplicates = netDuplicates(motherCommands, daughterCommmands)
    
