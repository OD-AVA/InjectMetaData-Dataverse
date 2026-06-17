import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import threading


def interpret_prompt(prompt):
    p = prompt.lower()
    if "modèle" in p or "dataverse" in p or "donnée" in p:
        steps = [
            "Lecture du dictionnaire Excel",
            "Identification des objets et attributs",
            "Exécution pipeline Dataverse"
        ]
    else:
        steps = [
            "Analyse globale du besoin",
            "Génération du modèle de données",
            "Création Dataverse"
        ]
    return {"steps": steps}


def run_pipeline(log, file_path):
    log.insert(tk.END, "\n📦 Initialisation du pipeline Dataverse...\n")

    scripts = [
        "parse_dictionary.py",
        "Scripts/create_tables.py",
        "Scripts/create_fields.py",
        "Scripts/create_picklists.py",
        "Scripts/create_multiselects.py",
        "Scripts/create_lookups.py"
    ]

    for s in scripts:
        log.insert(tk.END, f"\n▶️ {s}\n")
        log.update()

        cmd = ["python", s, file_path] if s == "parse_dictionary.py" else ["python", s]
        result = subprocess.run(cmd, capture_output=True, text=True)

        log.insert(tk.END, result.stdout)
        log.insert(tk.END, result.stderr)


def run_ai():
    log.delete(1.0, tk.END)

    prompt = entry.get("1.0", tk.END)
    file_path = selected_file.get()

    log.insert(tk.END, "\n🧠 Analyse du besoin métier...\n")

    result = interpret_prompt(prompt)
    log.insert(tk.END, "\n📋 Plan d'exécution :\n")
    for step in result["steps"]:
        log.insert(tk.END, f" - {step}\n")

    if not file_path:
        log.insert(tk.END, "\n❌ Aucun fichier sélectionné\n")
        return

    log.insert(tk.END, f"\n📂 Fichier : {file_path}\n")
    log.insert(tk.END, "\n🚀 Lancement du pipeline...\n")

    thread = threading.Thread(target=run_pipeline, args=(log, file_path), daemon=True)
    thread.start()


def browse_file():
    file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file:
        selected_file.set(file)



root = tk.Tk()
root.title("AI Dataverse Assistant")
root.geometry("700x500")

selected_file = tk.StringVar()

tk.Label(root, text="💬 Décris ton besoin").pack()

entry = tk.Text(root, height=4)
entry.pack(fill="x")

tk.Button(root, text="📂 Charger Excel", command=browse_file).pack()
tk.Label(root, textvariable=selected_file).pack()

tk.Button(root, text="🚀 Lancer", command=run_ai).pack(pady=10)

log = scrolledtext.ScrolledText(root)
log.pack(fill="both", expand=True)

root.mainloop()