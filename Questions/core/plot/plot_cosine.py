
import matplotlib.pyplot as plt
import numpy as np

class PlotCosine:
    '''
        Plot Cosine line in 2D axis
    '''
    def __init__(self, amplitude : float, period : float, omega : float, x_offset : float):
        self.amplitude = amplitude
        self.period = period
        self.omega = omega
        self.x_offset = x_offset
    
    def draw(self, xlabel = "", ylabel = "", file_path = ""):
        # Period
        T = self.period
        
        # Array of time points
        t = np.linspace(0, 1.25 * T, 500)

        # Calculate points from time 
        values = self.amplitude * np.cos(self.omega * t + self.x_offset)

        # Plot
        plt.figure(figsize=(8, 6)) # Kích thước hình vẽ
        plt.plot(t, values, linewidth=2)

        # label axis
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # x ticks - based on T
        low_X = 0
        high_X = 1.3*T
        plt.xticks(np.arange(low_X, high_X, 0.5))

        #  Add horizontal lines for easy reading
        plt.grid(axis='y', linestyle='-', alpha=0.7)
        
        # Ensure 2 axis meet at 0
        ax = plt.gca()
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        # Set limites for plot
        plt.xlim(t.min(), t.max())
        plt.ylim(-self.amplitude, self.amplitude)

        # Save chart to file
        plt.savefig(file_path)


