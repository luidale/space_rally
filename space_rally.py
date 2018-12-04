# impordi tk vidinad ja konstandid
from tkinter import *
# Pythoni moodulisüsteemi ühe nüansi tõttu tuleb ttk importida eraldi
from tkinter import ttk
import time
import random
import math
import _thread
import os
import platform

if platform.platform().find("Windows") != -1:
    import winsound


#juhtnuppude funktsioonid
def nool_üles(event):
    if not tahvel.coords(img)[1]-juku_sammu_pikkus <20:
        tahvel.move(img, 0, -juku_sammu_pikkus)
    _thread.start_new_thread(h22l,(5000,50))

def nool_alla(event):
    if not tahvel.coords(img)[1]+juku_sammu_pikkus >kasti_k6rgus-20:
        tahvel.move(img, 0, juku_sammu_pikkus)
    _thread.start_new_thread(h22l,(5000,50))

def nool_vasakule(event):
    if not tahvel.coords(img)[0]-juku_sammu_pikkus <20:
        tahvel.move(img, -juku_sammu_pikkus, 0)
    _thread.start_new_thread(h22l,(5000,50))

def nool_paremale(event):
    if not tahvel.coords(img)[0]+juku_sammu_pikkus >kasti_laius-20:
        tahvel.move(img, juku_sammu_pikkus, 0)
    _thread.start_new_thread(h22l,(5000,50))

def tulista(event):
    raketi_asukoht = tahvel.coords(img)
    for i in range(len(kuulid)):
        if tahvel.coords(kuulid[i]) == [-200,-200]: #kontroll, milline kuul ei ole kasutuses
            tahvel.coords(kuulid[i],raketi_asukoht[0],raketi_asukoht[1])
            tulista_abi(kuulid[i],0)
            _thread.start_new_thread(h22l,(500,100))
            return

def h22l(sagedus,pikkus):
    if platform.platform().find("Windows") != -1:
        winsound.Beep(sagedus,pikkus)
    else:
        pass
    

def tulista_abi(kuul,plahvatuse_aeg):
    #kontrollib kaua plahvatus kestnud on ja piisava pikkuse korral muudab plahvatuse pildi asukohta
    if plahvatuse_aeg>0:
        plahvatuse_aeg+=1
    if plahvatuse_aeg==2:
        tahvel.coords(plahvatus_id,-200,-200)
        tahvel.coords(plahvatus2_id,-200,-200)
        plahvatuse_aeg=0
        return
    #kuuli edasi liikumine
    tahvel.move(kuul, 0, -10)
    kuuli_asukoht = tahvel.coords(kuul)

    #kontrollitakse, kas on veel ekraanil
    if  kuuli_asukoht[1] <0: #kui kuul jõuab üles serva või on algpunkti tagsi viidud, lõpetatakse kuuli lend ära
        tahvel.coords(kuul,-200,-200)
        return
    #kontrollitakse, kas kuul tabab kivi
    for i in range(kivide_arv):
        asukoht=tahvel.coords(kivid[i]) #kivi asukoht (x ja y)
        if (kuuli_asukoht[0] in range(int(asukoht[0]-25),int(asukoht[0]+25))) \
        and (kuuli_asukoht[1] in range(int(asukoht[1]-25),int(asukoht[1]+25))):
            tahvel.coords(kivid[i],random.randrange(0,500),-30) # kui vastu kivi minnakse, siis läheb kivi uuesti üles uue koha peale
            tahvel.coords(kuul,-200,-200) #kuuli lend lõpetatakse ära
            tahvel.coords(plahvatus2_id,asukoht[0],asukoht[1])
            plahvatuse_aeg=1
            _thread.start_new_thread(h22l,(400,300))

    # kontrollitakse, kas kuul tabab ufot
    ufo_asukoht = tahvel.coords(ufo_id)
    if (kuuli_asukoht[0] in range(int(ufo_asukoht[0]-25),int(ufo_asukoht[0]+25))) \
    and (kuuli_asukoht[1] in range(int(ufo_asukoht[1]-25),int(ufo_asukoht[1]+25))):         
            #toob plahvatuse pildi ufo kohale
            tahvel.coords(plahvatus_id,ufo_asukoht[0],ufo_asukoht[1])
            plahvatuse_aeg=1
            tahvel.coords(kuul,-200,-200) #kuuli lend lõpetatakse ära
            # tuuakse tossava ufo pilt pihta saanud ufo asemele
            tahvel.coords(ufo2_id,ufo_asukoht[0],ufo_asukoht[1])
            # esialge ufo viiakse mujale
            tahvel.coords(ufo_id,-200,-200)
            kukkuv_ufo() #tossavat ufot hakatakse liigutama
            
    raam.after(10,tulista_abi,kuul,plahvatuse_aeg) # funktsioon kutsutakse 10 ms pärast uuesti esile

