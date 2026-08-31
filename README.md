# 🏎️ F1 Race Intelligence

An interactive Formula 1 race analytics dashboard built with **Python, FastF1, Pandas, Plotly, and Streamlit**.

The application allows users to select a Formula 1 season and Grand Prix, compare drivers, analyze race pace, study tyre performance and stint strategy, and explore detailed race data through an interactive dashboard.

## 📊 Dashboard Preview

Project screenshots are available in the [`screenshots/`](screenshots/) folder.

## ✨ Features

- 🏁 Dynamic Formula 1 season selection
- 🌍 Dynamic Grand Prix selection based on the selected season
- 📅 Automatically works with the latest completed seasons
- ⚔️ Driver-to-driver performance comparison
- ⏱️ Lap-time and race-pace analysis
- 📈 Track/race pace evolution
- 🏎️ Position progression analysis
- 🧩 Sector performance comparison
- 🛞 Tyre compound performance analysis
- 🔄 Stint and tyre strategy analysis
- 💡 Automatically generated race insights
- 📋 Detailed race-data exploration
- 📊 KPI cards for important race metrics
- ⚡ FastF1 persistent caching for faster repeated data access
- 🌙 Dark, responsive Streamlit interface

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application and data analysis |
| FastF1 | Formula 1 timing and race data |
| Pandas | Data processing and analysis |
| Plotly | Interactive visualizations |
| Streamlit | Web dashboard and UI |

## 🔎 Analytics Included

### Driver Battle
Compare two drivers using:

- Average lap time
- Fastest lap
- Median lap time
- Pace gap
- Position progression

### Race Pace
Analyze how lap times change throughout the race and identify pace trends.

### Sector Performance
Compare drivers across Sector 1, Sector 2, and Sector 3.

### Tyre Strategy
Analyze:

- Tyre compounds
- Tyre age
- Lap-time performance
- Stint duration
- Strategy sequence

### Race Data
Explore the cleaned lap-level dataset used by the dashboard.

## 📁 Project Structure

```text
F1-Race-Intelligence/
│
├── app.py
├── driver_analysis.py
├── explore_data.py
├── lap_comparison.py
├── stint_analysis.py
├── test_fastf1.py
├── track_evolution.py
├── tyre_analysis.py
│
├── screenshots/
│   └── dashboard screenshots
│
└── fastf1_cache/
    └── generated locally and ignored by Git
```

> `fastf1_cache/` is intentionally not included in the GitHub repository. FastF1 creates and manages the cache locally when the application runs.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/F1-Race-Intelligence.git
cd F1-Race-Intelligence
```

### 2. Create and activate the Conda environment

```bash
conda create -n f1-project python=3.11
conda activate f1-project
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The Streamlit application will open in your browser.

## 📦 Requirements

The main Python dependencies are:

```text
streamlit
fastf1
pandas
plotly
```

A complete dependency list is provided in [`requirements.txt`](requirements.txt).

## 💾 FastF1 Caching

The application uses a local FastF1 cache to avoid repeatedly downloading and processing the same race data.

The cache is created automatically in:

```text
fastf1_cache/
```

This directory is ignored by Git and should not be uploaded to GitHub.

The first load of a race on a new computer may take longer because the required data has not been cached yet. Repeated access can be faster after the data has been cached locally.

## 📚 Data Source

Race data is retrieved through the **FastF1** Python package, which provides access to Formula 1 timing and session data.

## 🎯 Project Objective

The objective of this project is to build an interactive analytics platform that transforms Formula 1 race data into useful visual insights about:

- Driver performance
- Race pace
- Tyre behaviour
- Stint strategy
- Sector performance
- Position changes

The project combines data collection, data cleaning, analysis, visualization, caching, and interactive dashboard development in one application.

## 🚀 Future Improvements

Potential future enhancements include:

- Telemetry comparison
- Circuit map visualization
- Advanced braking and acceleration analysis
- Season-wide driver performance comparison
- Machine-learning-based race or lap-time predictions

## 👨‍💻 Author

**Puneeth**

Built as a Python and data analytics portfolio project.

## ⭐ If you find this project useful

Feel free to star the repository and explore the code.
