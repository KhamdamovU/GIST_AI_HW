# Name: Ulugbek Khamdamov
# GIST 2021, AI Graduate School
# ID: 20204120

import sys
import re

# Please change the filename to test this code for another dataset
filename = "weather-test1-1000.txt"
transition_matrix = [[0.8,0.05,0.15],[0.2,0.6,0.2],[0.2,0.3,0.5]]
umbrella_prob = [[0.1,0.8,0.3],[0.9,0.2,0.7]]
initial_prob = [0.5,0.25,0.25]


# Function which normalizes the input list and returns the output list
def normalize(norm)->int:
    tot_sum = 0
    for i in norm:
        tot_sum+= i

    for i in range(len(norm)):
        norm[i] = round(norm[i]/tot_sum,5)

    return norm

def getUmbrellaValue(index):
    file = open(filename, "r")
    data = file.readlines()
    return data[index + 1].split(",")[1]


def filtering(stateIndex,isCalled=False):


    current_prob = initial_prob
    if not isCalled:
        print("The FILTERING inference")
        print(f"For day number: {0} ")
        print(f"Sunny: {current_prob[0]}, Rainy: {current_prob[1]}, Foggy: {current_prob[2]}\n")

    for count in range(stateIndex):
        temp_list =[]

        first = [element * current_prob[0] for element in transition_matrix[0]]
        second = [element * current_prob[1] for element in transition_matrix[1]]
        third = [element * current_prob[2] for element in transition_matrix[2]]
        for (item1, item2, item3) in zip(first, second, third):
            temp_list.append(item1 + item2 + item3)


        current_prob = []
        if getUmbrellaValue(count) == "no\n":
            for t in range(len(temp_list)):
                current_prob.append(umbrella_prob[1][t]*temp_list[t])
        else:
            for t in range(len(temp_list)):
                current_prob.append(umbrella_prob[0][t]*temp_list[t])
        current_prob = normalize(current_prob)
        if not isCalled:
            print(f"For day number: {count+1} ")
            print(f"Sunny: {current_prob[0]}, Rainy: {current_prob[1]}, Foggy: {current_prob[2]}\n")



    return current_prob


def prediction(stateIndex,lastEvidenceIndex):
    current_prob = initial_prob
    print("Prediction inference: ")
    print(f"For day number: {0} ")
    print(f"Sunny: {current_prob[0]}, Rainy: {current_prob[1]}, Foggy: {current_prob[2]}\n")
    for count in range(stateIndex):
        temp_list = []

        first = [element * current_prob[0] for element in transition_matrix[0]]
        second = [element * current_prob[1] for element in transition_matrix[1]]
        third = [element * current_prob[2] for element in transition_matrix[2]]
        for (item1, item2, item3) in zip(first, second, third):
            temp_list.append(item1 + item2 + item3)

        if count >= lastEvidenceIndex: # this control flow is for checking whether we should start predicting or not
            current_prob = temp_list.copy()
        if getUmbrellaValue(count) == "no\n" and count < lastEvidenceIndex:
            current_prob = []
            for t in range(len(temp_list)):
                current_prob.append(umbrella_prob[1][t] * temp_list[t])
        elif count < lastEvidenceIndex:
            current_prob = []
            for t in range(len(temp_list)):
                current_prob.append(umbrella_prob[0][t] * temp_list[t])
        current_prob = normalize(current_prob)
        if count - lastEvidenceIndex >= 0:
            print(f"Prediciton for day number: {count + 1} ")
            print(f"Sunny: {current_prob[0]}, Rainy: {current_prob[1]}, Foggy: {current_prob[2]}\n")

        else:
            print(f"For day number: {count+1} ")
            print(f"Sunny: {current_prob[0]}, Rainy: {current_prob[1]}, Foggy: {current_prob[2]}\n")


    return current_prob


# The recursive function for finding the backward part needed for smoothing inference
def recursiveBackwardAlgorithm(stateIndex, k):


    if k ==stateIndex:
        return 1
    else:
        first = []
        second = []
        third = []
        temp_list = []
        if getUmbrellaValue(k) =="no\n":
            nextElement = recursiveBackwardAlgorithm(stateIndex,k+1)

            if nextElement!=1:
                    for count in range(len(nextElement)):
                        first.append(umbrella_prob[1][0] * nextElement[count] * transition_matrix[0][count])
                        second.append(umbrella_prob[1][1] * nextElement[count] * transition_matrix[1][count])
                        third.append(umbrella_prob[1][2] * nextElement[count] * transition_matrix[2][count])
                    for (item1, item2, item3) in zip(first, second, third):
                        temp_list.append(item1 + item2 + item3)

                    return temp_list
            else:
                for count in range(3):
                    first.append(umbrella_prob[1][0] * transition_matrix[0][count])
                    second.append(umbrella_prob[1][1] * transition_matrix[1][count])
                    third.append(umbrella_prob[1][2] * transition_matrix[2][count])
                for (item1, item2, item3) in zip(first, second, third):
                    temp_list.append(item1 + item2 + item3)

                return temp_list
        else:
            nextElement = recursiveBackwardAlgorithm(stateIndex, k + 1)

            if nextElement != 1:
                for count in range(len(nextElement)):
                    first.append(umbrella_prob[0][0] * nextElement[count] * transition_matrix[0][count])
                    second.append(umbrella_prob[0][1] * nextElement[count] * transition_matrix[1][count])
                    third.append(umbrella_prob[0][2] * nextElement[count] * transition_matrix[2][count])
                for (item1, item2, item3) in zip(first, second, third):
                    temp_list.append(item1 + item2 + item3)

                return temp_list
            else:
                for count in range(3):
                    first.append(umbrella_prob[0][0] * transition_matrix[0][count])
                    second.append(umbrella_prob[0][1] * transition_matrix[1][count])
                    third.append(umbrella_prob[0][2] * transition_matrix[2][count])
                for (item1, item2, item3) in zip(first, second, third):
                    temp_list.append(item1 + item2 + item3)

                return temp_list