# tossava ufo liigutamine
def kukkuv_ufo():
    ufo2_asukoht = tahvel.coords(ufo2_id)
    tahvel.coords(ufo2_id, round(ufo2_asukoht[0]-10*math.sin(time.localtime().tm_sec*10)),ufo2_asukoht[1]+5,)
    _thread.start_new_thread(h22l,(2000,50))
    _thread.start_new_thread(h22l,(2500,50))
    if ufo2_asukoht[1]> 600:
        return
    raam.after(100, kukkuv_ufo)

# seadistab mängu vastavalt raskus astmele
def uuenda(t2hed,punktid,counter,sekundid2,nupp, kivid, pun_t2hed,plahvatuse_aeg,kiiruse_muutmise_seisund):
    if int(spinval.get()) ==1:
        kiirus = 100
        t2htede_hulk = 30
        kivide_hulk = 10
        pun_t2htede_hulk = 3
    elif int(spinval.get()) ==2:
        kiirus = 60
        t2htede_hulk = 20
        kivide_hulk = 15
        pun_t2htede_hulk = 2
    else:
        kiirus = 45
        t2htede_hulk = 10
        kivide_hulk = 20
        pun_t2htede_hulk = 1

    uuenda_abi(t2hed,kiirus,t2htede_hulk,kivide_hulk,pun_t2htede_hulk,punktid,counter,sekundid2,nupp, kivid, pun_t2hed,plahvatuse_aeg,kiiruse_muutmise_seisund)
   
