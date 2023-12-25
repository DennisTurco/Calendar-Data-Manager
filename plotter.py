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
    
    data = None
    
    def __init__():
        pass
    
    def loadData(self, filepath):
        try: 
            # Load data from the CSV file
            self.data = pd.read_csv(filepath, sep='|', header=None, encoding='utf-8')
            self.data.columns = ['col1', 'col2', 'col3', 'col4', 'col5']
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
            
    def graph():
        plt.show()