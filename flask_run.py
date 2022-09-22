"""
Flask Run
"""
from ProgramFiles.log import LOGGER
from ProgramFiles.flaskr import app

if __name__=="__main__":
    LOGGER.info("*************** M emurator Run ***************")
    app.run(
        host="0.0.0.0",
        port=80,
        debug=False,
        threaded=True
    )