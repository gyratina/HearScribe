from faster_whisper import WhisperModel
import psutil
import torch.cuda
import time
import os.path

from time import sleep


class Fst_WhisperPipeline:

    def __init__(self, model_name=None, device=None, quantization=None):
        self.device, self.quantization = (device, quantization or
                                              ("cuda", None if torch.cuda.is_available()
                                              else "cpu", "float32")
                                          )


        print(f"Using device: {"GPU" if self.device == "cuda" else self.device.upper()}")

        if self.device == "cuda":
            if model_name is None:
                vram = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
                if vram > 12:
                    model_name = "large-v2"
                    quantization = "float16"
                elif vram >= 10:
                    model_name = "medium"
                    quantization = "float16"
                elif vram >= 6:
                    model_name = "small"
                    quantization = "int8"
                else:
                    model_name = "base"
                    quantization = "int8"
            self.quantization = quantization
            print(f"Using model: Faster Whisper | Model size: {model_name} | Compute type: {self.quantization}")


        elif self.device == "cpu":

            if model_name is None:
                ram = psutil.virtual_memory().total / (1024 ** 3)
                if ram >= 16:
                    model_name = "medium"
                elif ram >= 8:
                    model_name = "small"
                else:
                    model_name = "tiny"
            print(f"Using model: Faster Whisper | Model size: {model_name} | Compute type: {quantization}")

        #self.file_name = os.path.basename(file_name)

        print("\nINIZIO TRASCRIZIONE.")
        print(f"\rLoading model...", end="", flush=True)


        self.model = WhisperModel(model_name, self.device, compute_type=self.quantization)


    def trascrizione(self, audio_file, segment_mode, end_transcription_advice):
        if segment_mode is None:
            print("\n")

        file_name = os.path.basename(audio_file)
        print(f"\rTranscribing: {file_name}")

        segments, info = self.model.transcribe(audio_file, language="it") # verbose: se su False mostra caricamento, se su True mostra sul momento le rige trascriversi

        result = " ".join(segment.text for segment in segments)
        # ^Questo è come fare:
                            # segment: str
                            # for segment in segments:
                            #     result += " ".join(segment.text)


        if segment_mode is False:
            return self.text_result(result, file_name, end_transcription_advice)
        if segment_mode is True:
            return self.segmented_result(segments, file_name, end_transcription_advice)


    def text_result(self, result, file_name, end_transcription_advice):
        print(f"\r{result.strip()}\n", end="", flush=True)

        print(save_txt(result, file_name, end_transcription_advice))


    def segmented_result(self, segments, file_name, end_transcription_advice):
        for segment in segments:
            start_time = segment.start
            end_time = segment.end
            phrase = segment.text.strip()

            start_min = int(start_time // 60)
            start_sec = int(start_time % 60)
            end_min = int(end_time // 60)
            end_sec = int(end_time % 60)

            print(f"\r[{start_min:02d}:{start_sec:02d}] -> [{end_min:02d}:{end_sec:02d}] {phrase}", flush=False)

            print(save_txt(result, file_name, end_transcription_advice))


    # Funzione attualmente inutilizzata
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

# Dopo l'implementazione del manager di raccolte far sì che l'utente possa decidere la posizione.
def save_txt(text, file_name, end_transcription_advice):
    #cartella_locale = os.path.dirname(__file__)            # with open(f"{os.path.join(cartella_locale, file_name[:-4])}.txt", "w") as f:
    file_name, file_ext = os.path.splitext(file_name)
    with open(f"raccolte/Storia/Trascrizioni/{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(text.strip())
        f.close()
    sleep(0.50)

    end_transcription_advice.put(text)
