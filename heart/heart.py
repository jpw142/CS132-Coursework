# r = 1 metrics
# Precision: 0.683
# Recall: 0.701
# Accuracy: 0.655
# r = 2 metrics
# Precision: 0.684
# Recall: 0.697
# Accuracy: 0.655

import csv;

def main():
    data = read_data("heart.csv")
    # get num_patients
    for key in data.keys():
        first_key = key
        break
    num_patients = len(data[first_key])
    # Do this twice for r = 1 and r = 2 
    for r in range(1, 3):
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0
        # Find best patient for each one
        for i in range(num_patients):
            predicted = nearest_neighbor(i, data, r) 
            reality = data["HeartDisease"][i]
            # Positive
            if predicted == 1:
                # True
                if reality == 1:
                    true_positives += 1
                # False
                else:
                    false_positives += 1
            # Negative
            else:
                # True
                if reality == 0:
                    true_negatives += 1
                # False
                else:
                    false_negatives += 1
        print("r = " + str(r))
        print("  True Positives: " + str(true_positives))
        print("  True Negatives: " + str(true_negatives))
        print("  False Positives: " + str(false_positives))
        print("  False Negatives: " + str(false_negatives))
        print("  Precision: " + str(true_positives / (true_positives + false_positives)))
        print("  Recall: " + str(true_positives / (true_positives + false_negatives)))
        print("  Accuracy: " + str((true_positives + true_negatives) / num_patients))



# Reads the data into a dictionary and the value is the columns list of values
# Cleans the data as well, turning it into floats or integers as appropriate
# Returns dictionary of column headers with values of corresponding lists of entries
def read_data(file_name):
    diction = {}
    with open(file_name) as file:
        reader = csv.DictReader(file)
        # Go through each row
        for row in reader:
            # gets each key value pair in that row
            for key, value in row.items():
                # If it's already in the dictionary (row 1+), append it
                if key in diction:
                    # These columns are not required to be type cast
                    if key == "Sex" or key == "ChestPainType":
                        diction[key].append(value)
                    # Every other value requires int typecasting
                    else:
                        diction[key].append(int(value))
                # If its the first row, start the list cause the key isnt in there
                else:
                    # These columns are not required to be type cast
                    if key == "Sex" or key == "ChestPainType":
                        diction[key] = [value]
                    # Every other value requires int typecasting
                    else:
                        diction[key] = [int(value)]
        return diction
                    
# Takes cleaned dictionary from read_data, patient number, and a tuning parameter
# r = 1 Manhattan Distance
# r = 2 Euclidean Distance
# Finds the nearest neighbor and returns their heart disease status (1 or 0)
def nearest_neighbor(pn, data_dict, r):
    # We can't do anything if r isn't 1 or 2
    if r != 1 and r != 2:
        print("You messed up! r has to be 1 or 2")
        return
    # just need 1 key to get the length of the number of patients
    for key in data_dict.keys():
        first_key = key
        break
    num_patients = len(data_dict[first_key])
        
    # We need a patient number thats not our patient, and the only case this doesnt work is 0, hence abs
    best_patient = abs(pn - 1)
    best_patient_score = 0
    for i in range(num_patients):
        # Dont compare patient to themself
        if i == pn:
            continue
        i_patient_score = -1
        # Go through each category thats not sex, chestpain, heartdisease
        for key, value in data_dict.items():
            # Skips unwanted categories
            if key == "ChestPainType" or key == "HeartDisease" or key == "Sex":
                continue
            # Formula for the euclidean distance
            i_patient_score += abs(value[pn] - value[i]) ** r
        # if its a better score then set it
        if best_patient_score == -1:
            best_patient_score = i_patient_score
            best_patient = i
        elif i_patient_score < best_patient_score:
            best_patient_score = i_patient_score
            best_patient = i
    return data_dict["HeartDisease"][best_patient]

main()
