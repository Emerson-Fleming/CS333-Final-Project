#Name: Emerson Fleming
#Date: May 7 2024
#Class: CS 333 Section 1001
#Assignment: Final Project
#File: tests.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import io
import sys
import argparse
import pyshark
import os

# Import the functions from the scripts
from script_to_csv import save_packet_data_to_csv, process_packet
from line_graph import read_data, process_data, plot_graph
from bar_graph import read_data as read_data_bar, process_data as process_data_bar, plot_bar_graph

#UNIT TESTING
class TestScriptToCSV(unittest.TestCase):
    def test_process_packet_matching_ip(self):
        # Create a mock packet object with the required attributes
        mock_packet = type('MockPacket', (), {
            'ip': type('MockIP', (), {
                'src': '192.168.0.1',
                'dst': '192.168.0.2'
            }),
            'sniff_time': '2024-05-07 12:00:00',
            'transport_layer': 'TCP',
            'length': 100
        })()

        # Call the process_packet function with the mock packet and IP address
        result = process_packet(mock_packet, '192.168.0.1')

        # Check if the result matches the expected data
        expected_result = ('2024-05-07 12:00:00', '192.168.0.1', '192.168.0.2', 'TCP', 100, 'Source')
        self.assertEqual(result, expected_result)

    def test_process_packet_not_matching_ip(self):
        # Create a mock packet object with the required attributes
        mock_packet = type('MockPacket', (), {
            'ip': type('MockIP', (), {
                'src': '192.168.0.2',
                'dst': '192.168.0.3'
            }),
            'sniff_time': '2024-05-07 12:00:00',
            'transport_layer': 'UDP',
            'length': 200
        })()

        # Call the process_packet function with the mock packet and IP address
        result = process_packet(mock_packet, '192.168.0.1')

        # Check if the result is None (packet should not match the IP address)
        self.assertIsNone(result)

    @patch('pyshark.FileCapture')
    def test_save_packet_data_to_csv(self, mock_FileCapture):
        # Mocking argparse arguments
        capture_file = 'test_capture.pcapng'
        csv_file = 'test_output.csv'
        ip_address = '192.168.0.1'

        # Mocking reading packets from capture file
        mock_packets = [
            type('MockPacket', (), {
                'ip': type('MockIP', (), {
                    'src': '192.168.0.1',
                    'dst': '192.168.0.2'
                }),
                'sniff_time': '2024-05-07 12:00:00',
                'transport_layer': 'TCP',
                'length': 100
            })(),
            # Add more mock packets as needed
        ]

        # Set up mock FileCapture instance
        mock_cap = mock_FileCapture.return_value
        mock_cap.__iter__.return_value = iter(mock_packets)

        # Call the save_packet_data_to_csv function with mock arguments
        save_packet_data_to_csv(capture_file, csv_file, ip_address)

        # Check if CSV file exists
        self.assertTrue(os.path.exists(csv_file))

        # Read the CSV file
        data = pd.read_csv(csv_file)

        # Define expected row count (adjust as needed)
        expected_row_count = len(mock_packets)

        # Check number of rows
        self.assertEqual(len(data), expected_row_count)
# Assert specific data if known


class TestLineGraph(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'Time': [1, 2, 3, 4, 5],
            'Source IP': ['192.168.0.1', '192.168.0.2', '192.168.0.1', '192.168.0.3', '192.168.0.2'],
            'Destination IP': ['192.168.0.2', '192.168.0.1', '192.168.0.3', '192.168.0.1', '192.168.0.3'],
            'Protocol': ['TCP', 'UDP', 'TCP', 'UDP', 'TCP'],
            'Length': [100, 200, 150, 120, 180]
        })

    def test_read_data(self):
        # Mocking file path
        file_path = 'test_data.csv'

        # Mocking reading CSV data
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with patch('builtins.open', return_value=io.StringIO(self.data.to_csv())):
                data = read_data(file_path)

        # Remove the 'Unnamed: 0' column from the returned data
        data = data.drop(columns=['Unnamed: 0'])

        # Print the modified returned data for inspection
        print("Modified Returned Data:")
        print(data)
        print("\nExpected Data:")
        print(self.data)

        # Compare the data
        self.assertEqual(data.equals(self.data), True)

    def test_process_data(self):
        # Test process_data function with sample data
        protocol_count, dataArr = process_data(self.data)

    def test_plot_graph(self):
        # Mocking plot_graph function
        with patch('matplotlib.pyplot.show'):
            plot_graph({}, [])  # Assuming empty data for testing

