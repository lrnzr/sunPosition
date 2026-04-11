import math
import datetime
import csv

# Funzioni di utilità  
    
def input_utente():
    """Chiede di inserire i dati geografici e temporali."""
    print("Calcola la principali grandezze solari e le rispettive coordinate\n")
    
    # Coordinate geografiche
    while True:
        try:
            lat = float(input("Inserire la latitudine (gradi, -90 a 90): "))
            if -90 <= lat <= 90:
                break
            else:
                print("Errore: La latitudine deve essere tra -90 e 90 gradi.")
        except ValueError:
            print("Errore: Inserire un numero valido.")
    
    while True:
        try:
            lon = float(input("Inserire la longitudine (gradi, -180 a 180): "))
            if -180 <= lon <= 180:
                break
            else:
                print("Errore: La longitudine deve essere tra -180 e 180 gradi.")
        except ValueError:
            print("Errore: Inserire un numero valido.")
    
    # fuso orario
    while True:
        try:
            tz = float(input("Inserire il fuso orario (in ore): "))
            if -12 <= tz <= 14:
                break
            else:
                print("Errore: Il fuso orario deve essere tra -12 e 14 ore.")
        except ValueError:
            print("Errore: Inserire un numero valido.")

    # Data e ora
    while True: 
        try:
            date_str = input("Inserire la data e l'ora (YYYY-MM-DD HH:MM:SS): ")
            dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            break
        except ValueError:
            print("Errore: Formato data non valido. Usare YYYY-MM-DD HH:MM:SS.")
  
    return lat, lon, dt, tz

def giorno_giuliano(dt: datetime.datetime) -> float:
    """Calcola il giorno giuliano a partire da una data e ora."""
    a = math.modf(7 * (dt.year + ((dt.month + 9) / 12)) / 4)
    b = math.modf((275 * dt.month) / 9)
    jd = 367 * dt.year - a[1] + b[1] + dt.day + 1721013.5 + dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
    return jd 
   

# Funzioni per esportazione CSV
def raccogli_risultati():
    """Raccoglie i risultati in una lista di coppie (campo, valore)."""
    return [
        ("latitudine_deg", latitudine_geo),
        ("longitudine_deg", longitudine_geo),
        ("data_e_ora", dt.isoformat(sep=' ')),
        ("fuso_orario", tz),
        ("delta_t", delta_t),
        ("greenwich_utc", greenwich_utc),
        ("giorno_giuliano_utc_jde", jde),
        ("delta_n_2000", delta_n_2000),
        ("anomalia_media_deg", anomalia_media_deg),
        ("longitudine_media_deg", longitudine_media_deg),
        ("eccentricita", eccentricita),
        ("eq_centro_rad", eq_centro_rad),
        ("longitudine_vera_sole_deg", longitudine_vera_sole_deg),
        ("obliquita_deg", epsilon_deg),
        ("declinazione_deg", declinazione_deg),
        ("ascensione_retta_deg", ascensione_retta_deg),
        ("anomalia_vera_deg", anomalia_vera_deg),
        ("raggio_ua", raggio),
        ("angolo_H_tramonto_deg", angolo_H_tramonto_deg),
        ("durata_di_h", durata_di),
        ("eq_tempo_min", eq_tempo_min),
        ("t_mezzogiorno_h", ora_mezzogiorno),
        ("t_sorgere_h", ora_alba),
        ("t_tramonto_h", ora_tramonto),
        ("ora_utc_h", ora_utc),
        ("tempo_locale_medio_h", tempo_locale_medio),
        ("tempo_solare_apparente_h", tempo_solare_apparente),
        ("angolo_orario_locale_deg", angolo_orario_locale_deg),
        ("altezza_deg", altezza),
        ("altezza_corretta_deg", altezza_corretta),
        ("zenit_deg", zenit),
        ("azimut_deg", azimut_deg),
    ]

