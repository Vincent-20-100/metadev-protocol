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

## Idee 6 : Timestamp = verite (plus recent gagne)

**Le probleme :** Si tout est sauvegarde, on accumule des fichiers qui peuvent se
contredire. Un gold file de janvier peut dire le contraire d'un gold file d'avril.

**La regle proposee :** Chaque fichier est timestampe. En cas de contradiction,
**le plus recent fait foi.** Simple, deterministe, pas d'ambiguite.

**Implication sur le header standardise :**
```markdown
> DATE : 2026-04-01
> SUPERSEDES : context-management-v1.md (si applicable)
```

## Idee 7 : Maintenance de la base de connaissances — Tri et nettoyage

**Le probleme :** Si on sauvegarde tout, ca devient un dump. Il faut du tri.

**3 mecanismes de tri proposes :**

### A. Human-in-the-loop (le plus fiable)
- L'humain decide periodiquement : garder, archiver, supprimer
- Skill /tidy qui liste les fichiers par date, taille, et demande "on garde ?"
- Frequence : fin de sprint ou quand .meta/ depasse un seuil

### B. Dream Mode (automatise, inspire du leak)
- Un process (skill ou hook) qui consolide les connaissances :
  - Fusionne les fichiers qui se recoupent
  - Archive les fichiers obsoletes (superseded)
  - Met a jour INDEX.md
- Equivalent de notre /consolidate mais pour TOUTE la base gold/references
- Pourrait etre une skill /dream ou /maintain

### C. Lifecycle naturel (convention)
- Les fichiers references/ ont une duree de vie limitee
  - > 3 mois sans etre cite par un gold → candidat a l'archivage
- Les fichiers gold/ sont maintenus tant que le sujet est actif
- Les fichiers decisions/ sont permanents (ADRs ne sont jamais supprimes)

**Les 3 mecanismes sont complementaires, pas exclusifs.**

## Idee 8 : Cycle de vie d'un fichier de connaissance

```
RECHERCHE                    SYNTHESE                    MAINTENANCE
   |                            |                            |
   v                            v                            v
references/raw.md  --/digest--> gold/synthesis.md  --/dream--> gold/synthesis-v2.md
   (bronze)                     (gold)                       (gold, mis a jour)
                                  |
                                  v
                              INDEX.md (mis a jour)
                                  |
                                  v
                          decisions/ADR-xxx.md (si decision prise)
```

### Les transitions :
1. **Recherche → Reference** : agent web/parsing, sauvegarde timestampee
2. **Reference → Gold** : skill /digest, extraction key takeaways
3. **Gold → Gold v2** : skill /dream ou /consolidate, fusion/mise a jour
4. **Gold → Decision** : humain valide, cree un ADR
5. **Reference → Archive** : /tidy ou human-in-the-loop, fichier obsolete

### Les regles de transition :
- Ref → Gold : TOUJOURS (pas de ref qui reste sans synthese)
- Gold stale (>3 mois sans update) : flag pour review humain
- Gold contradictoire : plus recent gagne, ancien archive
- Decision : JAMAIS supprimee, peut etre SUPERSEDED par une nouvelle

## Questions ouvertes pour le brainstorm

- Format exact de l'INDEX.md (table? liste? sections?)
- Comment la skill /digest met a jour l'INDEX.md automatiquement
- Est-ce que CLAUDE.md devrait pointer vers INDEX.md ("lis .meta/gold/INDEX.md") ?
- Est-ce que les sessions/ devraient aussi avoir un INDEX?
- Seuil de volume pour declencher /tidy (nombre de fichiers? taille totale?)
- Est-ce que /dream tourne automatiquement (hook SessionStart?) ou manuellement?
- Comment gerer les gold files qui couvrent plusieurs domaines?
- Est-ce que le template genere devrait inclure gold/ et references/ vides
  ou seulement les creer a la premiere utilisation?
