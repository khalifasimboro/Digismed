# Dashboard SMED & TRS – Suivi Intelligent de Production

## Objectif du projet

Ce projet vise à développer une **application web interactive** permettant :

* Le **suivi en temps réel des changements de formats** sur les lignes de production.
* L’**estimation de l’impact de ces changements sur le TRS** (Taux de Rendement Synthétique).
* L’assistance des opérateurs via une interface ergonomique avec **checklist SMED** et **chronomètre intégré**.

L’outil s’intègre aux systèmes **Evocon** (suivi machine) et **ERP** (planning de production) pour fournir des **données consolidées** accessibles depuis les tablettes des opérateurs.



## Fonctionnalités principales

* 📅 **Prévision du nombre total de changements de format** (global & par machine)
* ⏱️ **Estimation du temps total à allouer aux changements**
* 📉 **Calcul de l’impact des changements sur le TRS**
* 🧾 **Check-list SMED** avec distinction des tâches internes / externes
* ⏳ **Chronomètre interactif** pour le suivi réel des interventions
* 📲 **Accès via icône sur tablette** (mode opérateur)

---

## 📚 Architecture du projet

/smed_dashboard/
│
├── 📁 app/
│   ├── main.py                         ⬅️ Lancement de l’app Streamlit
│   ├── pages/                          ⬅️ Pages du dashboard (optionnel si multi-pages)
│   │   ├── home.py
│   │   ├── changement_format.py
│   │   ├── suivi_smed.py
│   │   └── impact_trs.py
│   ├── components/
│   │   ├── charts.py                   ⬅️ Fonctions d’affichage graphique
│   │   └── layout.py                   ⬅️ Structure visuelle
│   └── utils/
│       ├── api_evocon.py               ⬅️ Connexion et requêtes à Evocon API
│       ├── api_erp.py                  ⬅️ Connexion à l’ERP (ou fichier CSV/DB simulé)
│       ├── data_processing.py          ⬅️ Traitement des données brutes
│       └── smed_calculations.py        ⬅️ Logique SMED (tâches internes/externes, gains…)
│
├── 📁 data/                            ⬅️ Données simulées ou exportées (au cas où)
│   ├── mock_production_schedule.csv
│   ├── mock_trs_data.csv
│   └── mock_smed_tasks.csv
│
├── 📁 assets/                          ⬅️ Logos, icônes, illustrations
│   └── logo_usine.png
│
├── 📁 tests/                           ⬅️ (facultatif) tests de ton code
│   └── test_api_evocon.py
│
├── .env                                ⬅️ Clés API, identifiants (non versionnés)
├── requirements.txt                    ⬅️ Librairies à installer (Streamlit, requests, pandas…)
├── README.md                           ⬅️ Doc du projet
└── config.yaml                         ⬅️ Paramètres généraux (URL API, seuils, machines…)


## 🔌 Données d’entrée

### Depuis l’ERP (ou Excel) :

* Nom du produit
* Machine associée
* Séquence de production journalière
* Durée de production par produit

### Depuis Evocon :

* TRS (global & par machine)
* Temps d'arrêt par type (réglage, nettoyage, panne…)
* Données temps réel machine

---

## 🧮 Indicateurs calculés

* **Nombre de changements de formats** prévus (globaux & par machine)
* **Temps perdu estimé** dû aux changements
* **TRS projeté** avec/sans optimisation SMED
* **Détails des tâches internes/externe** (avant et après optimisation)
* **Comparatif avant/après SMED**

---

## 📦 Dépendances

Liste des principales bibliothèques utilisées :

```bash
streamlit
pandas
numpy
requests
plotly
matplotlib
```

Installe-les avec :

```bash
pip install -r requirements.txt
```

## 🛠️ Lancement de l’application

En local :

```bash
streamlit run src/main.py


## 📲 Intégration sur tablette opérateur

* Déployer l’app sur un serveur accessible ( **Streamlit Cloud**, **Serveur local**).
* Créer un **raccourci** (icône) vers l’URL du dashboard sur les tablettes.
* Prévoir un **mode simplifié** pour les utilisateurs non techniques.

## 🔐 Sécurité & Authentification


## 📌 Cas d’usage futur
