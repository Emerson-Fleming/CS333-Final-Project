#Name: Emerson Fleming
#Date: May 7 2024
#Class: CS 333 Section 1001
#Assignment: Final Project
#File: line_graph.py

import pandas as pd
from matplotlib import pyplot as plt

def read_data(file_path):
    """
    Reads data from a CSV file into pandas DataFrame.
    
    Args:
    - file_path: The path to the CSV file
    
    Returns:
    - data: Pandas DataFrame containing the read data
    """
    data = pd.read_csv(file_path)
    return data

def process_data(data):
    """
    Processes the data to count calls per protocol.
    
    Args:
    - data: Pandas DataFrame containing the data
    
    Returns:
    - protocol_count: A dictionary containing counts of calls per protocol
    """
    dataArr = data.to_numpy()
    protocol_count = {}
    for i in range(len(dataArr)):
        protocol = str(dataArr[i][2]) + " " + str(dataArr[i][4])
        if protocol in protocol_count:
            for j in range(i - len(protocol_count[protocol])):
                protocol_count[protocol].append(protocol_count[protocol][-1])
            protocol_count[protocol].append(protocol_count[protocol][-1] + 1)
        else:
            protocol_count[protocol] = [1]
    return protocol_count, dataArr

def plot_graph(protocol_count, dataArr):
    """
    Plots a line graph of calls per protocol.
    
    Args:
    - protocol_count: A dictionary containing counts of calls per protocol
    - dataArr: Numpy array containing the data
    """
    domain = list(range(1, len(dataArr), 1))
    for k in range(len(protocol_count)):
        if k == 0:
            protocol_count[list(protocol_count.keys())[k]] = protocol_count[list(protocol_count.keys())[k]][1:]
        protocol_count[list(protocol_count.keys())[k]] = [0] * (len(domain) - len(protocol_count[list(protocol_count.keys())[k]])) + protocol_count[list(protocol_count.keys())[k]]
        plt.plot(domain, protocol_count[list(protocol_count.keys())[k]], linestyle='-', label=list(protocol_count.keys())[k])

    # Add labels and a title
    plt.xlabel('Total Calls')
    plt.ylabel('Calls per Protocol')
    plt.title('Line Graph of Data Points')

    # Display the graph
    plt.legend()
    plt.show()

if __name__ == "__main__":
    file_path = r"switchdata.csv"
    data = read_data(file_path)
    protocol_count, dataArr = process_data(data)
    plot_graph(protocol_count, dataArr)