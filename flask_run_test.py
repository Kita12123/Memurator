"""
Flask Run TEST
"""
from ProgramFiles.log import LOGGER
from ProgramFiles.flaskr import app

if __name__=="__main__":
    LOGGER.debug(f"*************** M emurator Run TEST ***************")
    app.run(
        debug=True
    )