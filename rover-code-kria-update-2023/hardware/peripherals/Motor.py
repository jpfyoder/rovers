from pynq.lib.rpi import GPIO


class Motor:
    def __init__(self, pwm_pin=None):
        self.pwm_pin = pwm_pin

    def select_pwm_pin(self, pin_number):
        self.pwm_pin = Arduino_IO(pin_number, "out")

    def update_pwm(self):
        current_time = time.monotonic()
        if current_time >= self.next_toggle_time:
            if GPIO.input(self.pwm_pin) == GPIO.HIGH:
                off_time = 1 / self.frequency * (1 - (self.duty_cycle / 100))
                self.next_toggle_time = current_time + off_time
                GPIO.output(self.pwm_pin, GPIO.LOW)
            else:
                on_time = 1 / self.frequency * (self.duty_cycle / 100)
                self.next_toggle_time = current_time + on_time
                GPIO.output(self.pwm_pin, GPIO.HIGH)