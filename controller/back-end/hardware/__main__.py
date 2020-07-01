import threading

from hardware.clock import Led

if __name__ == "__main__":
    LED = Led(cli=True)
    led_thread = threading.Thread(target=LED.run)
    led_thread.start()
    led_thread.join()
