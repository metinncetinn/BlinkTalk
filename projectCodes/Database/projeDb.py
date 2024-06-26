import pypyodbc

db = pypyodbc.connect(
    'Driver={SQL Server};'
    'Database sunucu isminiz;'
    'Database= Database isminiz;'
    'Trusted_Connection=True;'
    'Connection Timeout=30;'
)

imlec = db.cursor()

def dbInsertSorular(soru):#Soru Ekleme
    komut = 'INSERT INTO tblSorular (soru) VALUES (?)'
    imlec.execute(komut, (soru,))
    db.commit()

def dbInsertCevaplar(cevap):#Cevap Ekleme
    komut = 'INSERT INTO tblCevaplar (cevap) VALUES (?)'
    imlec.execute(komut, (cevap,))
    db.commit()

def dbInsertSoruCevap(soru,cevap):#Sorulara Cevap Bağlama
    komut = "INSERT INTO tblSoruCevap (soruId, cevapId) VALUES ((SELECT id FROM tblSorular WHERE soru = ?),(SELECT id FROM tblCevaplar WHERE cevap = ?))"
    imlec.execute(komut, (soru,cevap))
    db.commit()

def dbUpdateKullanimSayisi(soru,cevap):#Kullanım sayısını 1 arttırır.
    imlec.execute("select kullanimSayisi from tblSoruCevap where soruId=(select top 1 tblSoruCevap.soruId from tblSoruCevap inner join tblSorular on tblSorular.id=tblSoruCevap.soruId where soru=?) and cevapId=(select top 1 tblSoruCevap.cevapId from tblSoruCevap inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId where cevap=?)", (soru,cevap))
    eskiIdDizi = imlec.fetchall()
    eskiId = int(eskiIdDizi[0][0])
    yeniId=eskiId+1
    imlec.execute("select tblSoruCevap.soruId,tblSoruCevap.cevapId  from tblSoruCevap inner join tblSorular on tblSorular.id=tblSoruCevap.soruId inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId where  soru=? and cevap=?", (soru,cevap))
    cevapIdDizi = imlec.fetchall()
    soruId= int(cevapIdDizi[0][0])
    cevapId = int(cevapIdDizi[0][1])
    imlec.execute('UPDATE tblSoruCevap SET kullanimSayisi = ? WHERE soruId = ? and cevapId= ?', (yeniId, soruId, cevapId))
    db.commit()

def dbCokKullanilmislar(soru):#Herhangi bir soruya verilen cevaplardan maksimumu
    imlec.execute("select top 2 tblCevaplar.cevap from tblSoruCevap inner join tblCevaplar on tblCevaplar.id=tblSoruCevap.cevapId inner join tblSorular on tblSorular.id=tblSoruCevap.soruId where soru=? ORDER BY kullanimSayisi DESC", (soru,))
    cokKullanilmisCevapDizi=imlec.fetchall()
    cokKullanilmisCevap=[]
    cokKullanilmisCevap.append(cokKullanilmisCevapDizi[0][0])#En çok verilen cevapların ilki kaydedileni.
    cokKullanilmisCevap.append(cokKullanilmisCevapDizi[1][0])#En çok verilen cevapların ikincisi kaydedileni.
    return cokKullanilmisCevap

def dbKacCevapVar(soru):#Soruya kaç kere farklı cevap verildiğini gösterir
    imlec.execute("select count(soruId) from tblSoruCevap where soruId=(select id from tblSorular where soru=?)", (soru,))
    kereVar=imlec.fetchall()
    kereVar=kereVar[0][0]
    return int(kereVar)

def dbSoruVarMi(soru):#Soru databasede vara
    imlec.execute("SELECT id FROM tblSorular WHERE soru=?", (soru,))
    var=imlec.fetchall()
    if (var):
        return True
    else:
        return False

def dbCevapVarMi(cevap):#Cevap databasede varsa
    imlec.execute("SELECT id FROM tblCevaplar WHERE cevap=?", (cevap,))
    var=imlec.fetchall()
    if (var):
        return True
    else:
        return False

def dbSoruCevapVarMi(soru,cevap):#Cevap databasede varsa
    imlec.execute("select kullanimSayisi from tblSoruCevap where cevapId=(select id from tblCevaplar where cevap=?) and soruId=(select id from tblSorular where soru=?)", (cevap,soru))
    var=imlec.fetchall()
    if (var):
        return True
    else:
        return False

def dbOzelMi(soru):
    imlec.execute("SELECT cevap FROM tblOzel inner join tblCevaplar on tblCevaplar.id=tblOzel.cevapId inner join tblSorular on tblSorular.id=tblOzel.soruId WHERE soru=?", (soru,))
    var=imlec.fetchall()
    if (var):
        return var[0][0]
    else:
        return False

#soru = "what is your name"
#cevap = "hello"
#dbInsertSorular(soru)
#dbInsertCevaplar(cevap)
#dbInsertSoruCevap(soru,cevap)
#dbUpdateKullanimSayisi(soru,cevap)
#print(dbCokKullanilmislar(soru))
#dbKacCevapVar(soru)
#dbSoruVarMi(soru)
#dbCevapVarMi(cevap)
#dbSoruCevapVarMi(soru,cevap)
"""
if dbOzelMi(soru):
    print(dbOzelMi(soru))
"""