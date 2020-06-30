import RPi.GPIO as GPIO
import math, time, queue, signal, json
import _thread, threading

from urllib.request import Request, urlopen

from datetime import datetime
from enum import Enum

from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.render import canvas
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT, SINCLAIR_FONT

"""
  Basic utilities for the class LED matrix which can be reused for other purposes
"""

class TermText():
  RED = "\u001b[31m"
  GREEN = "\u001b[32m"
  WHITE = "\u001b[37]"
  RESET = "\u001b[0m"
  BOLD = "\u001b[1m"
  BACKGROUND_YELLOW = "\u001b[43;1m"
  BACKGROUND_RED = "\u001b[41;1m"
  BACKGROUND_BLACK = "\u001b[0m"

class Led():
  """
    Main class for manipulation of LED matrx with core methods below:

    1. run(): Main method which should be called to run the display consisting of
        a. Initiialising threads
        b. Process inputs and outputs
        c. Terminate the program appropriately

    2. display(): Manipulate what is shown on the LED
  """
  def __init__(self, width=32, height=8, block_orientation=-90):
    serial = spi(port=0, device=0, gpio=noop())
    self.device = max7219(serial, width=width, height=height, block_orientation=block_orientation)
    self.virtual = viewport(self.device, width=width, height=height)

    # Clears image on device
    self.device.clear()

    # Task Queue
    self.tasks = queue.Queue()

    # Display config
    self.led_attrs = {
            "display": "show",
            "display_mode": "message",
            "contrast" : "10",
            "message": "tbptbp",
            "power": "on"
    }
    self.git_repos = []
    self.threads = []

    # Some required locks
    self.io_lock = threading.RLock()
    self.attr_lock = threading.RLock()

  """
    Methods for printing to the terminal
  """
  def io_print(self, message, c_before=TermText.RESET, c_after=TermText.RESET):
    self.io_lock.acquire()
    try:
      print("{}{}{}".format(c_before, message, c_after))
    finally:
      self.io_lock.release()

  def get_input(self, prompt=''):
    self.io_lock.acquire()
    try:
      input_str = input(prompt)
      return input_str
    finally:
      self.io_lock.release()

  def program_print(self, message, c_before=TermText.RESET, bkgd_before=TermText.RESET, c_after=TermText.RESET, bkgd_after=TermText.RESET):
    self.io_lock.acquire()
    try:
      print("{}{}System: {}{}{}".format(c_before, bkgd_before, message, c_after, bkgd_after))
    finally:
      self.io_lock.release()

  def set_led_attrs(self, new_attrs):
    for k,v in new_attrs.items():
      if not(k in self.led_attrs):
        continue
      self.attr_lock.acquire()
      self.led_attrs[k] = v
      self.attr_lock.release()
    self.io_print(json.dumps(self.led_attrs, indent=2))
  """
    Main functionalities of the LED class starts here
  """

  def run(self):
    input_worker = threading.Thread(target=self.read_keyboard_input)
    input_proc_worker = threading.Thread(target=self.input_processor)
    display_worker = threading.Thread(target= self.display)

    self.threads.append(input_worker)
    self.threads.append(input_proc_worker)
    self.threads.append(display_worker)

    for t in self.threads:
      t.start()

    try:
      for t in self.threads:
        t.join()
    except KeyboardInterrupt:
      pass
    except:
      self.program_print("Threads cannot be initialised...", c_before=TermText.WHITE, c_after=TermText.BACKGROUND_RED)
    self.device.cleanup()

  def read_keyboard_input(self):
    """
      Reads input from the keyboard then add it to the task queue for the worker to process it
      Each line of input has a limit of 10s due to locking mechanism of printing to stdscr
      which may block the process of other threads for too long
    """
    x = 0
    while self.led_attrs['power'] == 'on':
      prompt = '{}In[{}]: {}'.format(TermText.GREEN, x, TermText.RESET)
      timeout = 10
      timer = threading.Timer(timeout, _thread.interrupt_main)
      try:
        timer.start()
        input_str = self.get_input(prompt).lower()
      except KeyboardInterrupt:
        continue
      finally:
        timer.cancel()
      self.tasks.put(input_str)
      if (input_str == 'quit'):
        output_str = "Exiting..."
        break
      else:
        output_str = "{}Type{} 'quit' {}to terminate program!".format(TermText.RESET, TermText.BOLD, TermText.RESET)
      self.io_print("Out[{}]: {}".format(x, output_str), c_before=TermText.RED, c_after=TermText.RESET)
      x += 1
    self.program_print("Read keyboard input Thread done!", c_before=TermText.WHITE, bkgd_before=TermText.BACKGROUND_YELLOW)

  def input_processor(self):
    """
      Worker that handles the tasks in the task queue
    """
    while self.led_attrs['power'] == 'on':
      if self.tasks.empty():
        continue
      input_str = self.tasks.get()
      if (input_str == 'quit'):
        self.led_attrs['power'] = 'off'
        continue
      elif (input_str == 'help'):
        self.io_print(json.dumps(self.led_attrs, indent=2))
        continue
      try:
        kv_list = [x.strip() for x in input_str.split(' ')]
        kv_dict = dict(s.split('=') for s in kv_list)
      except:
        self.program_print("Invalid command: {}\nPlease try <attribute>=<value>".format(input_str),
                c_before=TermText.WHITE, bkgd_before=TermText.BACKGROUND_RED)
        continue
      self.set_led_attrs(kv_dict)
    self.program_print("Input Processor Thread done!", c_before=TermText.WHITE, bkgd_before=TermText.BACKGROUND_YELLOW)


  def get_github_api(self):
    time = datetime.now()
    if (time.minute % 15 != 0) and len(self.git_repos) > 0:
      return

    PATH = '/home/pi/secret/github.json'
    with open(PATH, 'r') as githubfile:
      data = json.load(githubfile)

    url = "{}/users/{}/repos".format(data["url"], data["user"])
    request = Request(url)
    request.add_header('Authorization', 'token: {}'.format(data['token']))
    response = urlopen(request)
    repo = json.loads(response.read().decode('utf-8'))
    self.git_repos = [r["name"] for r in repo]


  def clock_display(self):
    """ """
    with canvas(self.virtual) as led_canvas:
      date_time = datetime.now()
      cur_time = date_time.strftime("%H:%M")
      hour = date_time.hour
      text(led_canvas, (1, 0), cur_time, fill="red", font=proportional(SINCLAIR_FONT))
    time.sleep(1)

  def text_display(self):
    """ """
    self.get_github_api()
    with canvas(self.virtual) as led_canvas:
      show_message(self.device, self.led_attrs['message'], fill="red", font=proportional(SINCLAIR_FONT))
      for repo in self.git_repos:
        show_message(self.device, repo, fill="red", font=proportional(LCD_FONT))
    time.sleep(1)


  def display(self):
    while self.led_attrs['power'] == 'on':
      self.device.contrast(int(self.led_attrs['contrast']))
      if (self.led_attrs['display'] == 'show'):
        self.device.show()
      else:
        self.device.hide()
      if (self.led_attrs['display_mode'] == 'clock'):
        self.clock_display()
      else:
        self.text_display()
    self.program_print("Display Thread Done!", c_before=TermText.WHITE, bkgd_before=TermText.BACKGROUND_YELLOW)

def main():
  dot_matrix = Led()
  dot_matrix.run()

if __name__ == '__main__':
    main()