#funktsioon tähtede,kivid ja ufo liikuma panemiseks, aja arvestamiseks ja punktide lugemiseks
def uuenda_abi(t2hed,kiirus,t2htede_hulk,kivide_hulk,pun_t2htede_hulk,punktid,counter,sekundid2,nupp, kivid, pun_t2hed,plahvatuse_aeg,kiiruse_muutmise_seisund):
    #kontrollib kaua plahvatus kestnud on ja piisava pikkuse korral muudab plahvatuse pildi asukohta
    if plahvatuse_aeg>0:
        plahvatuse_aeg+=1
    if plahvatuse_aeg==2:
        tahvel.coords(plahvatus_id,-200,-200)
        tahvel.coords(suur_pun_t2ht_id,-200,-200)
        tahvel.coords(suur_t2ht_id,-200,-200)
        plahvatuse_aeg=0

    nupp.destroy() #kaotab startnupu
    tase.place(x=-230, y=-460)
    raketi_asukoht = tahvel.coords(img)

    #kollaste tähtede kontroll
    for i in range(t2htede_hulk):
        asukoht=tahvel.coords(t2hed[i]) #tähe asukoht (x ja y)
        if asukoht[1]>500: #kontroll kas y on jõudnud tahvli servani
            tahvel.coords(t2hed[i],random.randrange(0,500),0) # kui on jõudnud servani, läheb uuesti üles, ning uue koha peale
        elif (raketi_asukoht[0] in range(int(asukoht[0]-10),int(asukoht[0]+10))) \
        and (raketi_asukoht[1] in range(int(asukoht[1]-10),int(asukoht[1]+10))):  # kollase tähe ja raketi asukoha kontroll
            tahvel.coords(t2hed[i],random.randrange(0,500),0) # kui täht ära puudutatakse, siis läheb täht uuesti üles uue koha peale
            tahvel.coords(suur_t2ht_id,asukoht[0],asukoht[1]) # ja asemle tuuakse suur täht
            plahvatuse_aeg=1
            _thread.start_new_thread(h22l,(400,300))
            punktid +=1  # punktide saamine, kui tähe ja raketi asukoht enam-vähem kattuvad
            kiiruse_muutmise_seisund = True
        else:
            tahvel.coords(t2hed[i],asukoht[0],asukoht[1]+kiiruse_erinevused[i])# kui ei ole tahvli servas liigutatakse täht allapoole (erinevad tähed erineva kiirusega)
    var2.set(punktid)

    #kivide kontroll
    for i in range(kivide_hulk):
        asukoht=tahvel.coords(kivid[i]) #kivi asukoht (x ja y)
        if asukoht[1]>500: #kontroll kas y on jõudnud tahvli servani
            tahvel.coords(kivid[i],random.randrange(0,500),0) # kui on jõudnud servani, läheb uuesti üles, ning uue koha peale
        elif (raketi_asukoht[0] in range(int(asukoht[0]-25),int(asukoht[0]+25))) \
        and (raketi_asukoht[1] in range(int(asukoht[1]-25),int(asukoht[1]+25))): #kivi ja raketi asukoha kontroll
            tahvel.coords(kivid[i],random.randrange(0,500),0) # kui vastu kivi minnakse, siis läheb kivi uuesti üles uue koha peale
            tahvel.coords(plahvatus_id,raketi_asukoht[0],raketi_asukoht[1]) #toob plahvatuse pildi raketi kohale
            plahvatuse_aeg=1
            _thread.start_new_thread(h22l,(400,300))
            counter -=10 #võetakse aega maha
            
        else:
            tahvel.coords(kivid[i],asukoht[0],asukoht[1]+kiiruse_erinevused[i])# kui ei ole tahvli servas liigutatakse kivi allapoole (erinevad kivid erineva kiirusega)
    aeg.set(counter)
        
    #ufo liikumine
    ufo_asukoht=tahvel.coords(ufo_id)
    tahvel.coords(ufo_id, ufo_asukoht[0]-10,round(ufo_asukoht[1]-10*math.sin(time.localtime().tm_sec*10)))
    
    #ufo ilmumine
    if counter%10==1:
        tahvel.coords(ufo_id,560,random.randrange(100,400))
            
    for i in range(pun_t2htede_hulk):
        asukoht=tahvel.coords(pun_t2hed[i]) #punase tähe asukoht (x ja y)
        if asukoht[1]>500: #kontroll kas y on jõudnud tahvli servani
            tahvel.coords(pun_t2hed[i],random.randrange(0,500),0) # kui on jõudnud servani, läheb uuesti üles, ning uue koha peale
        elif (raketi_asukoht[0] in range(int(asukoht[0]-15),int(asukoht[0]+15))) \
        and (raketi_asukoht[1] in range(int(asukoht[1]-15),int(asukoht[1]+15))): # punase tähe ja raketi asukoha kontroll
            tahvel.coords(pun_t2hed[i],random.randrange(0,500),0) # kui täht ära puudutatakse, siis läheb täht uuesti üles uue koha peale
            tahvel.coords(suur_pun_t2ht_id,asukoht[0],asukoht[1]) # ja asemle tuuakse suur täht
            plahvatuse_aeg=1
            _thread.start_new_thread(h22l,(400,300))
            counter +=5 #aja kaotamine
    
        else:
            tahvel.coords(pun_t2hed[i],asukoht[0],asukoht[1]+kiiruse_erinevused[i])# kui ei ole tahvli servas liigutatakse täht allapoole (erinevad tähed erineva kiirusega)
    aeg.set(counter)

    # aja arvestus
    sekundid = time.localtime().tm_sec # absoluutne aeg sekundites
    if sekundid != sekundid2: # kui absoluutne aeg on muutunud
        counter -=1
    sekundid2 = sekundid
    aeg.set(counter) # muudab aega programmi aknas

    #kiiruse suurendamine iga 10 punkti järel
    if (punktid+1)%10 == 0 and kiiruse_muutmise_seisund == True:
        kiiruse_muutmise_seisund = False
        kiirus = int(kiirus/1.5)

    #mängu lõpetamine kui aeg otsa saab
    if counter <= 0:
        tulemus(punktid)
        return
    raam.after(kiirus, uuenda_abi,t2hed,kiirus,t2htede_hulk,kivide_hulk,pun_t2htede_hulk,punktid,counter,sekundid2,nupp, kivid, pun_t2hed,plahvatuse_aeg,kiiruse_muutmise_seisund) #kutsub peale pausi uuesti esile

