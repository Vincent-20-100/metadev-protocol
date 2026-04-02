# Idees brutes — Systeme de connaissances hierarchique

> Capture des idees de Vincent, 2026-04-01. A brainstormer en profondeur plus tard.
> PAS une decision — un input pour le brainstorm.

---

## Idee 1 : Skill /digest — Traitement d'information systematique

**Le probleme :** Quand un agent fait de la recherche web ou parse un gros document,
le resultat reste dans le chat (contexte volatile) ou dans un fichier brut non structure.

**La regle proposee :** Des qu'un agent fait de la recherche ou du parsing, il DOIT
produire (ou proposer) un fichier de synthese. Le travail est restitue ET memorise.

**Implications :**
- Ce n'est pas juste une skill, c'est une **convention de travail** a mettre dans CLAUDE.md
- La skill /digest automatise la transformation raw → gold
- Mais la regle "toujours produire une synthese" est plus large que la skill

## Idee 2 : Hierarchie de connaissances avec docstrings

**Le probleme :** Un LLM qui arrive dans un projet doit comprendre le contexte
general AVANT de plonger dans les details. Aujourd'hui il doit ouvrir et lire
chaque fichier.

**La solution proposee :** Utiliser les docstrings/headers comme des "resumes executifs"
a chaque niveau de la hierarchie :

```
.meta/gold/
├── INDEX.md                         ← Resume de TOUS les gold files (10-20 lignes)
│                                       Lu en premier, donne la carte
├── skills-workflow-and-utilities.md ← Header = resume (5 lignes)
│                                       Body = detail complet
├── context-management.md           ← Header = resume (5 lignes)
│                                       Body = detail complet
└── ...
```

**Le flow de lecture d'un LLM :**
1. Lit INDEX.md (20 lignes) → comprend tout ce qu'on sait
2. Ouvre le fichier gold pertinent → detail actionnable
3. Si besoin, va a la source dans references/ → raw data

**C'est du progressive disclosure applique a la documentation, pas juste aux skills.**

## Idee 3 : Mapping sur les 3 niveaux

| Niveau | Contenu | Quand le lire | Equivalent |
|--------|---------|---------------|------------|
| **Carte** (INDEX.md) | 1-2 lignes par sujet | Toujours | Description de skill |
| **Gold** (gold/*.md) | Key takeaways structures | Quand on travaille sur le sujet | Body de skill |
| **Source** (references/*.md) | Raw data, URLs, citations | Quand on a besoin de preuves | Documentation externe |

## Idee 4 : Convention pour les fichiers

Chaque fichier .md dans gold/ et references/ commence par un header standardise :

```markdown
# Titre

> RESUME : [1-2 phrases qui disent l'essentiel]
> SOURCES : [fichiers source]
> DATE : [date de creation]
> CONFIANCE : [haute/moyenne/basse]
```

Ce header est ce qui apparait dans l'INDEX.md. Le LLM peut scanner
les headers sans ouvrir les fichiers.

## Idee 5 : Generaliser au template

Cette hierarchie n'est pas juste pour metadev-protocol. Elle devrait etre
dans le TEMPLATE genere :

```
.meta/
├── gold/           ← Syntheses actionnables (le LLM lit ca en priorite)
│   └── INDEX.md    ← Carte de tout ce qu'on sait
├── references/     ← Sources brutes (le LLM y va si besoin)
├── decisions/      ← ADRs (pourquoi on a choisi)
├── sessions/       ← Historique
└── scratch/        ← Brouillons (gitignored)
```

## A brainstormer plus tard

- Format exact de l'INDEX.md (table? liste? sections?)
- Comment la skill /digest met a jour l'INDEX.md automatiquement
- Est-ce que CLAUDE.md devrait pointer vers INDEX.md ("lis .meta/gold/INDEX.md pour le contexte") ?
- Comment gerer le versioning des gold files (date? hash?)
- Est-ce que les sessions/ devraient aussi avoir un INDEX?
- Comment faire pour que le LLM sache quand un gold file est stale?
