import json
from PySide6.QtWidgets import QMessageBox

CONFIG_PATH = "config.json"

def loadConfig():       
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        
        x = config["trackingPointCoords"]["x"]
        y = config["trackingPointCoords"]["y"]
        return x,y 

def validator(x, y, parent=None):
    if isinstance(x, (int)) and isinstance(y, (int)):
        if 0 <= x <= 100 and 0 <= y <= 100:
            return True

    # Show an error dialog if validation fails
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Validation Error")
    msg.setText("x and y must be numbers between 0 and 100.")
    msg.exec()
    return False

def filterMulti(x):
    x = x * 100

    return x
 
def filterMulti1(x):   
    x = x / 100

    return x

def save_config(x,y):
    if validator(x,y):
        config_data = {
            "trackingPointCoords": {
                "x": x,
                "y": y
            }
        }

        with open(CONFIG_PATH, "w") as f:
            json.dump(config_data, f, indent=4)  
        
        parent = None
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Configuration Saved")
        msg.setText("Tracking Point Config Saved")
        msg.exec()       

def resDef():
    
        config_data = {
            "trackingPointCoords": {
                "x": 50,
                "y": 4
            }
        }
        
        
        with open(CONFIG_PATH, "w") as f:
            json.dump(config_data, f, indent=4)  
        
        parent = None
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Configuration Saved")
        msg.setText("Settings restored to Defaults")
        msg.exec()       