# 🛡️ CyberDétection-IA
### Système Intelligent de Détection et Prédiction d'Attaques Réseau

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Streamlit-Interface-red?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn"/>
  <img src="https://img.shields.io/badge/Précision-92%25-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Statut-Actif-success?style=for-the-badge"/>
</p>

---

## 📌 À propos du projet

**CyberDétection-IA** est une plateforme complète de détection et de prédiction des attaques réseau, propulsée par l'intelligence artificielle.

Développé dans le cadre de la formation à **YaneCode Academy** sous l'encadrement de **Monsieur Jamal Et-Tousy**, ce projet combine cybersécurité, machine learning et visualisation de données pour offrir une solution intelligente d'analyse des menaces réseau en temps réel.

---

## ✨ Fonctionnalités

| Module | Description |
|--------|-------------|
| 🔴 **Attack Predictor** | Détecte et classifie 6 types d'attaques réseau en temps réel |
| 📊 **System Dashboard** | Vue globale des incidents avec statistiques et graphiques interactifs |
| 📡 **Live Monitoring** | Surveillance du trafic réseau en direct |
| 🔍 **Data Explorer** | Exploration de 3 000 incidents cybernétiques (2015–2024) |
| 📄 **Documentation** | Guide complet d'utilisation de la plateforme |

---

## 🎯 Types d'attaques détectées

- 🔴 **DDoS** — Attaque par déni de service distribué
- 🟠 **Phishing** — Hameçonnage et vol de données
- 🟡 **SQL Injection** — Injection de code malveillant dans les bases de données
- 🔵 **Ransomware** — Logiciel de rançon chiffrant les données
- 🟣 **Malware** — Logiciel malveillant infiltrant les systèmes
- ⚪ **Man-in-the-Middle (MitM)** — Interception et manipulation des communications

---

## 🤖 Modèles de Machine Learning implémentés

Tous les algorithmes suivants ont été développés et comparés dans ce projet :

| Algorithme | Description |
|------------|-------------|
| 📈 **Logistic Regression** | Modèle de classification linéaire de base |
| 🔵 **K-Nearest Neighbors (KNN)** | Classification par proximité des voisins |
| 🌲 **Random Forest** | Ensemble d'arbres de décision — **Meilleur modèle** ✅ |
| ⚡ **Support Vector Machine (SVM)** | Classification par hyperplan optimal |

### Techniques appliquées
- **SMOTE Balancing** — Équilibrage des classes pour éviter le biais
- **Cross-validation** — Validation croisée pour fiabiliser les résultats
- **Label Encoding** — Encodage des variables catégorielles
- **Feature Scaling** — Normalisation des données avec StandardScaler

### Résultats
| Métrique | Valeur |
|----------|--------|
| Meilleur modèle | **Random Forest** |
| Précision | **92%** |
| Dataset | Menaces mondiales en cybersécurité |
| Incidents analysés | **3 000** |
| Pays couverts | **10 pays** |

---

## 💻 Stack Technique

```
Python 3.12        → Langage principal
Streamlit          → Interface web interactive
Scikit-learn       → Modèles de Machine Learning
Pandas             → Manipulation et analyse des données
Matplotlib         → Visualisation des données
Pickle             → Sauvegarde des modèles entraînés
```

---

## 🚀 Installation & Lancement

### 1. Cloner le projet
```bash
git clone https://github.com/lehdaoui/cyberdetection-IA.git
cd cyberdetection-IA
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run cyber.py
```

### 4. Ouvrir dans le navigateur
```
http://localhost:8501
```

---

## 📁 Structure du projet

```
cyberdetection-IA/
│
├── cyber.py                          # Point d'entrée principal (Streamlit)
├── Cyberdétecteur.py                 # Module de détection principal
├── requirements.txt                  # Dépendances Python
├── README.md                         # Documentation
│
├── best_model.pkl                    # Meilleur modèle ML sauvegardé (Random Forest)
├── label_encoder.pkl                 # Encodeur des labels sauvegardé
├── scaler.pkl                        # Scaler de normalisation sauvegardé
│
└── Menaces mondiales en matière      # Dataset — 3 000 incidents (2015–2024)
    de cybersécurité.csv
```

---

## 👩‍💻 Développé par

**Marwa Lehdaoui**
- 🎓 Étudiante en Cybersécurité — Option SSR
- 🏫 École Supérieure de Technologie de Safi (EST Safi)
- 🏢 Formée à **YaneCode Academy**
- 🔗 [LinkedIn](https://www.linkedin.com/in/marwa-lehdaoui-183379358/)
- 💻 [GitHub](https://github.com/lehdaoui)

---

## 🙏 Remerciements

Un grand merci à **Monsieur Jamal Et-Tousy**, formateur à YaneCode Academy, pour son encadrement rigoureux, sa pédagogie de qualité et sa disponibilité tout au long de ce projet. Son accompagnement a été déterminant dans la réussite de ce travail.

---

## 📄 Licence

Ce projet est développé à des fins éducatives dans le cadre de la formation à YaneCode Academy — Année 2026.

---

<p align="center">
  Fait par <strong>Marwa Lehdaoui</strong> · YaneCode Academy · 2026
</p>
