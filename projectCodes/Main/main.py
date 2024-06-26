from socket import *
import sys
import time
sys.path.append("path to your codes")
from TTS.speech_synthesis import text_to_speech
from STT.stt import sestt
from Database.projeDb import *
from AI.ai import yapayZekaSor
from BlinkDedector import *

# UDP client oluşturma.
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_message(clientSocket, serverName, serverPort, message):
    clientSocket.sendto(message.encode(), (serverName, serverPort))

def receive_message(clientSocket):
    try:
        modifiedMessage, _ = clientSocket.recvfrom(1024)
        decodedMessage = modifiedMessage.decode()
        if not modifiedMessage:
            return None
        return int(decodedMessage)
    except OSError:
        return None

# Cevap üretme
def cevapUret(Soru):
    global dbGuncelle
    verilenCevaplar = []
    if dbOzelMi(Soru):
        cevap1 = dbOzelMi(Soru)
        cevap2 = dbOzelMi(Soru)
        verilenCevaplar.append(cevap1)
        verilenCevaplar.append(cevap2)
        dbGuncelle = False
        return verilenCevaplar
    elif dbKacCevapVar(Soru) > 1:
        cevap3 = dbCokKullanilmislar(Soru)[0]
        cevap4 = dbCokKullanilmislar(Soru)[1]
        verilenCevaplar.append(cevap3)
        verilenCevaplar.append(cevap4)
        dbGuncelle = True
        return verilenCevaplar
    else:
        cevap5 = yapayZekaSor(Soru)[0]
        cevap6 = yapayZekaSor(Soru)[1]
        verilenCevaplar.append(cevap5)
        verilenCevaplar.append(cevap6)
        dbGuncelle = True
        return verilenCevaplar

# Ana döngü
dbGuncelle = False

while True:
    gelenSoru = sestt()
    tekrarSor = True
    while tekrarSor:
        send_message(clientSocket, serverName, serverPort, "give")
        secimmmm = receive_message(clientSocket)
        print(secimmmm)
        seciliecekCevaplar = cevapUret(gelenSoru)
        if secimmmm == 0:
            verilenCevap = seciliecekCevaplar[0]
            tekrarSor = False
        elif secimmmm == 1:
            verilenCevap = seciliecekCevaplar[1]
            tekrarSor = False
        elif secimmmm == 2:
            continue
    # Görev sonrası database güncellemesi.
    if dbGuncelle:
        if dbSoruVarMi(gelenSoru) and dbCevapVarMi(verilenCevap):  # Soru ve cevap databasede var ise.
            if dbSoruCevapVarMi(gelenSoru, verilenCevap):  # Soru ve cevap ilişkisi var ise.
                dbUpdateKullanimSayisi(gelenSoru, verilenCevap)
            else:  # İlişki yok ise.
                dbInsertSoruCevap(gelenSoru, verilenCevap)
        elif dbSoruVarMi(gelenSoru) and not dbCevapVarMi(verilenCevap):  # Soru var cevap yok ise, cevabı ekle ve sorucevap ekle.
            dbInsertCevaplar(verilenCevap)
            dbInsertSoruCevap(gelenSoru, verilenCevap)
        elif not dbSoruVarMi(gelenSoru) and dbCevapVarMi(verilenCevap):  # Cevap var soru yok ise, soruyu ekle ve sorucevap ekle.
            dbInsertSorular(gelenSoru)
            dbInsertSoruCevap(gelenSoru, verilenCevap)
        else:  # İkisini de ayrı ayrı ekle ve toplu ekle.
            dbInsertSorular(gelenSoru)
            dbInsertCevaplar(verilenCevap)
            dbInsertSoruCevap(gelenSoru, verilenCevap)
    text_to_speech(verilenCevap)  # Cevabı seslendir.
    time.sleep(7)

clientSocket.close()
