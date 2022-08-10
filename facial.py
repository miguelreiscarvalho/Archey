import threading
import time
from main import main, pressionar, click

threading.Thread(target=main).start()

time.sleep(0.5)
threading.Thread(target=click).start()

time.sleep(0.5)
pressionar()
