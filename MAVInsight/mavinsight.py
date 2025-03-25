"""
MAVInsight main module for establishing connections with MAVLink-based drones.

This module provides the main entry point for the MAVInsight application, 
handling the connection to drones using MAVLink protocol.
"""

import mavlink_connector


def main():
    """
    Establish a connection to a drone using MAVLink protocol.
    
    Attempts to connect to a drone using the mavlink_connector module.
    
    Returns:
        connection: A connection object if successful, None otherwise.
    """
    # Connect to the drone
    connection = mavlink_connector.connect_to_drone()
    if connection:
        print("Successfully connected to drone")
        # The connection object is now available for use
        return connection
    print("Failed to connect to drone")
    return None

if __name__ == "__main__":
    # Run the main function
    drone_connection = main()
    if drone_connection:
        print("Connection established. Connection object available for use.")
        # You can now use drone_connection for further operations
