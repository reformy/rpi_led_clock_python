import datetime
from time import sleep

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2)
seg = sevensegment(device)
seg.text = "eeeeHHHHoooollll"


def str_if_not_zero(n: int) -> str:
	return str(n) if n else ''


while True:
	now = datetime.datetime.now()
	print (f'time: {now.hour}, {now.minute}')
	h1 = str(now.hour % 10)
	h2 = str_if_not_zero(now.hour // 10)
	sig.text = '{hour1}{hour2}'
        m1 = str(now.min % 10)
        m2 = str(now.min // 10)
	sig.text = '{h1}{h2}{m1}{m2}'
	sleep(1)

