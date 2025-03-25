"""
MAVLink Connector Module.

This module provides functionality for connecting to drones using the MAVLink protocol.
It offers a simple interface to establish connections to UAVs via various connection methods
(UDP, TCP, serial, etc.) and handles the initial communication handshake.
"""

from pymavlink import mavutil


def connect_to_drone(connection_string="udp:localhost:14550"):
    """
    Connect to a drone using MAVLink protocol.
    
    Args:
        connection_string: MAVLink connection string (e.g., 'udp:localhost:14550', 
                          'tcp:localhost:5760', '/dev/ttyUSB0', etc.)
    
    Returns:
        A mavlink connection object if successful
    """
    try:
        # Create a connection
        connection = mavutil.mavlink_connection(connection_string)
        # Wait for the heartbeat message to confirm connection
        print("Waiting for heartbeat...")
        connection.wait_heartbeat()
        print(f"Connected to drone (system: {connection.target_system}, "
              f"component: {connection.target_component})")
        return connection
    except (ConnectionError, TimeoutError, OSError, ValueError) as e:
        print(f"Connection failed: {e}")
        return None
