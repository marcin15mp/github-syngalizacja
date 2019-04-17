#Projekt sygnalizacji świetlnej do obsługi sygnalizacji świetlnej realizowany na platformie Raspberry Pi 
#Importowanie bibliotek do obsługi GPIO, timera
import RPi.GPIO as GPIO
import time

# --- Przypianie oznaczeniom z tablicy konkretnych numerów portów GPIO - numeracja z płytki RPi ---

#Światła północ-południe samochody
L4 = 2		#czerwone
L5 = 3		#pomarańczowe
L6 = 4		#zielone

#Światła wschód-zachód samochody
L1 = 17		#czerwone
L2 = 27		#pomarańczowe
L3 = 22		#zielone

#Światła wschód-zachód piesi
L7 = 9		#czerwone
L8 = 11		#zielone

#Światła północ-południe piesi
L9 = 8		#czerwone
L10 = 7		#zielone

# --- Czasy świecenia i ilość mignięć świateł (jednostka to sekunda) ---
# --- Czas świecenia czerwonego jest determinowany czasem świecenia zielonego na jezdni prostopadłej ---
timeGreenPP = 10;	#czas świecenia światła zielonego północ-południe dla samochodów
timeGreenWZ = 10;	#czas świecenia światła zielonego wschód-zachód dla samochodów
timeAllRed = 2;		#czas gdy wszystko jest czerwone - czas na opuszczenie skrzyżowania

blinkingTime = 0.5	#czas zgaszenia i świecenia zielonego dla pieszych gdy zaczyna migać

#Funkcja inicjalizacyjna - tutaj konfigurujemy wszystkie potrzebne porty GPIO płytki Raspberry Pi
def initGPIO():
	GPIO.setmode(GPIO.BOARD)	#numeracja tak jak na płytce RPI
	GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)
    GPIO.setup(L5, GPIO.OUT)
    GPIO.setup(L6, GPIO.OUT)
    GPIO.setup(L7, GPIO.OUT)
    GPIO.setup(L8, GPIO.OUT)
    GPIO.setup(L9, GPIO.OUT)
    GPIO.setup(L10, GPIO.OUT)
	pass

