from faster_whisper import WhisperModel
import psutil
import torch.cuda
import time
import os.path

from time import sleep


class Fst_WhisperPipeline:

    def __init__(self, model_name=None, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available()
                                 else "cpu")


        print(f"Using device: {"GPU" if self.device == "cuda" else self.device.upper()}")

        if self.device == "cuda":
            if model_name is None:
                vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
                if vram > 12:
                    model_name = "large-v2"
                elif vram >= 10:
                    model_name = "medium"
                elif vram >= 6:
                    model_name = "small"
                else:
                    model_name = "base"
            print(f"Using model: Faster Whisper | Model size: {model_name}")

        elif self.device == "cpu":
            if model_name is None:
                ram = psutil.virtual_memory().total / (1024 ** 3)
                if ram >= 16:
                    model_name = "medium"
                elif ram >= 8:
                    model_name = "small"
                else:
                    model_name = "tiny"
            print(f"Using model: Faster Whisper | Model size: {model_name}")

        #self.file_name = os.path.basename(file_name)

        print("\nINIZIO TRASCRIZIONE.")
        print(f"\rLoading model...", end="", flush=True)


        self.model = whisper.load_model(model_name, self.device)


    def trascrizione(self, audio_file, segment_mode, coda_trascrizione):
        if segment_mode is None:
            print("\n")

        file_name = os.path.basename(audio_file)
        print(f"\rTranscribing: {file_name}")

        result = self.model.transcribe(audio_file, language="it", verbose=False) # verbose: se su False mostra caricamento, se su True mostra sul momento le rige trascriversi


        coda_trascrizione.put(result["text"])

        if segment_mode is False:
            return self.text_result(result, file_name)
        if segment_mode is True:
            return self.segmented_result(result, file_name)


    def text_result(self, result, file_name):
        print(f"\r{result["text"].strip()}\n", end="", flush=True)

        print(save_txt(result["text"], file_name))


    def segmented_result(self, result, file_name):
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            phrase = segment["text"].strip()

            start_min = int(start_time // 60)
            start_sec = int(start_time % 60)
            end_min = int(end_time // 60)
            end_sec = int(end_time % 60)

            print(f"\r[{start_min:02d}:{start_sec:02d}] {phrase}", flush=False)

            print(save_txt(result["text"], file_name))



    def time_counter(self, end_exe):
        start_time = time.monotonic()

        global time_shown
        while not end_exe.is_set():
            current_time = time.monotonic()
            elapsed_time = current_time - start_time

            mins = int(elapsed_time // 60)
            secs = float(elapsed_time % 60)

            time_shown = ""
            if mins > 0:
                time_shown += f"{mins}m "
            time_shown += f"{secs:.1f}s"

            print(f"\r{time_shown}", end="", flush=True)

        sleep(0.1)
        print(f"{time_shown}")


def save_txt(text, file_name):
    #cartella_locale = os.path.dirname(__file__)            # with open(f"{os.path.join(cartella_locale, file_name[:-4])}.txt", "w") as f:
    file_name, file_ext = os.path.splitext(file_name)
    with open(f"raccolte/Storia/Trascrizioni/{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(text.strip())
        f.close()
    sleep(0.50)
    return ("\nTRASCRIZIONE TERMINATA E SALVATA.")
