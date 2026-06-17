# InjectMetaData Dataverse

Guide d installation pour qu une autre personne puisse cloner le projet et le tester rapidement.

## 1) Ce que fait le projet

Le main est ai_app.py.
L application ouvre une interface Tkinter, lit un dictionnaire Excel, genere des JSON dans le dossier schema, puis appelle les scripts Dataverse dans le dossier Scripts.

Pipeline:
Excel -> parse_dictionary.py -> schema/*.json -> Scripts/create_*.py -> Dataverse

## 2) Prerequis machine

- Windows 10/11 (recommande)
- Python 3.10 ou 3.11
- Acces internet (authentification Microsoft)
- Un compte avec droits Dataverse suffisants (creation/edition metadata)
- Une solution Dataverse existante dans l environnement cible

## 3) Installation

Depuis le dossier du projet:

1. Creer l environnement virtuel
   python -m venv .venv

2. Activer l environnement
   .venv\Scripts\Activate.ps1

3. Installer les dependances
   pip install -r requirements.txt

## 4) Configuration .env (obligatoire)

Creer un fichier .env a la racine avec:

DATAVERSE_URL=https://votre-org.crm.dynamics.com
SOLUTION_NAME=NomUniqueDeLaSolution
LANGUAGE_CODE=1033

Explication:
- DATAVERSE_URL: URL de l environnement Dataverse cible
- SOLUTION_NAME: unique name de la solution Dataverse (pas le display name)
- LANGUAGE_CODE: 1033 pour anglais, 1036 pour francais, etc.

## 5) Lancement

Commande:
python ai_app.py

Ensuite dans l UI:
1. Cliquer sur Charger Excel
2. Selectionner le dictionnaire metier (.xlsx)
3. Cliquer sur Lancer

## 6) Comment marche l authentification

- Le token est obtenu via MSAL (OAuth2)
- Au premier lancement: login interactif Microsoft
- Ensuite: reutilisation du cache local token_cache.bin si possible

Important:
- Ne pas partager token_cache.bin
- Chaque personne doit se connecter avec son propre compte

## 7) Si vous partagez le projet avec d autres

Oui, ils peuvent executer le projet si:

1. Ils changent DATAVERSE_URL et SOLUTION_NAME dans leur .env
2. Ils ont les droits Dataverse necessaires
3. Ils font la connexion interactive a la premiere execution

## 8) Depannage rapide

- Erreur DATAVERSE_URL manquant:
  verifier le fichier .env a la racine

- Erreur SOLUTION_NAME manquant ou composant non trouve:
  verifier le unique name exact de la solution

- Erreur module not found:
  re activer .venv puis relancer pip install -r requirements.txt

- Aucun popup de login mais erreurs 401/403:
  supprimer token_cache.bin puis relancer

## 9) Fichiers principaux

- ai_app.py: interface et orchestration
- parse_dictionary.py: parse du fichier Excel choisi
- schema_builder.py / sheet_parser.py / schema_normalizer.py: transformation metadata
- schema_dispatcher.py: generation des JSON schema
- Scripts/create_tables.py
- Scripts/create_fields.py
- Scripts/create_picklists.py
- Scripts/create_multiselects.py
- Scripts/create_lookups.py