#Funkcja z główną pętlą programu
def loop():
	try:
		while True:
			#Startujemy w stanie: północ-południe mają światło zielone, a wschód-zachód czerwone
			print ("WZ: C--  C-")
			print ("PP: --Z  -Z")
			
				#Światła północ-południe samochody
				GPIO.output(L4, GPIO.LOW)
				GPIO.output(L5, GPIO.LOW)
				GPIO.output(L6, GPIO.HIGH)
				#Światła wschód-zachód samochody
				GPIO.output(L1, GPIO.HIGH)
				GPIO.output(L2, GPIO.LOW)
				GPIO.output(L3, GPIO.LOW)
				#Światła wschód-zachód piesi
				GPIO.output(L7, GPIO.HIGH)
				GPIO.output(L8, GPIO.LOW)
				#Światła północ-południe piesi
				GPIO.output(L9, GPIO.LOW)
				GPIO.output(L10, GPIO.HIGH)
			
			#Oczekiwanie na początek procedury migania świateł dla pieszych
			time.sleep(timeGreenPP - 3*2*blinkingTime)
			
			#Miganie światłami pieszych na osi północ-południe
			#Zgaś zielone północ-południe (piesi)
			print ("PP: --Z  --")
			GPIO.output(L10, GPIO.LOW)
			time.sleep(blinkingTime)
			#Zapal zielone północ-południe (piesi)
			print ("PP: --Z  -Z")
			GPIO.output(L10, GPIO.HIGH)
			time.sleep(blinkingTime)
			#Zapalamy pomarańczowe na osi północ-południe i dalej migamy
			GPIO.output(L5, GPIO.HIGH)
			GPIO.output(L6, GPIO.LOW)
			for i in range(2):
				#Zgaś zielone północ-południe (piesi)
				print ("PP: -P-  --")
				GPIO.output(L10, GPIO.LOW)
				time.sleep(blinkingTime)
				#Zapal zielone północ-południe (piesi)
				print ("PP: -P-  -Z")
				GPIO.output(L10, GPIO.HIGH)
				time.sleep(blinkingTime)
				
			#Zapalenie natychmiast po tym czerwonego dla pieszych i samochodów północ-południe (czyli dla wszystkich)
			print ("PP: C--  C-")
			#Światła północ-południe samochody
			GPIO.output(L4, GPIO.HIGH)
			GPIO.output(L5, GPIO.LOW)
			GPIO.output(L6, GPIO.LOW)
			#Światła wschód-zachód samochody
			GPIO.output(L1, GPIO.HIGH)
			GPIO.output(L2, GPIO.LOW)
			GPIO.output(L3, GPIO.LOW)
			#Światła wschód-zachód piesi
			GPIO.output(L7, GPIO.HIGH)
			GPIO.output(L8, GPIO.LOW)
			#Światła północ-południe piesi
			GPIO.output(L9, GPIO.HIGH)
			GPIO.output(L10, GPIO.LOW)
			
			#Czekamy na opuszczenie skrzyżowania
			time.sleep(timeAllRed)
			
			#Zapalamy pomarańczowe wschód-zachód
			print ("WZ: CP-  C-")
			GPIO.output(L2, GPIO.HIGH)
			time.sleep(4*blinkingTime) #na 2 sekundy
			
			#Zapalamy nową konfigurację - zielone na osi wschód-zachód
			print ("PP: C--  C-")
			print ("WZ: --Z  -Z")
			#Światła północ-południe samochody
			GPIO.output(L4, GPIO.HIGH)
			GPIO.output(L5, GPIO.LOW)
			GPIO.output(L6, GPIO.LOW)
			#Światła wschód-zachód samochody
			GPIO.output(L1, GPIO.LOW)
			GPIO.output(L2, GPIO.LOW)
			GPIO.output(L3, GPIO.HIGH)
			#Światła wschód-zachód piesi
			GPIO.output(L7, GPIO.LOW)
			GPIO.output(L8, GPIO.HIGH)
			#Światła północ-południe piesi
			GPIO.output(L9, GPIO.HIGH)
			GPIO.output(L10, GPIO.LOW)
			
			#Oczekiwanie na początek procedury migania świateł dla pieszych
			time.sleep(timeGreenWZ - 3*2*blinkingTime)
			
			#Miganie światłami pieszych na osi wschód-zachód
			#Zgaś zielone wschód-zachód (piesi)
			print ("WZ: --Z  --")
			GPIO.output(L8, GPIO.LOW)
			time.sleep(blinkingTime)
			#Zapal zielone wschód-zachód (piesi)
			print ("WZ: --Z  -Z")
			GPIO.output(L8, GPIO.HIGH)
			time.sleep(blinkingTime)
			#Zapalamy pomarańczowe na osi wschód-zachód i dalej migamy
			GPIO.output(L2, GPIO.HIGH)
			GPIO.output(L3, GPIO.LOW)
			for i in range(2):
				#Zgaś zielone wschód-zachód (piesi)
				print ("WZ: -P-  --")
				GPIO.output(L8, GPIO.LOW)
				time.sleep(blinkingTime)
				#Zapal zielone wschód-zachód (piesi)
				print ("WZ: -P-  -Z")
				GPIO.output(L8, GPIO.HIGH)
				time.sleep(blinkingTime)
				
			#Zapalenie natychmiast po tym czerwonego dla pieszych i samochodów wschód-zachód (czyli dla wszystkich)
			print ("WZ: C--  C-")
			#Światła północ-południe samochody
			GPIO.output(L4, GPIO.HIGH)
			GPIO.output(L5, GPIO.LOW)
			GPIO.output(L6, GPIO.LOW)
			#Światła wschód-zachód samochody
			GPIO.output(L1, GPIO.HIGH)
			GPIO.output(L2, GPIO.LOW)
			GPIO.output(L3, GPIO.LOW)
			#Światła wschód-zachód piesi
			GPIO.output(L7, GPIO.HIGH)
			GPIO.output(L8, GPIO.LOW)
			#Światła północ-południe piesi
			GPIO.output(L9, GPIO.HIGH)
			GPIO.output(L10, GPIO.LOW)
			
			#Czekamy na opuszczenie skrzyżowania
			time.sleep(timeAllRed)
			
			#Zapalamy pomarańczowe północ-południe, czyli początek nowego cyklu
			print ("PP: CP-  C-")
			GPIO.output(L5, GPIO.HIGH)
			time.sleep(4*blinkingTime) #na 2 sekundy
	finally:
		GPIO.cleanup()
	
	
initGPIO()
loop()	
