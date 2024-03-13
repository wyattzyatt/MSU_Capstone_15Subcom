import csv

def compare_csv(mother_file, daughter_file):
    mother_data = {}
    error_count = 0
    total_count = 0

    with open(mother_file, 'r') as mother_csv, open(daughter_file, 'r') as daughter_csv:
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

# Example usage:
mother_file = "Mother_4.19.52.csv"
daughter_file = "Daughter_4.19.4.csv"
error_rate = compare_csv(mother_file, daughter_file)
# print("Error rate:", error_rate)
