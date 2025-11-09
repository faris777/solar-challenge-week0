# solar-challenge-week0
challenge of the solar 
# Solar Data Visualization App

A **Streamlit** web application to explore and visualize solar datasets from multiple countries (Benin, Sierra Leone, and Togo). The app allows users to preview data, paginate through rows, view statistical summaries, and dynamically plot solar metrics.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Development Process](#development-process)
- [Features](#features)
- [Installation](#installation)
- [Usage Instructions](#usage-instructions)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)
- [Future Improvements](#future-improvements)

---

## Project Overview

This app was developed as part of the **Solar Challenge Week 0** project. Its main goal is to provide interactive tools for analyzing solar datasets collected from different countries, focusing on metrics such as:

- GHI (Global Horizontal Irradiance)
- DNI (Direct Normal Irradiance)
- DHI (Diffuse Horizontal Irradiance)
- Other environmental data (Temperature, Precipitation, etc.)

---

## Development Process

1. **Data Preparation**
   - Cleaned raw CSV files for Benin, Sierra Leone, and Togo.
   - Ensured consistent column names and timestamp formatting.
   - Saved cleaned CSVs in the `data/` directory.

2. **Streamlit App Setup**
   - Initialized a Streamlit app (`__init__.py`) with page configuration and layout.
   - Added a sidebar to select the country dataset dynamically.
   - Implemented session state for **pagination** of dataset preview.

3. **Interactive Features**
   - Data preview with **Next** and **Previous** buttons (paginated).
   - Statistical summaries with `df.describe()` in an expander.
   - Dynamic plotting:
     - Line plots (metric over time)
     - Boxplots (distribution)
     - Histograms
     - Scatter plots (metric comparisons)
   - Plot type and metric selection via sidebar widgets.

4. **Testing**
   - Verified file loading paths and absolute/relative path handling.
   - Ensured interactive features work with multiple datasets.
   - Confirmed plots update correctly with sidebar selections.

---

## Features

- **Country Selection**: Choose between Benin, Sierra Leone, and Togo.
- **Data Preview**: View dataset rows with pagination controls.
- **Data Summary**: Expandable statistical summary of selected dataset.
- **Dynamic Visualization**: Select plot type and metric to visualize solar data.
- **Interactive Sidebar**: Easy navigation and selection of dataset and visualization options.

---

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd solar-challenge-week0
