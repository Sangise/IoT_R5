import RPi.GPIO as GPIO
from time import sleep

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if adcnum > 7 or adcnum < 0:
		return -1
	GPIO.output(cspin, GPIO.HIGH)
	GPIO.output(clockpin, GPIO.LOW)
	GPIO.output(cspin, GPIO.LOW)

	commandout = adcnum
	commandout = commandout | 0x18
	commandout = commandout << 3

	for i in range(5):
		if commandout & 0x80 == 0x80:
			GPIO.output(mosipin, GPIO.HIGH)
		else:
			GPIO.output(mosipin, GPIO.LOW)
		commandout = commandout << 1
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)

	adcout = 0 #出力をすべて0に初期化
	for i in range(13):
		GPIO.output(clockpin, GPIO.HIGH)
		GPIO.output(clockpin, GPIO.LOW)
		if i == 0: #Null(無効)ビットの場合
			pass
		elif i > 0: #有効ビットの場合
			adcout = adcout << 1 #左シフト
			if GPIO.input(misopin) == GPIO.HIGH: #有効ビットがHIGH(1)の場合
				adcout = adcout | 0x1 #最後のビットに1を代入
			elif GPIO.input(misopin) == GPIO.LOW: #有効ビットがLOW(0)の場合
				adcout = adcout | 0x0 #最後のビットに0を代入

	GPIO.output(cspin, GPIO.HIGH)
	return adcout

GPIO.setmode(GPIO.BCM)
SPICLK = 11
SPIMOSI = 10
SPIMISO = 9
SPICS = 8

GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICS, GPIO.OUT)

try:
	while True:
		inputVal0 = readadc(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
		print("ADC = "+ str(inputVal0))
		sleep(1.0)

except KeyboardInterrupt:
	pass

GPIO.cleanup()