import datetime as dt
import io, subprocess, sys
import numpy as np


try:
    import pandas as pd
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas as pd
try:
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
except:
    subprocess.call([sys.executable, "-m", "pip", "install", "matplotlib"])
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties


class Plotter:
    
    def graph():
        house_prices = np.random.normal(200000, 25000, 5000)
        plt.polar(house_prices)
        plt.show()