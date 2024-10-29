import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Class to detect anomalies in real-time using a sliding window of data
class AnomalyDetector:
    def __init__(self, window_size=50, threshold=3):
        # Window size for calculating rolling statistics (mean and standard deviation)
        self.window_size = window_size
        # Threshold in standard deviations to define an anomaly
        self.threshold = threshold
        # A deque to store the most recent data points (up to 'window_size' entries)
        self.data_window = deque(maxlen=window_size)
    
    # Method to detect if a new data point is an anomaly
    def detect(self, new_value):
        # Add new data point to the sliding window
        self.data_window.append(new_value)
        
        # If window is not yet full, cannot calculate statistics reliably
        if len(self.data_window) < self.window_size:
            return False  # No anomaly detection when data is insufficient
        
        # Calculate the mean and standard deviation of the values in the window
        mean = np.mean(self.data_window)
        std_dev = np.std(self.data_window)
        
        # If new value deviates from the mean by more than 'threshold' * standard deviation, it’s an anomaly
        if abs(new_value - mean) > self.threshold * std_dev:
            return True  # Anomaly detected
        return False  # No anomaly detected


# Function to generate a continuous data stream with potential anomalies
def data_stream_generator(length=1000, anomaly_prob=0.01):
    # Generate time steps from 0 to 'length'
    time = np.arange(0, length)
    
    # Define a linear trend component
    trend = 0.05 * time
    
    # Define a seasonal component using a sine wave
    seasonality = 10 * np.sin(0.1 * time)
    
    # Add random noise to simulate variability
    noise = np.random.normal(0, 1, length)
    
    # Combine trend, seasonality, and noise to create the final data stream
    data = trend + seasonality + noise
    
    # Introduce anomalies: randomly select points to alter based on 'anomaly_prob'
    anomalies = np.random.rand(length) < anomaly_prob
    data[anomalies] += np.random.choice([-30, 30], size=np.sum(anomalies))  # Anomalies as large deviations
    
    # Yield each value in the generated data stream one by one
    for value in data:
        yield value


# Function to plot the data stream in real-time and highlight anomalies
def plot_real_time(data_gen, detector):
    # Set up the plotting window
    fig, ax = plt.subplots()
    
    # Initialize lists to store time and data values for plotting
    x_data, y_data = [], []
    # List to store anomaly points for plotting separately
    anomaly_points = []
    
    # Define the update function to animate the plot in real-time
    def update(frame):
        # Add the current time frame to the x-axis data
        x_data.append(frame)
        
        # Retrieve the next value from the data generator
        y = next(data_gen)
        y_data.append(y)  # Add it to the y-axis data
        
        # Check if the current value is an anomaly
        is_anomaly = detector.detect(y)
        
        # Print each data point to the terminal, marking anomalies
        if is_anomaly:
            print(f"Time: {frame}, Value: {y} (Anomaly)")  # Print anomaly message
            anomaly_points.append((frame, y))  # Add anomaly point to the list
        else:
            print(f"Time: {frame}, Value: {y}")  # Print regular data point
        
        # Clear and update the plot for each frame
        ax.clear()
        ax.plot(x_data, y_data, label="Data Stream")  # Plot the main data stream
        
        # Plot anomalies as red points on the graph if any have been detected
        if anomaly_points:
            ax.scatter(*zip(*anomaly_points), color='red', label="Anomalies")
        
        # Configure plot labels and title
        ax.legend()
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("Real-Time Data Stream with Anomalies")
    
    # Initialize FuncAnimation to update the plot every 50 milliseconds
    ani = FuncAnimation(fig, update, interval=50, cache_frame_data=False)
    
    # Display the animated plot
    plt.show()


# Instantiate the data generator
data_gen = data_stream_generator()

# Instantiate the anomaly detector with default parameters
detector = AnomalyDetector()

# Start the real-time plotting of data stream and anomalies
plot_real_time(data_gen, detector)
