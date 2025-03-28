import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]]. 
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Prestej število pikslov z barvo kože v škatli.'''
    pass

def doloci_barvo_koze(slika,levo_zgoraj,desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''
    pass

if __name__ == '__main__':
    # Pripravi kamero
    kamera = cv.VideoCapture(0)

    if not kamera.isOpened():
        print('Kamera ni bila uspešno odprta.')
        exit()

    # Zajami prvo sliko iz kamere
    ret, prva_slika = kamera.read()

    if not ret:
        print("Napaka: Neuspešno zajemanje slike iz kamere.")
        kamera.release()
        exit()
    
    # Prikaže zajeto sliko
    cv.imshow('Prva slika', prva_slika)

    
    levo_zgoraj = None
    desno_spodaj = None
    risanje = False

    # Nastavi MouseCallback za okno
    cv.setMouseCallback('Prva slika', narisi_pravokotnik)

    # Počakaj na izris in pritisk tipke Enter
    while True:
        key = cv.waitKey(1) & 0xFF
        if key == 13: 
            break

    cv.destroyAllWindows()

    # Preveri, če je pravokotnik bil narisan
    if levo_zgoraj is None or desno_spodaj is None:
        print("Napaka: Pravokotnik ni bil narisan.")
        kamera.release()
        exit()

    # Izračunamo barvo kože na prvi sliki
    barva_koze = doloci_barvo_koze(prva_slika, levo_zgoraj, desno_spodaj)    
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
    pass