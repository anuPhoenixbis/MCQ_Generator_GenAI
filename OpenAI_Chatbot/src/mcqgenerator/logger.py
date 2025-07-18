#this file is the place where we will log messages to a file 
#By messages we mean the whatever is going around between the code execution
#like the errors, warnings, info , debug messages etc. 
import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}_genai.log"

#getting the path name and creating the logs folder in the curr dir
log_path = os.path.join(os.getcwd(),"logs") #getting the path for the logs folder in the current dir(cwd) and naming it "logs" then, passing the logs file to it
os.makedirs(log_path, exist_ok=True) #if the logs folder DNE then it will create a new one, else it won't do anything

LOG_FILEPATH = os.path.join(log_path, LOG_FILE) #join the log path and log file name to get the full path for the log file

#logging the current config
logging.basicConfig(
    level = logging.INFO, #setting the level to info, it will log all msgs
    filename = LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)