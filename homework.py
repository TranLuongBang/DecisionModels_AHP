# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:57:43 2020

@author: ADMIN
"""

import pandas as pd
import numpy as np

def readData(filename):
    matrix = pd.read_csv(filename)
    data = matrix.iloc[:, 1:].to_numpy()
    return data

def returnRCIValue(criterion):
    data = pd.read_csv('RCI.csv')
    n = criterion.shape[1]
    RCIValue = data.iloc[0,n]
    return RCIValue
    
def returnPriority(criterion):
    criterion_sum = np.sum(criterion, axis=0)
    criterion_normalized = criterion/criterion_sum
    criterion_pev = np.mean(criterion_normalized, axis=1)
    return criterion_pev

def checkConsistency(criterion, priorityVector, RCIValue):
    print("Consistenty check:")
    print("RCI Value: ", RCIValue)
    
    if RCIValue == 0:
        print("With RCI value equals to 0. Should revise the comparison matrix")
    else: 
        criterion_sum = np.sum(criterion, axis=0)
        n = criterion.shape[1]
        
        # print(criterion_sum)
        # print(priorityVector)
        
        lambdamax = criterion_sum.dot(priorityVector)
        print("Lambdamax:", lambdamax)
        
        CI = (lambdamax - n)/(n-1)
        # print("CI:", CI)
        
        CR = CI/RCIValue
        print("CR: ", CR)
        
        if not CR >= 0.1:
            print("Consistency OK")
        else: 
            print("Revise the comparison matrix")

def makeDecision(priorityList, priorityVector):
    print("Decision Making:")
    
    # Summary of the results of Priorities with respect to each criterion
    a = np.array(priorityList)
    results = np.transpose(a)
    print("Priorities:" , results)
            
    # calculate the overall Priority
    overallPriority = results.dot(priorityVector)
    print("Overall priorities: ", overallPriority)
            
    # Recommend to make the final decision lying on max overall priority
    index = np.where(overallPriority == np.amax(overallPriority))
    print("the final decision could be made by alternative number:", index[0]+1, "with max overall priority: ", np.amax(overallPriority))

def main():
    while(True):
        try:
            # Deriving priorities for the criteria
            print("Input file name of pairwise comparison matrix of criteria: ")
            filename = input()
            if filename == '0':
                break
            
            criterion = readData(filename)
            print("Comparision Matrix:", criterion)
            
            # calculate priority vector for criteria
            priorityVector = returnPriority(criterion)
            print("Priority Vector:", priorityVector)
            
            RCIValue = returnRCIValue(criterion)
            
            #Consistency check for creiteria
            checkConsistency(criterion, priorityVector, RCIValue)
            
            
            # Deriving priorities for the alternatives
            priorityList = []
            
            # n is the number of criteria
            n = criterion.shape[1]
            while(n>0):
                print("Input file name of pairwise comparison matrix of alternative: ")
                try:
                    filename = input()
                    if filename == '0':
                        break
                    alternative = readData(filename)
                    
                    # calculate the priorities of each alternatives
                    pev = returnPriority(alternative)
                    print("Priority: ", pev)
                    
                    rci = returnRCIValue(alternative)
                    
                    #Consistency check for alternatives
                    checkConsistency(alternative, pev, rci)
                    
                    # add priority of each alternative to a prority list
                    priorityList.append(pev)
                    n = n-1
                except FileNotFoundError:
                    print("File not found")
                    continue
            
            makeDecision(priorityList, priorityVector)
            
        except FileNotFoundError:
                print("File not found")
                continue
        except:
                break  
    return 0
main()
        
        