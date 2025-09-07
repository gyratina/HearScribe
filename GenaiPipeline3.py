import os.path
from time import sleep
from google import genai
from google.genai import types
from dotenv import load_dotenv


class GenaiPipeline3:

    def __init__(self, model=None, file_prompt=None, fusion_mode=False, coda_rec=None):
        load_dotenv()
        self.client = genai.Client(api_key = os.environ.get("GEMINI_API_KEY"))
        self.model = "gemini-2.5-flash"

        if fusion_mode is False:
            file_prompt, file_ext, = os.path.splitext(file_prompt)
            with open(f"raccolte/Storia/Trascrizioni/{file_prompt}.txt", "r", encoding="utf-8") as f:
                prompt = f.read().strip()
                self.final_prompt = (
                    f"Ciao, potresti cortesemente riorganizzare in modo ordinato e senza tralasciare il minimo dettaglio, questa interrogazione?"
                    f"\nEscludi eventuali informazioni irrilevanti rispetto ai temi principali dell'interrogazione come note decontestualizzate."
                    f"\n\nINTERROGAZIONE:\n{prompt}"
                )

        else:
            prompt = ""
            for rec_name in coda_rec:
                rec_name = os.path.basename(rec_name)
                rec_name, file_ext = os.path.splitext(rec_name)
                with open(f"raccolte/Storia/Rielaborati/{rec_name}.md", "r", encoding="utf-8") as f:  # MODIFICARE IL "WITH OPEN" CON QUELLO REALMENTE FUNZIONANTE *(FARE LO STESSO PER SAVE_TXT E SAVE MS)*
                    prompt += f"{f.read().strip()}\n\n"

            self.final_prompt = (
                f"Rielabora le seguenti lezioni in un solo testo evitando ripetizioni di argomenti"
                f"\n\nLEZIONI:\n{prompt}"
            )

            # FOR DEVS ONLY - Salva il prompt usato per l'elaborato complessivo.     # DEBUGGING
            with open(f"raccolte/Storia/Elaborati complessivi/Prompt_complessivo.txt", "w", encoding="utf-8") as f:
                f.write(prompt)
                f.close()




    def generazione(self, doc_name):
        prompt_setting = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=self.final_prompt
                    )
                ]
            )
        ]

        generation_config = types.GenerateContentConfig(
            temperature=0.8,
            top_p=0.95,
            top_k=64,
            max_output_tokens=65536,
            response_mime_type="text/plain",
        )

        risposta = self.client.models.generate_content(
            model = self.model,
            contents = prompt_setting,
            config = generation_config
        )

        righe = risposta.text.splitlines(keepends=True)  # Mantiene gli '\n'     # Suddivide la risposta in righe
        for rigo in righe:
            parole = rigo.split()       # Suddivide le righe in parole
            for parola in parole:
                print(parola, end=" ")
                sleep(0.01)
            if rigo.endswith("\n"):
                print()     # Va a capo
        print()
        return (save_md(risposta.text.strip(), doc_name) )



def save_md(text, file_name):
    # cartella_locale = os.path.dirname(__file__)           # with open(f"{os.path.join(cartella_locale, file_name[:-4])}.md", "w")as f:
    file_name, file_ext = os.path.splitext(file_name)
    with open(f"raccolte/Storia/Rielaborati/{file_name}.md", "w", encoding="utf-8") as f:
        f.write(text)
        f.close()
    sleep(0.50)
    return ("\n\nRIELABORAZIONE TERMINATA E SALVATA.")


def complessive_prompt():
    pass
