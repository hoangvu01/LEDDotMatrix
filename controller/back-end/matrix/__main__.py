import threading
from hardware.clock import Led

from matrix import app, LED
import matrix.control

def init_display():
   LED.run()

if __name__ == '__main__':
    led_thread = threading.Thread(target=init_display)
    led_thread.start()
    app.run(host='0.0.0.0')

    try:
        led_thread.join()
    except:
        pass


