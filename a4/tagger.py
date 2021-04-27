import os
import sys
import numpy as np
from collections import defaultdict
START = '<s>'
END = '</s>'
notation = ['.', '!', '?', '"']
N = 1e6
LAMBDA = 0.9

def generate_training_data(training_list):
    training_data = []
    for (num, filename) in enumerate(training_list):
        with open(filename) as f:
            for line in f.readlines():
                if(line.split(':')[0].rstrip() != ':'):
                    word = line.split(':')[0].rstrip()
                    tag = line.split(':')[1].rstrip().lstrip()
                else:
                    word = ':'
                    tag = line.split(':')[2].rstrip().lstrip()
                training_data.append((word,tag))               
            
    return training_data
    
def generate_testing_data(test_file):
    test_data = []
    with open(test_file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            test_data.append(line.strip().split()[0])
    return test_data
    
def train(training_data):
    #initialize
    l = len(training_data)
    context_dict = defaultdict(float)
    list_key_curr = defaultdict(float)
    transition_dict = defaultdict(float)
    emission_dict = defaultdict(float)
    
    transition_dict[START]= {}
       
    for line in training_data:
        word = line[0]
        tag = line[1]        
        list_key_curr[tag] += 1                       
       
    
    num = 0
    while num <= l-1:
        #initialize to 1 avoid dividing by zero
        transition_dict[START][training_data[num][1]] = 1
        transition_dict[training_data[num][1]] = {}
        if training_data[num][1] not in emission_dict:
            emission_dict[training_data[num][1]] = {}
        num +=1
    
    num = 0    
    while num <= l-1:
       
        transition_dict[START][training_data[0][1]] += 1 
        if training_data[num - 1][0] in notation:
            transition_dict[START][training_data[num][1]] += 1  
        
        transition_dict[training_data[num - 1][1]][training_data[num][1]] = 1
        transition_dict[training_data[num - 1][1]][training_data[num][1]] += 1 

        if training_data[num][0] not in emission_dict[training_data[num][1]]:    
            emission_dict[training_data[num][1]][training_data[num][0]] = 1 
        emission_dict[training_data[num][1]][training_data[num][0]] += 1 
        
        num +=1

    transition_dict = dict((k, dict((index, np.log(x)) for index, x in v.items())) for k, v in transition_dict.items())
    emission_dict = dict((k, dict((index, np.log(LAMBDA * x + (1 - LAMBDA) * 1 / N)) for index, x in v.items())) for k, v in emission_dict.items())
    
                
    return list_key_curr,transition_dict,emission_dict

def calculate_score(score,t_prob,e_prob):
    return score+t_prob+e_prob

def test(test_data,transition_dict,emission_dict,list_key_curr):

    t_prob = 0
    e_prob = 0
    score = {}
    outputing = {}
    
    l = len(test_data)
    for num in range(0,l):
        optimal_score = {}
        optimal_soln = {}
        emiss_key = test_data[num]
        
        if test_data[num - 1][0] in notation:

            #notation = ['.', '!', '?', '"']
            if test_data[num - 1][0] == '"':   
                outputing[num - 1] = 'PUQ'
            if test_data[num - 1][0] == '!':
                outputing[num - 1] = 'PUN'
            if test_data[num - 1][0] == '?': 
                outputing[num - 1] = 'PUN'
            if test_data[num - 1][0] == '.': 
                outputing[num - 1] = 'PUN'
           

        for trans_key in list_key_curr:        
            if test_data[num - 1][0] in notation:
                if trans_key not in transition_dict[START] or emiss_key not in emission_dict[trans_key]:
                    optimal_score[trans_key] = t_prob + e_prob
                    continue   
                t_prob = transition_dict[START][trans_key] 
                e_prob = emission_dict[trans_key][emiss_key]                
                optimal_score[trans_key] = calculate_score(0,t_prob,e_prob)
                
            else:
                optimal_score[trans_key] = float('-inf')
                for x in score:
                    if x in transition_dict:
                        if trans_key in transition_dict[x]:
                            t_prob = transition_dict[x][trans_key]
                        else:
                            t_prob = -1
                        if emiss_key in emission_dict[trans_key]:
                            e_prob = emission_dict[trans_key][emiss_key]
                        else:
                            e_prob= -1
                        prob = calculate_score(score[x],t_prob,e_prob)
                        
                        if optimal_score[trans_key] < prob or trans_key not in optimal_score:
                            optimal_score[trans_key] = prob
                            optimal_soln[trans_key] = x
                outputing[num - 1] = optimal_soln[max(optimal_score, key=lambda key: optimal_score[key])]
        
        score = optimal_score
      
    outputing[test_data[l-1]] = max(optimal_score, key=lambda key: optimal_score[key])
    outputing[len(test_data)-1] = 'PUN'
    with open(output_file, "w") as f:
        for i in range(len(test_data)):
            f.write(f'{test_data[i]} : {outputing[i]}\n')
       

def tag(training_list, test_file, output_file):
    # Tag the break_line from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("-------Tagging the file-------")
    
    #Construct training dataset
    training_data = generate_training_data(training_list)
    
    #Train model
    list_key_curr,transition_dict,emission_dict = train(training_data)
  
    #Construct testing dataset
    test_data = generate_testing_data(test_file)

    #Test
    test(test_data,transition_dict,emission_dict,list_key_curr)



if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    print("Training files: " + str(training_list))
    print("Test file: " + test_file)
    print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)
	