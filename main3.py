import time
import os
import queue

from Fst_Whisper import Fst_WhisperPipeline
from GenaiPipeline3 import GenaiPipeline3


def avvio_trascrizione(coda_rec=None, model_name=None, device=None, segmented_mode=False):
    print("Running HearScribe:")
    whisper = WhisperPipeline(model_name=model_name, device=device)

    def threads_trascrizione():
        coda_trascrizione = queue.Queue()

        whisper.trascrizione(rec, segmented_mode, coda_trascrizione,)

        trascrizione = (coda_trascrizione.get()).strip()

        time.sleep(0.75)
        print("\nINIZIO RIELABORAZIONE.")

        # print("\n\rRielaborazione in corso...", end="", flush=True)
        print("Registrazione rielaborata:\n")
        print(select_chatbot(file_name=os.path.basename(rec)))


    fusion_mode = False     # flag che abilita la rielaborazione complessiva.
    i = 0
    for rec in coda_rec:
        threads_trascrizione()
        i += 1
        if len(coda_rec) > 1:
            print("=" * 120 + "\n")


    if len(coda_rec) > 1:
        print("\nINIZIO RIELABORAZIONE COMPLESSIVA.")
        print("Rielaborazione completata:\n")

        file_name = f"Rielaborato Complessivo HS_{get_datetime()}"
        fusion_mode = True
        print(select_chatbot(file_name=file_name, fusion_mode=fusion_mode, coda_rec=coda_rec))

# Forse sarebbe meglio fare il ciclo che crea il final_prompt nel GenaiPipeline? Ad esempio passando per parametro la dimensione di coda_rec.
# Oppure si potrebbe fare con un altro parametro impostare quando usare la modalità con il nome del file o con il final_prompt.


def select_chatbot(file_name=None, fusion_mode=False, coda_rec=None):
    genai = GenaiPipeline3(
        model=None,
        file_prompt=file_name,
        fusion_mode=fusion_mode,
        coda_rec=coda_rec
    )
    return genai.generazione(file_name)


def get_datetime():
    local_datetime = time.localtime()

    day = str(local_datetime.tm_mday)
    month = str(local_datetime.tm_mon)
    year = str(local_datetime.tm_year)

    hour = local_datetime.tm_hour
    min = local_datetime.tm_min
    sec = local_datetime.tm_sec

    real_datetime = f"{day}-{month}-{year}_{hour}{min}{sec}"
    return real_datetime


def raccolta_exist(cartella_raccolte=None):

    cartella_raccolte = cartella_raccolte or "./raccolte"

    try:
        return os.listdir(cartella_raccolte)

    except FileNotFoundError:
        print(f"Errore: La cartella '{cartella_raccolte}' non esiste.")
        return False

    except NotADirectoryError:
        print(f"Errore: '{cartella_raccolte}' non è una cartella.")
        return False


def mk_raccolta(): 
    message = (
        "IMPOSTAZIONI RACCOLTE:"
        "Le raccolte servono ad organizzare in modo ordinato le tue lezioni, appunti ed elaborati.\n"
        "Comandi:"
        "new {nome_raccolta}   <-- Per creare una nuova raccolta."
        "exit                  <-- Per uscire dalle impostazioni raccolte."
        "-----------------------------------------------------------------------------------------"
    )
    print("")
    while comando.startswith("exit"):
        print(f"\r{message}", end="", flush=True)
        comando = str(input("Inserisci "))




def main():
    if raccolta_exist() is True:
        print("Non sono attualmente presenti Raccolte, devi crearne una.")
        str(input("Nuova Raccolta:"))
        os.mkdir("./raccolte/", )
    else:
        print(f"La cartella non è vuota.")



    lista_rec = [
        r"raccolte/Storia/Interrogazione Storia 30-05-2025.mp3"
    ]

    avvio_trascrizione(
        coda_rec=lista_rec,
        model_name = "large",
        device = "cuda",
        segmented_mode = False
    )

if __name__ == "__main__":
    main()