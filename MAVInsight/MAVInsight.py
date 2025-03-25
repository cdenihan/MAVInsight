import mavlink_connector

def main():
    # Connect to the drone
    connection = mavlink_connector.connect_to_drone()
    
    if connection:
        print("Successfully connected to drone")
        # The connection object is now available for use
        return connection
    else:
        print("Failed to connect to drone")
        return None

if __name__ == "__main__":
    # Run the main function
    drone_connection = main()
    
    if drone_connection:
        print("Connection established. Connection object available for use.")
        # You can now use drone_connection for further operations
