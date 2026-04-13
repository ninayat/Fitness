# 🏋️‍♂️ Fitness Park - Manuel Opérationnel 2025

![Version](https://img.shields.io/badge/version-2025-blue)
![Statut](https://img.shields.io/badge/status-actif-success)
![Licence](https://img.shields.io/badge/licence-interne-lightgrey)

## 🚀 Objectif

Dépôt de travail structuré à partir du fichier source du repo :
**`PROCEDURES _ SMQ 2025 - Réseau franchise.pdf`**.

## 📚 Organisation

- [Coin Formation](./formation/README.md)
- [Coin Procédures](./procedures/README.md)
- [Extraits de sommaire SMQ 2025](./sources/SMQ-2025-sommaire.md)

## 🧭 Principe éditorial

- Base de construction : le PDF SMQ 2025 présent dans ce repo.
- Les nouvelles pages créées suivent les rubriques visibles du sommaire (Basiques, Options, Relances, Cas particuliers).
- Aucun ajout de processus hors périmètre du document source.

## 🌐 Utilisation en mode site

1. Lancer un serveur statique à la racine du repo :
   ```bash
   python -m http.server 8080
   ```
2. Ouvrir : `http://localhost:8080`
3. Le manuel est navigable via la barre latérale (`_sidebar.md`) et la recherche intégrée.

## 🚀 Publication GitHub Pages

Le repo est prêt pour GitHub Pages avec le workflow:
- `.github/workflows/deploy-pages.yml`

URL cible après push + activation Pages:
- `https://ninayat.github.io/fitness/`
