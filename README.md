# AI Music Workshop

This repository hosts code and resources for analysis of data collected during the "Music and AI" workshop held at the NRWC2024 Conference. The purpose of this project is to investigate preferences and attitudes towards AI-generated music and privacy. The project focuses on survey analysis and quiz data, with visualizations and statistical analyses managed in Jupyter Notebook workflows.

## Table of Contents
1. [Project Overview](#project-overview)
2. [File Descriptions](#file-descriptions)
3. [Setup and Installation](#setup-and-installation)

## Project Overview

The AI Music Workshop project analyzes survey and quiz data to explore how people perceive AI-generated music in retail spaces. It utilizes Python-based data analysis workflows, organized in Jupyter notebooks, and external configuration files for handling ordinal data and custom recoding of survey responses.

### Background

This project is part of the research initiative *Sound Environment in Retail: A Cross-Industry Study on Sound Design and Music Strategies*. The goal is to explore how background music and environmental sounds in retail spaces influence employee-customer interactions, and their impact on satisfaction and well-being.

### Aim

The workshop aimed to explore the impact of sound environments on retail customer experiences with representatives from the retail and wholesale sectors. A key question addressed was: "Is generative AI the solution for in-store music, or does it risk overengineering and alienating customers?" Participants discussed how music shapes atmosphere and consumer behavior, while considering the role of AI-generated content.

### Approach

- **Pre-Workshop Survey**: An online survey was distributed to participants (retail and wholesale professionals) to assess their attitudes toward AI-powered music solutions. G-tests were used to analyze categorical data, with Benjamini-Hochberg FDR corrections applied to control for multiple comparisons.
- **On-Site Quiz**: A quiz was conducted during the workshop to evaluate the ability to distinguish between sounds and images of retail stores, as well as human-created vs AI-generated music. Crochan's Q test and McNemar's test were used to assess differences between image-based and sound-based questions.
- **Real-time Survey Data Analysis**: Survey data was analyzed during the workshop to provide immediate insights and inform discussions.

### Findings

- **Pre-Workshop Survey**: Analysis revealed a preference for human-made music over AI-generated music. There was also a strong preference for in-store music over silence, as well as a desire for personalized music experiences.
- **On-Site Quiz**: Results showed significant differences in performance between image-based and sound-based questions. 

## File Descriptions

- **AI-music-workshop.ipynb**: Main Jupyter notebook for running all project analyses and generating outputs.
- **config/**: Stores JSON configuration files for handling categorical and ordinal data processing.
- **data/**: Contains original data files (excluded from the repository until the scientific paper is published).
- **output/**: Stores generated outputs such as figures and data exports (some contents excluded pre-publication).
  - **data/**: Folder for data exports (excluded from repository pre-publication).
  - **plots/**: Folder for generated plots, with subdirectories for `quiz` and `survey` plots.
- **src/**: Python scripts with helper functions for configuration loading, data processing, plotting, and statistical analysis.
 
## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/AI-music-workshop.git
    cd AI-music-workshop
    ```

2. **Install required packages**: To run the Jupyter Notebook, first install dependencies directly within a notebook cell:
    ```python
    !pip install -r requirements.txt
    ```

3. **Run the Notebook**:
   Open `AI-music-workshop.ipynb` in Jupyter Notebook. All configurations, including ordinal columns and recode mappings, will load automatically. 
