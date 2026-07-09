# Copper Exploration Potential in Arizona and Nevada

## Overview

This project analyzes the exploratory potential of copper sites in Arizona and Nevada using open geospatial data, QGIS and Python.

The objective is not to estimate mining profitability, but to build a reproducible decision-support workflow to identify priority areas for further exploration analysis.

The study is based on 8,789 copper-related MRDS sites across Arizona and Nevada. An exploratory scoring method classifies sites into three potential classes: Low, Medium and High. Among them, 147 sites are classified as high potential.

## Research question

How can open mining and geospatial data be used to rank copper sites in Arizona and Nevada and identify priority counties for further exploration analysis?

## Tools used

- QGIS
- Python
- pandas
- geopandas
- matplotlib
- USGS open data
- OpenStreetMap basemap

## Methodology

The workflow includes:

1. Downloading MRDS data for Arizona and Nevada.
2. Filtering sites related to copper.
3. Merging both state datasets.
4. Building an exploratory scoring system using:
   - development status,
   - MRDS record quality,
   - deposit type,
   - total score.
5. Selecting high-potential copper sites.
6. Creating 10 km buffers around high-potential sites.
7. Crossing these sites with historical mining features.
8. Producing statistical tables, charts and maps.

## Key results

- Total copper-related MRDS sites: 8,789
- High-potential sites: 147
- High-potential sites in Nevada: 77
- High-potential sites in Arizona: 70
- High-potential sites located in strong or very strong historical mining contexts: 115 out of 147

The main priority counties identified are:

- Cochise
- Humboldt
- Pima
- Gila
- Mineral
- Lander
- Pinal

## Main outputs

### Maps

- `Carte_1_potentiel_cuivre_AZ_NV.png`  
  General map of copper sites by potential class.

- `Carte_2_sites_prioritaires_contexte_minier_10km_AZ_NV.png`  
  High-potential copper sites by historical mining context within 10 km.

### Figures

- Distribution of copper sites by potential class.
- High-potential sites by state.
- Historical mining context around high-potential sites.
- Priority counties by number of high-potential sites.

## Limits

This project is an exploratory screening analysis. It does not estimate mining profitability.

The MRDS dataset does not provide homogeneous information on:

- copper grades,
- resources,
- reserves,
- CAPEX,
- OPEX,
- transport costs,
- energy access,
- environmental constraints,
- permitting status.

A full investment analysis would require additional technical and economic data.

## Sources

- USGS ScienceBase
- USGS MRDS — Mineral Resources Data System
- USGS TopoMineSymbols
- U.S. Census Bureau Cartographic Boundary Files
- OpenStreetMap contributors

## Author

Lucas Lokumu  
Master Économie Appliquée — Université de Lille