def tulemus(punktid):
# funktsioon tulemuse ja nime salvestamiseks
    # loome akna
    tulemus = Tk()
    tulemus.title("Tulemuse salvestamine")
    tulemus.geometry("300x100")

    # loome tekstikasti jaoks sildi
    silt = ttk.Label(tulemus, text= "Nimi")
    silt.place(x=5, y=5)

    # loome tekstikasti
    nimi = ttk.Entry(tulemus)
    nimi.place(x=70, y=5, width=150)

    # loome nupu
    nupp = ttk.Button(tulemus, text="Salvesta!", command= lambda: salvesta(punktid,nimi,tulemus))
    nupp.place(x=70, y=40, width=150)

    # ilmutame akna ekraanile
    tulemus.mainloop()

def salvesta(punktid,nimi,tulemus):
    # tulemuse salvestamine
    f = open(os.path.join("data","rekord.txt"), "a")
    value = str(punktid) + " " + str(nimi.get()) + " "+ str(spinval.get())+"\n"
    s = str(value)
    f.write(s)
    f.close()
    tulemus.destroy()
    n2ita_rekord()
 
    
    startnupp() #teeb uuesti start nuppu
    
def n2ita_rekord():
    f = open(os.path.join("data",'rekord.txt'), "r")
    record_tabel1 = []
    record_tabel2 = []
    record_tabel3 = []
    for rida in f: # kõik tulemused listiks
        rekord = rida.strip().split(" ")
        if rekord[2] == str(1):
            record_tabel1.append(rekord)
        elif rekord[2] == str(2):
            record_tabel2.append(rekord)
        elif rekord[2] == str(3):
            record_tabel3.append(rekord)
    par1.set(" ")
    par2.set(" ")
    par3.set(" ")
    if int(spinval.get()) ==1:
    # try catch selle pärast, et kui rekordi faili on puudu või seal ei ole piisavalt ridu, ei tuleks error.
        try:
            sort_record = sorted(record_tabel1, key=lambda record: int(record[0]), reverse = True)
        # tulemuste listi soteerimine
            par1.set(" ".join([sort_record[0][0], "p", sort_record[0][1]]))
            par2.set(" ".join([sort_record[1][0], "p", sort_record[1][1]]))
            par3.set(" ".join([sort_record[2][0], "p", sort_record[2][1]]))
        except:
            ValueError
    # try catch selle pärast, et kui rekordi faili on puudu või seal ei ole piisavalt ridu, ei tuleks error.
    elif int(spinval.get()) ==2:
        try:
            sort_record = sorted(record_tabel2, key=lambda record: int(record[0]), reverse = True)
        # tulemuste listi soteerimine
            par1.set(" ".join([sort_record[0][0], "p", sort_record[0][1]]))
            par2.set(" ".join([sort_record[1][0], "p", sort_record[1][1]]))
            par3.set(" ".join([sort_record[2][0], "p", sort_record[2][1]]))
        except:
            ValueError
    # try catch selle pärast, et kui rekordi faili on puudu või seal ei ole piisavalt ridu, ei tuleks error.
    else:
        try:
            sort_record = sorted(record_tabel3, key=lambda record: int(record[0]), reverse = True)
        # tulemuste listi soteerimine
            par1.set(" ".join([sort_record[0][0], "p", sort_record[0][1]]))
            par2.set(" ".join([sort_record[1][0], "p", sort_record[1][1]]))
            par3.set(" ".join([sort_record[2][0], "p", sort_record[2][1]]))
        except:
            ValueError
    f.close()
    
