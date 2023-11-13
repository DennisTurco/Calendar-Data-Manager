import json

JSON_PATH = "settings/session.json"

class SJONSettings:
    def __init__():
        pass
    
    @staticmethod
    def ReadFromJSON():
        try:
            fileObject = open(JSON_PATH, "r")
            jsonContent = fileObject.read()
            list = json.loads(jsonContent)
            return list
        except:
            return None
            
    @staticmethod
    def WriteToJSON(credentials_path: str, token_path: str):
        if credentials_path == None or len(credentials_path) == 0: Exception("Credentials path can't be empty")
        if token_path == None or len(token_path) == 0: Exception("Token path can't be empty")
        
        # check for '\\' on string path
        credentials_path = credentials_path.replace('\\\\', '\\')
        token_path = token_path.replace('\\\\', '\\')
        
        res = {"CredentialsPath":credentials_path, "TokenPath":token_path}
        jsonString = json.dumps(res)
        jsonFile = open(JSON_PATH, "w")
        jsonFile.write(jsonString)
        jsonFile.close()