from typing import List, Dict

class DataCSV:
    @staticmethod
    def save_data_to_file(data: Dict[str, List[str]], filepath: str, delimiter: str = "|", encoding_type: str = ""):
        if filepath is None or len(filepath) == 0: raise ValueError("File path can't be null")

        file = open(filepath, "w", encoding=encoding_type)
        counter = 0
        for ID in data.keys():
            elem = data[ID]
            elem = [str(element) for element in elem]
            line = delimiter.join(elem)
            if (counter + 1) < len(data):
                line = line + "\n"
            file.write(line)
            counter += 1
        file.close()

    @staticmethod
    def load_data_from_file(filepath: str, delimiter: str = "|") -> Dict[str, List[str]]:
        if filepath is None or len(filepath) == 0: raise ValueError("File path can't be null")

        file = open(filepath, "r")
        data = dict()
        lines = file.readlines()
        for line in lines:
            elem = line.replace("\n", "").split(delimiter)
            data_id = elem[0]
            data[data_id] = elem
        file.close()
        return data

    @staticmethod
    def add_data(data: Dict[str, List[str]], data_id: str, data_list: List[str]) -> bool:
        if data_id is None: ValueError("ID can't be null")

        if data_id not in data:
            data[data_id] = data_list
            return True
        else:
            return False