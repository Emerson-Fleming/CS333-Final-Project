#Name: Emerson Fleming
#Date: May 7 2024
#Class: CS 333 Section 1001
#Assignment: Final Project
#File: bar_graph.py

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
    Processes the data to count occurrences of each protocol type.
    
    Args:
    - data: Pandas DataFrame containing the data
    
    Returns:
    - protocol_count: A dictionary containing counts of each protocol type
    - total_count: Total count of protocol occurrences
    """
    protocol_count = {}
    for i in range(len(data)):
        protocol = str(data.iloc[i, 2]) + " " + str(data.iloc[i, 4])
        if protocol in protocol_count:
            protocol_count[protocol] += 1
        else:
            protocol_count[protocol] = 1
    total_count = sum(protocol_count.values())
    return protocol_count, total_count

def plot_bar_graph(protocol_count, total_count):
    """
    Plots a bar graph of protocol counts.
    
    Args:
    - protocol_count: A dictionary containing counts of each protocol type
    - total_count: Total count of protocol occurrences
    """
    labels = list(protocol_count.keys())
    values = list(protocol_count.values())

    # Creating a bar graph
    bars = plt.bar(labels, values, color=['skyblue', 'lightcoral', 'lightgreen', 'gold', 'purple', 'orange'])

    # Adding labels and title
    plt.xlabel('Protocol Type')
    plt.ylabel('Count')
    plt.title('Protocol Counts')

    # Rotating x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Adding counts on top of each bar
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                 str(value), ha='center', va='bottom', color='black')

    # Adding percentages in the middle in white
    for bar, value in zip(bars, values):
        percentage = (value / total_count) * 100
        if percentage >= 5:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2,
                     f'{percentage:.2f}%', ha='center', va='center', color='white', fontweight='bold')

    # Display the graph
    plt.show()

if __name__ == "__main__":
    file_path = r"switchdata.csv"
    data = read_data(file_path)
    protocol_count, total_count = process_data(data)
    plot_bar_graph(protocol_count, total_count)