def startnupp():
    # loome nupu alustamiseks
    nupp = ttk.Button(raam, text="Alusta!", command=lambda:uuenda(t2hed,0,m2ngu_pikkus,0,nupp, kivid, pun_t2hed,plahvatuse_aeg,kiiruse_muutmise_seisund))
    for i in range (len(t2hed)):
        tahvel.coords(t2hed[i],random.randrange(0,500),random.randrange(-500,-20)) #muudame tähtede asukohta nii, et uue mängu alguses
                                                                                #oleks need jälle alguses
    for i in range (len(kivid)):
        tahvel.coords(kivid[i],random.randrange(0,500),random.randrange(-500,-30)) #muudame kivide asukohta nii, et uue mängu alguses
    for i in range (len(pun_t2hed)):                                               #oleks need jälle alguses
        tahvel.coords(pun_t2hed[i],random.randrange(0,500),random.randrange(-500,-20)) #muudame punaste_tähtede asukohta nii, et uue müngu alguses
                                                                                     #oleks need jälle alguses
    tahvel.coords(img,250, 480) # rakett algusesse tagasi                                                    
    tahvel.coords(ufo_id,-200,-200) # ufo algusesse tagasi
    tahvel.coords(plahvatus_id,-200,-200)
    nupp.place(x=250, y=540, width=150)
    tase.place(x=30, y=460)
    
#Muutujad
juku_sammu_pikkus = 10
kiirus=100
kasti_k6rgus = 500
kasti_laius = 500
t2htede_arv = 30
kivide_arv = 20
pun_t2htede_arv = 3
m2ngu_pikkus = 40
plahvatuse_aeg=0
kiiruse_muutmise_seisund = True


#tekitame järjendi tähtede liikumikiirustega
kiiruse_erinevused=[]
for i in range(t2htede_arv):
    kiiruse_erinevused.append(random.randrange(5,15))


# loome akna
raam = Tk()
raam.title("Space Rally - Ultimate mission")  # määrame pealkirja
raam.geometry("700x700") # määrame akna suuruse

#loob kasti
tahvel = Canvas(raam, width=kasti_laius, height=kasti_k6rgus, background="white")
tahvel.grid()

# tasemed
spinval = StringVar()
tase = Spinbox(raam, width=5, textvariable=spinval, command=lambda:n2ita_rekord(),from_=1.0, to=3.0)
tase.place(x=30, y=460)


#tekitab raketi
rakett = PhotoImage(file=os.path.join("data","rocket.gif"))
img = tahvel.create_image(250, 480, image=rakett)

t2hed = []
#loob tähed (hulk tähti ja järjendisse)
t2ht = PhotoImage(file=os.path.join("data","star.gif"))
for i in range (t2htede_arv):
    t2he_id=tahvel.create_image(random.randrange(0,500),random.randrange(-500,-20), image = t2ht)
    t2hed.append(t2he_id)

#loob suure tähe
suur_t2ht = PhotoImage(file=os.path.join("data","star2.gif"))
suur_t2ht_id = tahvel.create_image(-200, -200, image=suur_t2ht)

kivid = []
#loob kivid (hulk kivisid ja järjendisse)
kivi = PhotoImage(file=os.path.join("data","asteroid.gif"))
for i in range (kivide_arv):
    kivi_id=tahvel.create_image(random.randrange(0,500),random.randrange(-500,-50), image = kivi)
    kivid.append(kivi_id)

