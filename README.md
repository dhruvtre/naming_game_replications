# Minimal Naming Game

A learning exercise reproducing the qualitative behavior of the minimal Naming Game. The saved experiment uses 1,000 agents, one object, and 100,000 exchanges per run, with four random seeds: 42, 43, 44, and 45.

## File Descriptions

- `20102026_naming_game.py` - Implements the agents and interaction rules, runs a simulation, and saves measurements after each exchange to CSV.
- `naming_game_plots.py` - Averages the four runs at matching turns and plots total stored words, distinct names, and success rate. It also shows individual word-count trajectories and a labelled 50-exchange moving average for success.
- `run_*.csv` - The four runs' recorded measurements, including turn number, speaker/listener IDs, vocabulary counts, and whether the exchange succeeded. Each filename records the run number, settings, and seed.
- `naming_game_average_4_runs.png` - The exported figure comparing the four runs and their averages.

## Relevant Papers

- **[The Grounded Naming Game](https://martin-loetzsch.de/publications/steels12grounded.pdf)** - Luc Steels and Martin Loetzsch (2012). 
- **[Sharp transition towards shared vocabularies in multi-agent systems](https://arxiv.org/abs/physics/0509075)** : Andrea Baronchelli et al. (2006). Presents the minimal model and its transition to a shared vocabulary. The model rules and Figure 2 were the main reference for this reproduction.
- **[A gentle introduction to the minimal Naming Game](https://arxiv.org/abs/1701.07419)** : Andrea Baronchelli (2016). 