# Smoothing is implemented using Forward and backward algorithm discussed on our textBook
# To find the backward part the recursive function was implemented
def smoothing(stateIndex, k):
    print("Smoothing inference: ")
    print(f"For day number: {k} with state index: {stateIndex}")

    forward = filtering(k,True)
    backwardRecursion = recursiveBackwardAlgorithm(stateIndex, k+1)
    final_result = []
    for count in range(3):
        final_result.append(forward[count]*backwardRecursion[count])
    normalize(final_result)

    print(f"Sunny: {final_result[0]}, Rainy: {final_result[1]}, Foggy: {final_result[2]}\n")
    return final_result




def umbrellaFalseOrTrue(index):
    file = open(filename, "r")
    data = file.readlines()
    if data[index + 1].split(",")[1] == "no\n":
        return 1
    else: return 0

# This function returns the most likely sequence of hidden state elements given the number of evidence variables
# The output of this function is a list of most likely elements
# You can find more about the implementation of this code in the report
def viterbi(weatherStateIndex, numOfObservations):
   pdist = initial_prob
   back_pointers = []
   for k in range(0, numOfObservations):
      pdist_new = []
      prev_pointer = []
      for i in range(0,3):
         prob_i = 0.0
         best_j = 0
         for j in range(0,3):
            prob_i_from_j = transition_matrix[i][j] * pdist[j]
            if (prob_i_from_j > prob_i):
               prob_i = prob_i_from_j
               best_j = j
         prob_i = prob_i * umbrella_prob[umbrellaFalseOrTrue(k)][i]
         pdist_new.append(prob_i)
         prev_pointer.append(best_j)
      pdist = normalize(pdist_new)
      back_pointers.append(prev_pointer)

   n = numOfObservations - 1
   s_prob = 0
   s = 0
   for i in range(0,3):
      if (pdist[i] > s_prob):
         s_prob = pdist[i]
         s = i
   seq = []
   for k in range(n,-1,-1):
      seq.append(weatherStateIndex[s])
      s = back_pointers[k][s]
   seq.reverse()

   return seq


# This function is used for viterbi algorithm to check the accuracy of the output generated by viterbi function

def getAccuracy(viterbiSequence):
    file = open(filename, "r")
    data = file.readlines()
    correctCount = 0
    for count in range(len(viterbiSequence)):
        if data[count + 1].split(",")[0] == viterbiSequence[count]:        # This function splits line into two parts that is Hidden state data and Evidence data, but in this case it returns hidden state data
            correctCount+=1
    return correctCount/len(viterbiSequence)


# This function receives the sequence number and extracts all the weather
# data from txt file until the sequence number is reached
def getWeatherSequence(numOfSequence):
    file = open(filename, "r")
    data = file.readlines()
    sequence = []
    for count in range(numOfSequence):
        sequence.append(data[count + 1].split(",")[0])
    return sequence


# The main function is used as a test function to the see the results of all four inference tasks
# The variable n_obs_short is used for all inference tasks
if __name__ == '__main__':
    n_obs_short = 10
    #
    filtering(stateIndex=n_obs_short)
    prediction(stateIndex=n_obs_short, lastEvidenceIndex=n_obs_short-1)
    smoothing(stateIndex=n_obs_short, k=5)
    weatherStateIndex = {0: 'sunny', 1: 'rainy', 2: 'foggy'}
    print(f'Viterbi - predicted state sequence for the first {n_obs_short} elements: ', viterbi(weatherStateIndex, n_obs_short))
    print(f'Viterbi - actual state sequence: {getWeatherSequence(n_obs_short)}')
    print(f"Accuracy for the first {n_obs_short} elements is: {getAccuracy(viterbi(weatherStateIndex,n_obs_short))}")
    print(f"Accuracy for the full sequence is: {getAccuracy(viterbi(weatherStateIndex,1000))}")
    print(viterbi(weatherStateIndex,100))







