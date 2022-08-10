import threading
import time
from main import main, recvoice

threading.Thread(target=main).start()
time.sleep(0.5)
recvoice()
