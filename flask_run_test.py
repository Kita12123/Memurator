"""
Flask Run TEST
"""
# .pycを作成しない
import sys
sys.dont_write_bytecode = True

from ProgramFiles.flaskr import app

if __name__ == "__main__":
    app.run(
        host="192.168.0.96",
        port=80,
        debug=True,
        threaded=True
    )
