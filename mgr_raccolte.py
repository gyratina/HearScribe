import os
from time import sleep


class mgr_raccolte:

    def mgr_raccolta():

        base_dir = "raccolte"


        def showMSG(delay=True):
            message = (
                "IMPOSTAZIONI RACCOLTE:\n"
                "Le raccolte servono ad organizzare in modo ordinato le tue lezioni, appunti ed elaborati.\n\n"
                "Comandi:\n"
                "new {nome_raccolta}                         <-- Per creare una nuova raccolta.\n"
                "see                                         <-- Per visualizzare tutte le raccolte.\n"
                "rename {nome_raccolta} {nuovo_nome}         <-- Per rinominare una raccolta.\n"
                "del {nome_raccolta}                         <-- Per eliminare una raccolta con tutti i suoi contenuti.\n"
                "exit                                        <-- Per uscire dalle impostazioni raccolte.\n"
            )
            if delay is True:
                sleep(0.5)
            print(f"{message}", end="", flush=True)


        def nav_raccolta():
            lista_dir = os.listdir(base_dir)
            print("Le tue Raccolte:")

            branches = ["├─", "└─"]
            i = 0
            if len(lista_dir) > 0:
                for raccolta in lista_dir:
                    i += 1
                    if len(lista_dir) == 1:     # Con queste condizioni decido il tipo di ramo da mettere prima del nome.
                        branch = branches[1]
                    elif i < len(lista_dir):
                        branch = branches[0]
                    else:
                        branch = branches[1]

                    print(f"{branch}{raccolta}")
                #print("\n")
            else:
                print("Non sono presenti raccolte.")


        def nameFormatter(name):
            name = name[0].upper() + name[1:].lower()
            return name


        comando = ""
        showMSG(delay=False)
        while not comando.startswith("exit"):

            comando = str(input("\n>"))

            if comando.startswith("new"):
                try:
                    nome_raccolta = comando[3:].strip()
                    nome_raccolta = nameFormatter(nome_raccolta)
                    os.mkdir(f"{base_dir}/{nome_raccolta}")
                    os.mkdir(f"{base_dir}/{nome_raccolta}/Registrazioni")
                    os.mkdir(f"{base_dir}/{nome_raccolta}/Trascrizioni")
                    os.mkdir(f"{base_dir}/{nome_raccolta}/Rielaborati")
                    os.mkdir(f"{base_dir}/{nome_raccolta}/Elaborati complessivi")
                    print("La raccolta è stata creata")
                except PermissionError:
                    print(f"Impossibile creare la cartella (Permesso negato).\n")
                except OSError as OSe:
                    print(f"Errore nella creazione della cartella: {OSe}\n")

                showMSG()


            elif comando.startswith("see"):
                nav_raccolta()


            elif comando.startswith("rename"):
                comando = comando.lower()
                lista_dir = os.listdir(base_dir)
                for raccolta in lista_dir:
                    cmd__ = f"rename {raccolta.lower()}"

                    if comando.startswith(cmd__):
                        old_name = comando[7:7+len(raccolta)].strip()
                        new_name = (comando[len(cmd__):]).strip()
                        new_name = nameFormatter(new_name)
                        break

                try:
                    os.rename(src=f"{base_dir}/{old_name}", dst=f"{base_dir}/{new_name}")
                    print("Raccolta rinominata.\n")
                except FileNotFoundError or FileExistsError:
                    print("Raccolta da rinominare non trovata o inesistente.\n")
                except PermissionError:
                    print("Impossibile rinominare la raccolta (Permesso negato).\n")

                showMSG()


            elif comando.startswith("del"):
                nome_raccolta = comando[3:].strip()

                try:
                    os.rmdir(f"{base_dir}/{nome_raccolta}")
                    print("Raccolta eliminata.\n")
                except FileNotFoundError or FileExistsError:
                    print("Raccolta non trovata o inesistente.\n")
                except PermissionError:
                    print("Impossibile eliminare la raccolta (Permesso negato).\n")

                showMSG()


            elif not comando.startswith("exit"):
                print("Comando sbagliato o non esistente, riprova.\n")
                showMSG()



mgr_raccolte.mgr_raccolta()
