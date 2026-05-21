# N-Queens Optimization Project

This project solves the N-Queens problem with the four required approaches:

- `dfs_nqueens.ipynb`
- `greedy_nqueens.ipynb`
- `simulated_annealing_nqueens.ipynb`
- `genetic_nqueens.ipynb`

The notebooks benchmark the required board sizes `N = 10, 30, 50, 100, 200, 500`, save result tables in CSV format, and generate board visuals plus performance graphs for the report.

## Folder Structure

```text
ML_Ashu/
|-- dfs_nqueens.ipynb
|-- greedy_nqueens.ipynb
|-- simulated_annealing_nqueens.ipynb
|-- genetic_nqueens.ipynb
|-- README.md
|-- outputs/
|   |-- all_algorithms_comparison.csv
|   |-- dfs_nqueens_results.csv
|   |-- greedy_nqueens_results.csv
|   |-- simulated_annealing_nqueens_results.csv
|   |-- genetic_nqueens_results.csv
|   |-- board_images/
|   `-- charts/
`-- overleaf_report/
    |-- main.tex
    |-- Bibliography.bib
    `-- Figures/
```

## How To Run

1. Open a notebook in Jupyter.
2. Run the main execution cells.
3. Check the `outputs/` folder for saved CSV files, charts, and board images.

## Main Output Files

- `outputs/all_algorithms_comparison.csv`
- `outputs/dfs_nqueens_results.csv`
- `outputs/greedy_nqueens_results.csv`
- `outputs/simulated_annealing_nqueens_results.csv`
- `outputs/genetic_nqueens_results.csv`
- `outputs/charts/all_algorithms_comparison.png`
- `outputs/board_images/*.svg`

## Overleaf Report

The `overleaf_report/` folder is prepared in IEEE conference style and already includes:

- `main.tex`
- `Bibliography.bib`
- `Figures/` with the workflow diagram, comparison charts, and problem illustration

Upload the full `overleaf_report/` folder to Overleaf and compile there.

## Report Contents

The report includes:

- Introduction
- Related Work
- Gap Analysis
- Problem Statement
- Novelty of our work
- Our Solutions
- Methodology
- Results
- Discussion
- Future Directions
- Conclusion

It also includes your N-Queens tables, generated graphs, and board images in the required IEEE-style layout.

## Notes

- The report reads figures from `overleaf_report/Figures/`, which is case-correct for Overleaf.
- Two empty folders, `nqueens/` and `tests/`, may still remain if they are locked by another process in your IDE. They are not used by the project.
