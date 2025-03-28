import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina))

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

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
    Način izračuna je prepuščen vaši domišljiji.'''

    # Pridobi škatlo oz. ROI (Region of Interest) iz slike
    roi = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]

    # Izračuna povprečje in standardno deviacijo barv v ROI
    mean_bgr = np.mean(roi, axis=(0, 1))
    std_bgr = np.std(roi, axis=(0, 1))

    # Definira spodnjo in zgornjo mejo barve kože
    spodnja_meja = np.array([max(0, mean_bgr[0] - std_bgr[0]),  # Blue lower limit
                             max(0, mean_bgr[1] - std_bgr[1]),  # Green lower limit
                             max(0, mean_bgr[2] - std_bgr[2])], dtype=np.uint8)  # Red lower limit

    zgornja_meja = np.array([min(255, mean_bgr[0] + std_bgr[0]),  # Blue upper limit
                              min(255, mean_bgr[1] + std_bgr[1]),  # Green upper limit
                              min(255, mean_bgr[2] + std_bgr[2])], dtype=np.uint8)  # Red upper limit

    return spodnja_meja, zgornja_meja

if __name__ == '__main__':
    #Pripravi kamero

    #Zajami prvo sliko iz kamere

    #Izračunamo barvo kože na prvi sliki

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.
    pass