class TestBarGraph(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.data = pd.DataFrame({
            'Time': [1, 2, 3, 4, 5],
            'Source IP': ['192.168.0.1', '192.168.0.2', '192.168.0.1', '192.168.0.3', '192.168.0.2'],
            'Destination IP': ['192.168.0.2', '192.168.0.1', '192.168.0.3', '192.168.0.1', '192.168.0.3'],
            'Protocol': ['TCP', 'UDP', 'TCP', 'UDP', 'TCP'],
            'Length': [100, 200, 150, 120, 180]
        })

    def test_process_data(self):
        # Test process_data_bar function with sample data
        protocol_count, total_count = process_data_bar(self.data)

    def test_plot_bar_graph(self):
        # Mocking plot_bar_graph function
        with patch('matplotlib.pyplot.show'):
            plot_bar_graph({}, 0)  # Assuming empty data for testing

#INTEGRATION TESTING
class TestIntegration(unittest.TestCase):
    @patch('pyshark.FileCapture')
    def test_process_packet_integration(self, mock_FileCapture):
        # Mock argparse arguments
        capture_file = 'test_capture.pcapng'
        csv_file = 'test_output.csv'
        ip_address = '192.168.0.1'
        
        # Mock packets for testing
        mock_packets = [
            MagicMock(ip={'src': '192.168.0.1', 'dst': '192.168.0.2'}, sniff_time='2024-05-07 12:00:00', transport_layer='TCP', length=100),
            # Add more mock packets as needed
        ]
        
        # Set up mock FileCapture instance
        mock_cap = mock_FileCapture.return_value
        mock_cap.__iter__.return_value = iter(mock_packets)
        
        # Call the function to be tested
        save_packet_data_to_csv(capture_file, csv_file, ip_address)
        
        # Read the CSV file
        try:
            data = pd.read_csv(csv_file)
            print("CSV file content:")
            print(data)
        except Exception as e:
            print("Error reading CSV file:", e)
            self.fail("Failed to read CSV file")

    @patch('pyshark.FileCapture')
    def test_process_packet_different_ip(self, mock_FileCapture):
        # Mock argparse arguments
        capture_file = 'test_capture.pcapng'
        csv_file = 'test_output.csv'
        ip_address = '192.168.0.2'  # Different IP address
        
        # Mock packets for testing
        mock_packets = [
            MagicMock(ip={'src': '192.168.0.1', 'dst': '192.168.0.2'}, sniff_time='2024-05-07 12:00:00', transport_layer='TCP', length=100),
            MagicMock(ip={'src': '192.168.0.2', 'dst': '192.168.0.3'}, sniff_time='2024-05-07 12:01:00', transport_layer='UDP', length=200),
            # Add more mock packets as needed
        ]
        
        # Set up mock FileCapture instance
        mock_cap = mock_FileCapture.return_value
        mock_cap.__iter__.return_value = iter(mock_packets)
        
        # Call the function to be tested
        save_packet_data_to_csv(capture_file, csv_file, ip_address)
        
        # Read the CSV file
        try:
            data = pd.read_csv(csv_file)
            print("CSV file content:")
            print(data)
        except Exception as e:
            print("Error reading CSV file:", e)
            self.fail("Failed to read CSV file")

    @patch('pyshark.FileCapture')
    def test_process_packet_different_capture_files(self, mock_FileCapture):
        # Mock argparse arguments
        capture_file_1 = 'test_capture_1.pcapng'
        capture_file_2 = 'test_capture_2.pcapng'
        csv_file = 'test_output.csv'
        ip_address = '192.168.0.1'
        
        # Mock packets for the first capture file
        mock_packets_1 = [
            MagicMock(ip={'src': '192.168.0.1', 'dst': '192.168.0.2'}, sniff_time='2024-05-07 12:00:00', transport_layer='TCP', length=100),
            MagicMock(ip={'src': '192.168.0.2', 'dst': '192.168.0.3'}, sniff_time='2024-05-07 12:01:00', transport_layer='UDP', length=200),
            # Add more mock packets as needed
        ]
        
        # Set up mock FileCapture instance for the first capture file
        mock_cap_1 = mock_FileCapture.return_value
        mock_cap_1.__iter__.return_value = iter(mock_packets_1)
        
        # Call the function to be tested with the first capture file
        save_packet_data_to_csv(capture_file_1, csv_file, ip_address)
        
        # Read the CSV file generated from the first capture file
        try:
            data = pd.read_csv(csv_file)
            print("CSV file content (Capture File 1):")
            print(data)
        except Exception as e:
            print("Error reading CSV file:", e)
            self.fail("Failed to read CSV file")
        
        # Mock packets for the second capture file
        mock_packets_2 = [
            MagicMock(ip={'src': '192.168.0.1', 'dst': '192.168.0.2'}, sniff_time='2024-05-07 12:02:00', transport_layer='TCP', length=150),
            MagicMock(ip={'src': '192.168.0.2', 'dst': '192.168.0.3'}, sniff_time='2024-05-07 12:03:00', transport_layer='UDP', length=250),
            # Add more mock packets as needed
        ]
        
        # Set up mock FileCapture instance for the second capture file
        mock_cap_2 = mock_FileCapture.return_value
        mock_cap_2.__iter__.return_value = iter(mock_packets_2)
        
        # Call the function to be tested with the second capture file
        save_packet_data_to_csv(capture_file_2, csv_file, ip_address)
        
        # Read the CSV file generated from the second capture file
        try:
            data = pd.read_csv(csv_file)
            print("CSV file content (Capture File 2):")
            print(data)
        except Exception as e:
            print("Error reading CSV file:", e)
            self.fail("Failed to read CSV file")


    @patch('pyshark.FileCapture')
    def test_process_packet_large_data_sets(self, mock_FileCapture):
        # Mock argparse arguments
        capture_file = 'large_capture.pcapng'
        csv_file = 'test_output.csv'
        ip_address = '192.168.0.1'
        
        # Generate a large number of mock packets for testing
        num_packets = 1000
        mock_packets = [
            MagicMock(ip={'src': '192.168.0.1', 'dst': '192.168.0.2'}, sniff_time=f'2024-05-07 12:00:{i:02}', transport_layer='TCP', length=100) for i in range(num_packets)
        ]
        
        # Set up mock FileCapture instance
        mock_cap = mock_FileCapture.return_value
        mock_cap.__iter__.return_value = iter(mock_packets)
        
        # Call the function to be tested
        save_packet_data_to_csv(capture_file, csv_file, ip_address)
        
        # Read the CSV file
        try:
            data = pd.read_csv(csv_file)
            print("CSV file content:")
            print(data)
        except Exception as e:
            print("Error reading CSV file:", e)
            self.fail("Failed to read CSV file")

    @patch('pyshark.FileCapture')
    def test_process_packet_error_handling(self, mock_FileCapture):
        # Mock argparse arguments
        capture_file = 'test_capture.pcapng'
        csv_file = 'test_output.csv'
        ip_address = '192.168.0.1'
        
        # Mock packets for testing, including one packet with missing attributes
        mock_packets = [
            MagicMock(ip={'src': '192.168.0.1', 'dst': '192.168.0.2'}, sniff_time='2024-05-07 12:00:00', transport_layer='TCP', length=100),
            MagicMock(ip={'src': '192.168.0.2'}, sniff_time='2024-05-07 12:00:01', transport_layer='UDP', length=200),  # Packet with missing 'dst' attribute
        ]
        
        # Set up mock FileCapture instance
        mock_cap = mock_FileCapture.return_value
        mock_cap.__iter__.return_value = iter(mock_packets)
        
        # Call the function to be tested
        save_packet_data_to_csv(capture_file, csv_file, ip_address)
        
        # Read the CSV file
        try:
            data = pd.read_csv(csv_file)
            print("CSV file content:")
            print(data)
        except Exception as e:
            print("Error reading CSV file:", e)
            self.fail("Failed to read CSV file")


if __name__ == '__main__':
    unittest.main()
