# Scripts for the Climatological Renewable Energy Deviation Index

Version 1.0.1

A set of scripts detailing the Climatological Renewable Energy Deviation Index as describe in [this paper](https://arxiv.org/abs/2307.08909). 


## Project organization

```
.
├── .gitignore
├── CITATION.md
├── LICENSE.md
├── README.md
├── requirements.txt
├── data                     <- All project data, ignored by git
│   ├── processed            <- The final, canonical data sets for modeling.
│   ├── raw                  <- The original, immutable data dump, ignored by git.
│   └── temp                 <- Intermediate data that has been transformed, ignored by git.
├── docs                     <- Documentation notebook for users
│   └── arXiv                <- Preprint arXiv files, e.g. LaTeX files
├── results
│   ├── publication          <- Figures for the publication
│   ├── supplementary        <- Supplementary figures for the investigation and publication
│   ├── additional_regions   <- Base figures generated for other regions
│   └── figures_development  <- Figures generated in the development phase of the project
└── src                      <- Scripts and source code for this project 

```


## License

This project is licensed under the terms of the [MIT License](/LICENSE.md)

## Citation

If you use CREDI in a scientific publication, we would appreciate citations to the following paper:

[The Climatological Renewable Energy Deviation Index](https://arxiv.org/abs/2307.08909), Stoop, L. P., van der Wiel, K., Zappa, W., Haverkamp, A., Feelders, A., & van den Broek, M. (2023).

Bibtex entry:
```bibtex
@misc{stoop2023climatological,
      title={The Climatological Renewable Energy Deviation Index}, 
      author={Laurens P. Stoop and Karin van der Wiel and William Zappa and Arno Haverkamp and Ad J. Feelders and Machteld van den Broek},
      year={2023},
      eprint={2307.08909},
      archivePrefix={arXiv},
      primaryClass={physics.ao-ph}
}
```

If you want to cite scripts as provided here, please use:

Scripts for The Climatological Renewable Energy Deviation Index, Stoop, L. P. (2023) https://github.com/laurensstoop/CREDI

Bibtex entry:
```bibtex
@misc{stoop2023CREDIscripts,
      title={Scripts for The Climatological Renewable Energy Deviation Index}, 
      author={Laurens P. Stoop},
      year={2023},
      url={ https://github.com/laurensstoop/CREDI}
}
```
