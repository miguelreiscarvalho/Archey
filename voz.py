import threading
import time
from main import main, recvoice, cap, cv

#  threading.Thread(target=main).start()
time.sleep(0.5)
recvoice()

cap.release()
cv.destroyAllWindows()
