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
    
    # Pridobi dimenzije slike
    visina_slike, sirina_slike, _ = slika.shape

    # Inicializira prazen seznam za rezultate
    rezultat = []

    # Z zanko gre skozi sliko v korakih visina_skatle in sirina_skatle
    for y in range(0, visina_slike, visina_skatle):
        vrstica = []  # Inicializira vrsto za trenutne škatle 
        for x in range(0, sirina_slike, sirina_skatle):
            # Pridobi trenutno škatlo (ROI) z uporabo "Slicing"
            box = slika[y:y + visina_skatle, x:x + sirina_skatle]

            # Preštej število pikslov z barvo kože v škatli
            st_pikslov = prestej_piklse_z_barvo_koze(box, barva_koze)

            # Appenda število pikslov v škatli v trenutno vrsto
            vrstica.append(st_pikslov)

        # Appenda trenutno vrsto v rezultat
        rezultat.append(vrstica)

    return rezultat

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:
    '''Preštej število pikslov z barvo kože v škatli.'''
    spodnja_meja, zgornja_meja = barva_koze 

    # Ustvari masko, ki vsebuje vse piksle, ki so znotraj barve kože in jih označi z belo barvo (255) vse ostale pa z črno (0)
    mask = cv.inRange(slika, spodnja_meja, zgornja_meja)

    # Preštej število belih pikslov
    st_pikslov = cv.countNonZero(mask)

    return st_pikslov

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

def narisi_pravokotnik(event, x, y, flags, param):
    '''Funkcija za risanje pravokotnika z miško.'''
    global levo_zgoraj, desno_spodaj, risanje, prva_slika

    if event == cv.EVENT_LBUTTONDOWN:  # Začetek risanja
        risanje = True
        levo_zgoraj = (x, y)

    elif event == cv.EVENT_MOUSEMOVE and risanje:  # Dinamično risanje pravokotnika
        desno_spodaj = (x, y)
        slika_kopija = prva_slika.copy()
        cv.rectangle(slika_kopija, levo_zgoraj, desno_spodaj, (0, 255, 0), 2)
        cv.imshow('Prva slika', slika_kopija)

    elif event == cv.EVENT_LBUTTONUP:  # Konec risanja
        risanje = False
        desno_spodaj = (x, y)
        slika_kopija = prva_slika.copy()
        cv.rectangle(slika_kopija, levo_zgoraj, desno_spodaj, (0, 255, 0), 2)
        cv.imshow('Prva slika', slika_kopija)

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
    
    # Začetek FPS merjenja
    start_time = time.time()

    # Zajemaj slike iz kamere in jih obdeluj     
    while True:
        # Pridobi frame iz kamere
        ret, frame = kamera.read()
        if not ret:
            print("Napaka: Kamera ni poslala slike.")
            break

        # Zmanjšaj sliko na 220x340
        resized_frame = zmanjsaj_sliko(frame, 220, 340)

        # Prešteje število pikslov kože v vsaki škatli
        sirina_skatle = 20 
        visina_skatle = 20  
        rezultat = obdelaj_sliko_s_skatlami(resized_frame, sirina_skatle, visina_skatle, barva_koze)

        # Izračuna povprečje števila pikslov kože v škatlah
        all_pixels = [pixel for row in rezultat for pixel in row]
        povprecje = sum(all_pixels) / len(all_pixels) if all_pixels else 0
    
        # Pretvori sliko nazaj na originalno velikost
        original_height, original_width, _ = frame.shape
        scale_x = original_width / 220
        scale_y = original_height / 340

        # Nariše škatle z nadpovprečnim številom pikslov kože
        for i, row in enumerate(rezultat):
            for j, st_pikslov in enumerate(row):
                if st_pikslov > povprecje:
                    # Izračuna koordinate škatle v originalni sliki
                    x1 = int(j * sirina_skatle * scale_x)
                    y1 = int(i * visina_skatle * scale_y)
                    x2 = int((j + 1) * sirina_skatle * scale_x)
                    y2 = int((i + 1) * visina_skatle * scale_y)

                    # Nariše škatle na sliko
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Izmeri čas in izračina FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        start_time = end_time

        # Izpiše FPS na sliko
        cv.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Pokaže frame z označenimi škatlami
        cv.imshow('Kamera v realnem casu', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    kamera.release()
    cv.destroyAllWindows()

    # Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        # Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
    '''Floodfill poišče še sosede vsake škatle, ki imajo večje štilo pikslov kože in jih združi v eno območje, tako najde le eno skupno območje in predvideva da je to obraz. Vse ostale pa izbriše.'''
        # Vprašanje 2: Kako prešteti število ljudi?
    '''Če floodfill najde več območij, ki so večja od določene velikosti, potem je to več ljudi, če pa najde samo eno območje, potem je to ena oseba.'''

        # Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        # in ne pozabite, da ni nujno da je škatla kvadratna.  
    '''Če so škatle manjše je natančnost večja, vendar se FPS zmanjša
       Če so škatle večje je natančnost manjša, vendar se FPS poveča'''
           
    pass