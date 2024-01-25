from typing import List, Set, Tuple, Dict

class DataCSV:
    @staticmethod
    def saveDataToFile(data: Dict[str, List[str]], filepath: str, delimeter: str = "|", encodingType: str = None):
        if filepath == None or len(filepath) == 0: raise ValueError("File path can't be null")
        
        file = open(filepath, "w", encoding=encodingType)
        counter = 0
        for ID in data.keys():
            elem = data[ID]
            elem = [str(element) for element in elem]
            line = delimeter.join(elem)
            if (counter + 1) < len(data):
                line = line + "\n"
            file.write(line)
            counter += 1
        file.close()
    
    @staticmethod
    def loadDataFromFile(filepath: str, delimeter: str = "|") -> Dict[str, List[str]]:
        if filepath == None or len(filepath) == 0: raise ValueError("File path can't be null")
        
        file = open(filepath, "r")
        data = dict()
        lines = file.readlines()
        for line in lines:
            elem = line.replace("\n", "").split(delimeter)
            ID = elem[0]
            data[ID] = elem
        file.close()
        return data
    
    
    @staticmethod
    def addData(data: Dict[str, List[str]], ID: str, data_list: List[str]) -> bool:
        if ID == None: ValueError("ID can't be null")
        
        if ID not in data:
            data[ID] = data_list
            return True
        else:
            return False