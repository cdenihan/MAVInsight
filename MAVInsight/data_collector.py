"""
This module provides functionality for collecting and storing MAVLink data from drones.
It captures various telemetry messages like attitude and position data, processes them
into structured formats, and allows retrieving the collected data for analysis.
"""

import time
import threading
import pandas as pd

class DataCollector:
    """
    A class for collecting and storing MAVLink data from drones.
    
    Takes a MAVLink connection as input, provides storage for collected data,
    and includes flags to control when collection is running.
    """

    def __init__(self, mavlink_connection):
        """
        Initialize the DataCollector with a MAVLink connection.
        
        Args:
            mavlink_connection: The MAVLink connection to use for data collection.
        """
        # Store the MAVLink connection
        self.connection = mavlink_connection

        # Data storage for different message types
        self.attitude_data = []
        self.position_data = []

        # Flags for controlling collection
        self.running = False
        self.collection_thread = None
        # Define which message types to collect
        self.message_types = {
            "ATTITUDE": self._process_attitude_message,
            "GLOBAL_POSITION_INT": self._process_position_message
        }
    def start_collection(self):
        """
        Start collecting MAVLink data in a background thread.
        Sets the running flag to True and starts the collection thread.
        """
        # Start a background thread for collection
        self.running = True
        self.collection_thread = threading.Thread(target=self._collection_loop)
        self.collection_thread.start()

    def stop_collection(self):
        """
        Stop collecting data.
        
        """
        # Stop the collection thread
        self.running = False
        self.collection_thread.join()

    def _collection_loop(self):
        """
        Main collection loop that runs in a background thread.
        
        Waits for messages of interest, processes them based on type, and stores the data.
        Continuously processes messages while the running flag is True.
        """
        while self.running:
            # Wait for a message
            msg = self.connection.recv_msg()
            if msg is not None:
                # Process the message based on type
                if msg.get_type() in self.message_types:
                    data = self.message_types[msg.get_type()](msg)
                    if data:
                        # Store the processed data
                        if msg.get_type() == "ATTITUDE":
                            self.attitude_data.append(data)
                        elif msg.get_type() == "GLOBAL_POSITION_INT":
                            self.position_data.append(data)
    def _process_attitude_message(self, msg):
        """
        Process an ATTITUDE message.
        
        Args:
            msg: The MAVLink ATTITUDE message to process.
        Returns:
            dict: A dictionary containing timestamp, roll, pitch, and yaw values.
        """
        # Extract roll, pitch, yaw values
        roll = msg.roll
        pitch = msg.pitch
        yaw = msg.yaw

        # Add timestamp
        timestamp = time.time()

        # Format into a dictionary
        data = {
            "timestamp": timestamp,
            "roll": roll,
            "pitch": pitch,
            "yaw": yaw
        }

        return data
    def _process_position_message(self, msg):
        """
        Process a GLOBAL_POSITION_INT message.
        
        Args:
            msg: The MAVLink GLOBAL_POSITION_INT message to process.
            
        Returns:
            dict: A dictionary containing timestamp, latitude, longitude, and altitude values.
                  Values are converted to appropriate units if needed.
        """
        # Extract latitude, longitude, altitude
        lat = msg.lat
        lon = msg.lon
        alt = msg.alt
        # Add timestamp
        timestamp = time.time()

        # Format into a dictionary
        data = {
            "timestamp": timestamp,
            "latitude": lat,
            "longitude": lon,
            "altitude": alt
        }
        return data

    def get_collected_data(self, message_type=None):
        """
        Return collected data based on message type.
        Args:
            message_type (str, optional): The type of message to return data for.
                                         If None, returns all data. Defaults to None.
        Returns:
            pandas.DataFrame or dict: If message_type is specified, returns a DataFrame
                                     for that type. Otherwise, returns a dictionary of
                                     DataFrames keyed by message type.
        """
        # Return collected data based on message type
        if message_type:
            if message_type == "ATTITUDE":
                return pd.DataFrame(self.attitude_data)
            if message_type == "GLOBAL_POSITION_INT":
                return pd.DataFrame(self.position_data)
            return None
        return {
            "ATTITUDE": pd.DataFrame(self.attitude_data),
            "GLOBAL_POSITION_INT": pd.DataFrame(self.position_data)
        }
