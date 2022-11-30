"""
Flask Run TEST
"""
import sys

from ProgramFiles.flaskr import app

# .pycを作成しない
sys.dont_write_bytecode = True

if __name__ == "__main__":
    app.run(
        host="192.168.0.96",
        port=80,
        debug=True,
        threaded=True
    )