#loob ufo 
ufo = PhotoImage(file=os.path.join("data","ufo.gif"))
ufo_id=tahvel.create_image(-200,-200, image = ufo)
#loob ufo 
ufo2 = PhotoImage(file=os.path.join("data","ufo2.gif"))
ufo2_id=tahvel.create_image(-200,-200, image = ufo2)

#loob kuulid
kuulid = []
kuul = PhotoImage(file=os.path.join("data","bullet.gif"))
for i in range (10):
    kuul_id=tahvel.create_image(-200,-200, image = kuul)
    kuulid.append(kuul_id)


kuul_id=tahvel.create_image(-200,-200, image = kuul)

#loob plahvatuse 
plahvatus = PhotoImage(file=os.path.join("data","plahvatus.gif"))
plahvatus_id=tahvel.create_image(-200,-200, image = plahvatus)

#loob plahvatuse2 
plahvatus2 = PhotoImage(file=os.path.join("data","plahvatus2.gif"))
plahvatus2_id=tahvel.create_image(-200,-200, image = plahvatus2)

pun_t2hed = []
#loob punased tähed (hulk tähti ja järjendisse)
pun_t2ht = PhotoImage(file=os.path.join("data","redstar.gif"))
for i in range (pun_t2htede_arv):
    pun_t2he_id=tahvel.create_image(random.randrange(0,500),random.randrange(-1500,-20), image = pun_t2ht)
    pun_t2hed.append(pun_t2he_id)

#loob suure punasetähe
suur_pun_t2ht = PhotoImage(file=os.path.join("data","redstar2.gif"))
suur_pun_t2ht_id = tahvel.create_image(-200, -200, image=suur_pun_t2ht)
    
# loome aja jaoks nimesildi
silt = ttk.Label(raam, text="Aeg")
silt.place(x=25, y=50)

# loome aja jaoks sildi
aeg = StringVar()
silt2 = ttk.Label(raam, textvariable=aeg)
silt2.place(x=25, y=75)
aeg.set(m2ngu_pikkus)


# loome punktide jaoks nimesildi
silt = ttk.Label(raam, text="Punktid")
silt.place(x=25, y=150)

# loome punktide jaoks sildi
var2 = StringVar()
silt = ttk.Label(raam, textvariable=var2)
silt.place(x=25, y=175)
var2.set(0)


# loome rekordite jaoks nimesildi
silt3 = ttk.Label(raam, text="Parimad")
silt3.place(x=25, y=250)


#loome rekordi jaoks sildi
par1 = StringVar()
silt4 = ttk.Label(raam, textvariable=par1)
silt4.place(x=25, y=275)
par2 = StringVar()
silt5 = ttk.Label(raam, textvariable=par2)
silt5.place(x=25, y=300)
par3 = StringVar()
silt6 = ttk.Label(raam, textvariable=par3)
silt6.place(x=25, y=325)


# loome mängujuhendi
juhend = ttk.Label(raam, text="MÄNGU JUHEND\n\nNooltega liigutatakse raketti. Kollaseid tähti püüdes kogutakse punkte.\nPunaste tähtede vastu minnes saadakse \
lisaaega. Asteroididega pihta saamisel kaotatakse aega.\nTühikuga saab tulistades hävitada asteroide ja ufosid.")
juhend.place(x=25, y=565)

# loome tasemete jaoks nimesildi
silt7 = ttk.Label(raam, text="Tasemed")
silt7.place(x=25, y=430)
startnupp()
n2ita_rekord()
startnupp()


#juhtnuppude defineerimine
raam.bind_all("<Up>",    nool_üles)
raam.bind_all("<Down>",  nool_alla)
raam.bind_all("<Left>",  nool_vasakule)
raam.bind_all("<Right>", nool_paremale)
raam.bind_all("<space>", tulista)

tahvel.pack()
raam.mainloop()