def salva_csv(percorso, risultati):
    """Scrive i risultati su un file CSV: nella prima riga le intestazioni, nella seconda riga i valori."""
    intestazioni = [k for k, _ in risultati]
    valori = [v for _, v in risultati]
    try:
        with open(percorso, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(intestazioni)
            writer.writerow(valori)
    except Exception as e:
        print(f"Errore durante la scrittura del file CSV: {e}")

# Chiede se esportare i risultati in CSV e, in caso affermativo, salva il file
def esportazione_csv():
    print()
    resp = input("Salvare i risultati in CSV? (s/n): ").strip().lower()
    if resp in ('s', 'y'):
        fname = input("Nome file CSV (default output_coordinateSolari.csv): ").strip()
        if not fname:
                fname = 'output_coordinateSolari.csv'
        salva_csv(fname, raccogli_risultati())
        print(f"Risultati salvati in: {fname}")
    else:
        print("Programma terminato senza esportazione CSV")          

# ---------------------- input -------------------------------------------------------------  

# Raccoglie i dati dall'utente
latitudine_geo, longitudine_geo, dt, tz = input_utente()

#----------------------- calcoli -----------------------------------------------------------

jd = giorno_giuliano(dt) 
delta_t = 69.184
jde = jd - tz/24.0 + delta_t / 86400.0   
delta_n_2000  = jde - 2451545.0

greenwich_utc = dt - datetime.timedelta(hours = tz) 
    
# Anomalia media della Terra
anomalia_media_deg = (357.52910 + 0.9856002819986311 * delta_n_2000 - 1.168599418792319e-13*delta_n_2000**2 - 9.850778720459782e-21*delta_n_2000**3) % 360.0
anomalia_media_rad = math.radians(anomalia_media_deg)

# Longitudine media della Terra (normalizzata)
longitudine_media_rad = (4.8950629938800505 + 0.017202791698456926 * delta_n_2000 + 3.9666703992487734e-15 * delta_n_2000**2) % (2 * math.pi)
longitudine_media_deg = math.degrees(longitudine_media_rad)

# eccentricita
eccentricita = 0.016708617 - 1.1509103353867213e-9 * delta_n_2000 - 9.264842088693435e-17 * delta_n_2000**2

# eq. del centro
eq_centro_rad = 2 * eccentricita * math.sin(anomalia_media_rad) + 5/4 * eccentricita**2 * math.sin(2 * anomalia_media_rad) + 13/12 * eccentricita**3 * math.sin(3 * anomalia_media_rad)

# Longitudine eclittica del sole
longitudine_vera_sole_rad = (longitudine_media_rad + eq_centro_rad) % (2 * math.pi)
longitudine_vera_sole_deg = math.degrees(longitudine_vera_sole_rad)

# Obliquità dell'eclittica
epsilon_deg = 23.43929111111111 - 3.560346794433036e-7 * delta_n_2000 - 1.2284827472872003e-16 * delta_n_2000**2 + 1.033533670150092e-20 * delta_n_2000**3
epsilon_rad = math.radians(epsilon_deg)

# Declinazione solare
declinazione_rad = math.asin(math.sin(epsilon_rad) * math.sin(longitudine_vera_sole_rad))
declinazione_deg = math.degrees(declinazione_rad)

# Ascensione retta
ascensione_retta_rad = math.atan2(math.cos(epsilon_rad) * math.sin(longitudine_vera_sole_rad), math.cos(longitudine_vera_sole_rad))
ascensione_retta_deg = math.degrees(ascensione_retta_rad) % 360.0

# anomalia vera = M + eq_centro
anomalia_vera_rad = anomalia_media_rad + eq_centro_rad
anomalia_vera_deg = math.degrees(anomalia_vera_rad) % 360.0

# modulo del raggio vettore Sole-Terra in unità astronomiche
raggio = 1.000001018 * (1 - eccentricita**2) / (1 + eccentricita * math.cos(anomalia_vera_rad))

# angolo orario del tramonto
latitudine_geo_rad = math.radians(latitudine_geo)
angolo_H_tramonto_rad = math.acos(math.cos(math.radians(90 + 0.8333))/(math.cos(latitudine_geo_rad) * math.cos(declinazione_rad)) - math.tan(latitudine_geo_rad) * math.tan(declinazione_rad))
angolo_H_tramonto_deg = math.degrees(angolo_H_tramonto_rad)

# durata del dì in ore
durata_di = 2 * angolo_H_tramonto_deg / 15.0

# equazione del tempo
y = (math.tan(epsilon_rad/2))**2
eq_tempo_rad = (y * math.sin(2 * longitudine_media_rad) + 4*eccentricita* y * math.sin(anomalia_media_rad) * math.cos(2 * longitudine_media_rad) - 0.5 * (y**2) * math.sin(4 * longitudine_media_rad)) - (2 * eccentricita*math.sin(anomalia_media_rad) + 1.25 * eccentricita**2 * math.sin(2 * anomalia_media_rad))
eq_tempo_min = 4 * (180.0 / math.pi) * eq_tempo_rad

# tempi del mezzogiorno, sorgere e tramonto
ora_mezzogiorno = 12 - (12 / math.pi) * eq_tempo_rad - longitudine_geo / 15.0 + tz
ora_alba = ora_mezzogiorno - angolo_H_tramonto_deg / 15.0
ora_tramonto = ora_mezzogiorno + angolo_H_tramonto_deg / 15.0

# ora UTC
ora_utc = dt.hour - tz

# LMT = Local Mean Time
tempo_locale_medio = ora_utc + longitudine_geo / 15.0

# AST = Apparent Solar Time
tempo_solare_apparente = tempo_locale_medio + eq_tempo_min / 60.0

# angolo orario locale
angolo_orario_locale_deg = ((tempo_solare_apparente - 12) * 15.0 + 360.0) % 360.0
angolo_orario_locale_rad = math.radians(angolo_orario_locale_deg)

# altezza senza la rifrazione atmosferica
altezza = math.degrees(math.asin(math.sin(latitudine_geo_rad)*math.sin(declinazione_rad) + math.cos(latitudine_geo_rad) * math.cos(declinazione_rad) * math.cos(angolo_orario_locale_rad)))

# correzione per la rifrazione atmosferica
correzione_rifrazione = (1.02/60) / math.tan(math.radians(altezza + 10.3/(altezza + 5.11))) 

# altezza corretta considerando la rifrazione atmosferica
altezza_corretta = altezza + correzione_rifrazione

# zenit 
zenit = 90 - altezza_corretta

# azimut da sud verso ovest
azimut_rad = math.atan2(math.sin(angolo_orario_locale_rad), math.cos(angolo_orario_locale_rad)*math.sin(latitudine_geo_rad) - math.tan(declinazione_rad)*math.cos(latitudine_geo_rad))
azimut_deg = (math.degrees(azimut_rad) + 360) % 360

# ---------------------- output -------------------------------------------------------------

print()
print("Calcola la principali grandezze solari e le rispettive coordinate\n")
print("Dati di input:")
print("latitudine (deg): ", latitudine_geo)
print("longitudine (deg): ", longitudine_geo)
print("data e ora: ", dt)
print("fuso orario (h): ", tz)
print("\nRisultati calcolati:")
print("delta t (s): ", delta_t)
print("Greenwich UTC: ",greenwich_utc)
print("Giorno giuliano UTC jde (d): ", jde) 
print("n. giorni dal 2000 (d): ", delta_n_2000) 
print("anomalia media (deg): ", anomalia_media_deg)   
print("longitudine media (deg): ", longitudine_media_deg) 
print("eccentricità: ", eccentricita) 
print("equazione del centro (rad): ", eq_centro_rad) 
print("longitudine eclittica Sole (deg): ", longitudine_vera_sole_deg) 
print("obliquità (deg): ", epsilon_deg) 
print("declinazione (deg): ", declinazione_deg) 
print("ascensione retta (deg): ", ascensione_retta_deg)
print("anomalia vera (deg): ", anomalia_vera_deg)
print("raggio (UA): ", raggio)
print("angolo orario tramonto (deg): ", angolo_H_tramonto_deg)
print("durata del dì (h): ", durata_di)
print("eq. tempo (min): ", eq_tempo_min)
print("istante del mezzogiorno (h): ", ora_mezzogiorno) 
print("istante dell'alba (h): ", ora_alba) 
print("istante del tramonto (h): ", ora_tramonto) 
print("ora UTC (h): ", ora_utc)
print("tempo locale medio (h): ", tempo_locale_medio)
print("tempo solare apparente (h): ", tempo_solare_apparente)
print("angolo orario locale (deg): ", angolo_orario_locale_deg) 
print("altezza (deg): ", altezza)
print("altezza corretta (deg): ", altezza_corretta) 
print("zenit (deg): ", zenit)
print("azimut (deg): ", azimut_deg)  

# Chiede se esportare i risultati in CSV e, in caso affermativo, salva il file
esportazione_csv()