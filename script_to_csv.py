import pyshark
import csv

def process_packet(packet, ip_address):
    """
    Process a single packet and return the relevant data if it matches the given IP address.
    
    Args:
    - packet: A PyShark packet object
    - ip_address: The IP address to filter the data by
    
    Returns:
    - A tuple containing the packet data (time, source IP, destination IP, protocol, length) if it matches the IP address,
      otherwise None
    """
    try:
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst

        if ip_address == src_ip or ip_address == dst_ip:
            time = packet.sniff_time
            protocol = packet.transport_layer
            length = packet.length

            if ip_address == src_ip:
                direction = 'Source'
            else:
                direction = 'Destination'

            return (time, src_ip, dst_ip, protocol, length, direction)

    except AttributeError:
        # Handle packets without the expected attributes
        pass

    return None

def save_packet_data_to_csv(capture_file, csv_file, ip_address):
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(['Time', 'Source IP', 'Destination IP', 'Protocol', 'Length'])

        cap = pyshark.FileCapture(capture_file)

        for packet in cap:
            try:
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst

                # Check if the provided IP address is either the source or destination IP
                if ip_address == src_ip or ip_address == dst_ip:
                    time = packet.sniff_time
                    protocol = packet.transport_layer
                    length = packet.length

                    # Determine whether the IP address is the source or destination
                    if ip_address == src_ip:
                        direction = 'Source'
                    else:
                        direction = 'Destination'

                    # Write the data to the CSV file
                    csv_writer.writerow([time, src_ip, dst_ip, protocol, length])
                    
            except AttributeError:
                # Handle packets without the expected attributes
                pass

# Add a main guard to make the script executable
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Capture Wireshark data and save to CSV, filtering by IP address.')
    parser.add_argument('capture_file', type=str, help='Path to the Wireshark capture file (PCAP or PCAPNG).')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file where data will be saved.')
    parser.add_argument('ip_address', type=str, help='IP address to filter the data by.')

    args = parser.parse_args()

    save_packet_data_to_csv(args.capture_file, args.csv_file, args.ip_address)
    print(f'Data from {args.capture_file} for IP {args.ip_address} has been saved to {args.csv_file}')