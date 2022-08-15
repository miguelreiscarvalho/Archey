import threading
import time
from main import main, pressionar, button_right, click, cap, cv

threading.Thread(target=main).start()

time.sleep(0.5)
threading.Thread(target=click).start()

time.sleep(0.5)
threading.Thread(target=pressionar).start()

time.sleep(0.5)
button_right()

cap.release()
cv.destroyAllWindows()
