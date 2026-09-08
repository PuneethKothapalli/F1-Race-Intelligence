import streamlit as st
import fastf1
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# ============================================================
# FASTF1 CACHE
# ============================================================

os.makedirs("fastf1_cache", exist_ok=True)
fastf1.Cache.enable_cache("fastf1_cache")

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="F1 Race Intelligence",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .main-title {
        display: block;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: #f9fafb;
        margin-bottom: 2px;
    }

    .main-subtitle {
        display: block;
        color: #9ca3af;
        font-size: 0.9rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .race-heading {
        display: block;
        color: #f9fafb;
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 2px;
    }

    .race-subheading {
        display: block;
        color: #9ca3af;
        font-size: 0.88rem;
    }

    .race-badge {
        display: inline-block;
        margin-left: 10px;
        padding: 4px 9px;
        border: 1px solid #3b4250;
        border-radius: 999px;
        color: #b8c0cc;
        background: #151922;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        vertical-align: middle;
    }

    .summary-bar {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin: 18px 0 6px 0;
    }

    .summary-item {
        display: block;
        box-sizing: border-box;
        min-height: 72px;
        padding: 13px 15px;
        background: #151922;
        border: 1px solid #303642;
        border-radius: 10px;
    }

    .summary-label {
        display: block;
        color: #8f98a8;
        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .summary-value {
        display: block;
        color: #f9fafb;
        font-size: 1.05rem;
        font-weight: 750;
    }

    .summary-note {
        display: block;
        color: #7f8898;
        font-size: 0.68rem;
        margin-top: 2px;
    }

    .section-title {
        display: block;
        color: #f9fafb;
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .kpi-card {
        display: block;
        box-sizing: border-box;
        width: 100%;
        min-height: 125px;
        background: #151922;
        border: 1px solid #303642;
        border-radius: 12px;
        padding: 18px 20px;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }

    .kpi-card:hover {
        border-color: #6b7280;
        transform: translateY(-2px);
    }

    .kpi-label {
        display: block;
        color: #9ca3af;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 9px;
    }

    .kpi-value {
        display: block;
        color: #f9fafb;
        font-size: 1.65rem;
        font-weight: 750;
        line-height: 1.2;
    }

    .kpi-description {
        display: block;
        color: #9ca3af;
        font-size: 0.78rem;
        margin-top: 8px;
        line-height: 1.4;
    }

    .driver-card {
        display: block;
        box-sizing: border-box;
        width: 100%;
        min-height: 145px;
        background: #151922;
        border: 1px solid #303642;
        border-radius: 12px;
        padding: 20px 22px;
        text-align: center;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }

    .driver-card:hover {
        border-color: #6b7280;
        transform: translateY(-2px);
    }

    .driver-card.winner {
        border-color: #6b7280;
    }

    .driver-status {
        display: inline-block;
        margin-top: 10px;
        padding: 3px 8px;
        border: 1px solid #3b4250;
        border-radius: 999px;
        color: #c7cbd1;
        background: #10131a;
        font-size: 0.64rem;
        font-weight: 700;
        letter-spacing: 0.07em;
    }

    .driver-code {
        display: block;
        color: #f9fafb;
        font-size: 1.45rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .driver-team {
        display: block;
        color: #9ca3af;
        font-size: 0.82rem;
    }

    .driver-stat {
        display: block;
        color: #f9fafb;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 14px;
    }

    .driver-stat-label {
        display: block;
        color: #9ca3af;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 3px;
    }

    .versus {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        color: #6b7280;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 0.08em;
    }

    .insight-box {
        display: block;
        box-sizing: border-box;
        width: 100%;
        background: #151922;
        border: 1px solid #303642;
        border-left: 4px solid #6b7280;
        border-radius: 10px;
        padding: 16px 18px;
        margin-top: 18px;
    }

    .insight-title {
        display: block;
        color: #f9fafb;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .insight-text {
        display: block;
        color: #c7cbd1;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    [data-testid="stSidebar"] {
        background-color: #10131a;
        border-right: 1px solid #252a33;
    }

    .sidebar-section {
        display: block;
        color: #9ca3af;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    /* Make the selected tab slightly more prominent without
       changing the graph styling. */
    button[data-baseweb="tab"][aria-selected="true"] {
        font-weight: 750;
    }

    .app-footer {
        display: block;
        margin-top: 42px;
        padding-top: 18px;
        border-top: 1px solid #252a33;
        text-align: center;
        color: #737c8b;
        font-size: 0.72rem;
        line-height: 1.7;
    }

    .app-footer strong {
        color: #aeb6c3;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #303642;
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# REUSABLE UI HELPERS
# ============================================================

def render_kpi(label, value, description=""):
    """Render a KPI card as one continuous HTML string."""
    html = (
        f'<div class="kpi-card">'
        f'<span class="kpi-label">{label}</span>'
        f'<span class="kpi-value">{value}</span>'
        f'<span class="kpi-description">{description}</span>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_driver_card(driver, team, average_lap, is_faster=False):
    """Render a driver comparison card."""
    card_class = "driver-card winner" if is_faster else "driver-card"
    status = '<span class="driver-status">● FASTER</span>' if is_faster else ""
    html = (
        f'<div class="{card_class}">'
        f'<span class="driver-code">{driver}</span>'
        f'<span class="driver-team">{team}</span>'
        f'<span class="driver-stat">{average_lap:.3f} s</span>'
        f'<span class="driver-stat-label">Average Lap</span>'
        f'{status}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_insight(title, text):
    """Render an insight box as one continuous HTML string."""
    html = (
        f'<div class="insight-box">'
        f'<span class="insight-title">💡 {title}</span>'
        f'<span class="insight-text">{text}</span>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_section_title(title):
    """Render a section heading."""
    st.markdown(
        f'<span class="section-title">{title}</span>',
        unsafe_allow_html=True,
    )


# ============================================================
# AUTOMATIC SEASON DISCOVERY
# ============================================================

CURRENT_YEAR = datetime.now().year

# Six latest completed seasons.
# In 2026 this becomes:
# 2025, 2024, 2023, 2022, 2021, 2020

AVAILABLE_SEASONS = list(
    range(
        CURRENT_YEAR - 1,
        CURRENT_YEAR - 7,
        -1,
    )
)


# ============================================================
# SIDEBAR - RACE SELECTION
# ============================================================

st.sidebar.markdown(
    '<span class="sidebar-section">🏁 Race Selection</span>',
    unsafe_allow_html=True,
)

season = st.sidebar.selectbox(
    "Season",
    AVAILABLE_SEASONS,
)


# ============================================================
# LOAD SEASON CALENDAR
# ============================================================

@st.cache_data
def get_season_events(selected_season):
    schedule = fastf1.get_event_schedule(
        selected_season,
        include_testing=False,
    ).copy()

    if "EventFormat" in schedule.columns:
        schedule = schedule[
            schedule["EventFormat"] != "testing"
        ].copy()

    if "RoundNumber" in schedule.columns:
        schedule = schedule[
            schedule["RoundNumber"].notna()
        ].copy()

        schedule = schedule[
            schedule["RoundNumber"] > 0
        ].copy()

        schedule = schedule.sort_values(
            "RoundNumber"
        )

    return schedule


with st.spinner(
    f"Loading {season} F1 calendar..."
):
    try:
        schedule = get_season_events(season)
    except Exception as exc:
        st.error(
            f"Unable to load the {season} F1 calendar."
        )
        st.exception(exc)
        st.stop()


if schedule.empty:
    st.error(
        "No Grand Prix events were found for this season."
    )
    st.stop()


# ============================================================
# GRAND PRIX SELECTION
# ============================================================

grand_prix_list = (
    schedule["EventName"]
    .dropna()
    .tolist()
)

grand_prix = st.sidebar.selectbox(
    "Grand Prix",
    grand_prix_list,
)


# ============================================================
# SESSION TYPE
# ============================================================

session_type = st.sidebar.selectbox(
    "Session",
    ["Race"],
)


# ============================================================
# LOAD FASTF1 SESSION
# ============================================================

@st.cache_data
def load_session(
    selected_season,
    selected_grand_prix,
    selected_session,
):
    session = fastf1.get_session(
        selected_season,
        selected_grand_prix,
        "R",
    )

    session.load()

    return session.laps


with st.spinner(
    f"Loading {season} {grand_prix}..."
):
    try:
        laps = load_session(
            season,
            grand_prix,
            session_type,
        )
    except Exception as exc:
        st.error(
            "Unable to load this F1 session."
        )
        st.exception(exc)
        st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

laps = laps.copy()

# Keep accurate laps with a valid lap time.
laps = laps[
    (laps["IsAccurate"] == True)
    & (laps["LapTime"].notna())
].copy()

# Convert timedelta to seconds.
laps["LapTimeSeconds"] = (
    laps["LapTime"].dt.total_seconds()
)

# Remove pit/in-lap and other abnormal values.
laps = laps[
    (laps["LapTimeSeconds"] > 60)
    & (laps["LapTimeSeconds"] < 120)
].copy()


if laps.empty:
    st.error(
        "No valid lap-time records are available "
        "after data cleaning."
    )
    st.stop()


# ============================================================
# AVAILABLE DRIVERS
# ============================================================

available_drivers = sorted(
    laps["Driver"]
    .dropna()
    .unique()
    .tolist()
)

if len(available_drivers) < 2:
    st.error(
        "Not enough driver data is available "
        "for this race."
    )
    st.stop()


# ============================================================
# SIDEBAR - DRIVER BATTLE
# ============================================================

st.sidebar.markdown(
    '<span class="sidebar-section">⚔️ Driver Battle</span>',
    unsafe_allow_html=True,
)

driver1 = st.sidebar.selectbox(
    "Driver 1",
    available_drivers,
)

driver2_options = [
    driver
    for driver in available_drivers
    if driver != driver1
]

driver2 = st.sidebar.selectbox(
    "Driver 2",
    driver2_options,
)


# ============================================================
# RESET BUTTON
# ============================================================

st.sidebar.divider()

if st.sidebar.button(
    "↻ Reset Selection",
    use_container_width=True,
):
    st.rerun()


# ============================================================
# DRIVER DATA
# ============================================================

d1 = laps[
    laps["Driver"] == driver1
].copy()

d2 = laps[
    laps["Driver"] == driver2
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

d1_avg = d1["LapTimeSeconds"].mean()
d2_avg = d2["LapTimeSeconds"].mean()

d1_fastest = d1["LapTimeSeconds"].min()
d2_fastest = d2["LapTimeSeconds"].min()

d1_median = d1["LapTimeSeconds"].median()
d2_median = d2["LapTimeSeconds"].median()

d1_laps = len(d1)
d2_laps = len(d2)

total_laps = int(
    laps["LapNumber"].max()
)

pace_difference = d1_avg - d2_avg


# ============================================================
# TEAM NAME
# ============================================================

def get_team(driver_data):
    if "Team" in driver_data.columns:
        teams = (
            driver_data["Team"]
            .dropna()
            .unique()
            .tolist()
        )

        if teams:
            return teams[0]

    return "Team unavailable"


team1 = get_team(d1)
team2 = get_team(d2)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<span class="main-title">🏎️ F1 RACE INTELLIGENCE</span>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<span class="main-subtitle">'
    f'{season} Season • Race Analytics'
    f'</span>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<span class="race-heading">'
    f'{grand_prix.upper()}'
    f'<span class="race-badge">RACE DATA</span>'
    f'</span>',
    unsafe_allow_html=True,
)

st.markdown(
    f'<span class="race-subheading">'
    f'{season} • {session_type}'
    f'</span>',
    unsafe_allow_html=True,
)

# Compact race snapshot shown before the main analysis.
compound_count = laps["Compound"].dropna().nunique()
driver_count = laps["Driver"].nunique()

st.markdown(
    f'<div class="summary-bar">'
    f'<div class="summary-item">'
    f'<span class="summary-label">Race Distance</span>'
    f'<span class="summary-value">{total_laps} laps</span>'
    f'<span class="summary-note">Completed race</span>'
    f'</div>'
    f'<div class="summary-item">'
    f'<span class="summary-label">Drivers</span>'
    f'<span class="summary-value">{driver_count}</span>'
    f'<span class="summary-note">With valid lap data</span>'
    f'</div>'
    f'<div class="summary-item">'
    f'<span class="summary-label">Tyre Compounds</span>'
    f'<span class="summary-value">{compound_count}</span>'
    f'<span class="summary-note">Recorded in race data</span>'
    f'</div>'
    f'<div class="summary-item">'
    f'<span class="summary-label">Driver Gap</span>'
    f'<span class="summary-value">{abs(pace_difference):.3f} s</span>'
    f'<span class="summary-note">Average pace difference</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)


# ============================================================
# DRIVER COMPARISON
# ============================================================

render_section_title("⚔️ Driver Comparison")

driver_col1, versus_col, driver_col2 = st.columns(
    [5, 1, 5]
)

with driver_col1:
    render_driver_card(
        driver1,
        team1,
        d1_avg,
        is_faster=d1_avg < d2_avg,
    )

with versus_col:
    st.markdown(
        '<span class="versus">VS</span>',
        unsafe_allow_html=True,
    )

with driver_col2:
    render_driver_card(
        driver2,
        team2,
        d2_avg,
        is_faster=d2_avg < d1_avg,
    )


# ============================================================
# RACE PERFORMANCE KPI CARDS
# ============================================================

render_section_title("📊 Race Performance")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:
    faster_driver = (
        driver1
        if d1_avg < d2_avg
        else driver2
    )

    fastest_average = min(
        d1_avg,
        d2_avg,
    )

    render_kpi(
        "Average Pace",
        f"{fastest_average:.3f} s",
        f"{faster_driver} fastest average",
    )


with kpi2:
    fastest_driver = (
        driver1
        if d1_fastest < d2_fastest
        else driver2
    )

    fastest_time = min(
        d1_fastest,
        d2_fastest,
    )

    render_kpi(
        "Fastest Lap",
        f"{fastest_time:.3f} s",
        fastest_driver,
    )


with kpi3:
    render_kpi(
        "Race Distance",
        str(total_laps),
        "Total race laps",
    )


with kpi4:
    if abs(pace_difference) < 0.001:
        gap_description = "Equal pace"
    else:
        gap_driver = (
            driver1
            if pace_difference < 0
            else driver2
        )

        gap_description = (
            f"{gap_driver} advantage per lap"
        )

    render_kpi(
        "Pace Gap",
        f"{abs(pace_difference):.3f} s",
        gap_description,
    )


# ============================================================
# TABS
# ============================================================

overview_tab, driver_tab, tyre_tab, data_tab = st.tabs(
    [
        "🏠 Overview",
        "🏎️ Driver Battle",
        "🛞 Tyre Strategy",
        "📊 Race Data",
    ]
)


# ============================================================
# OVERVIEW TAB
# ============================================================

with overview_tab:

    # --------------------------------------------------------
    # POSITION PROGRESSION
    # --------------------------------------------------------

    render_section_title("🏁 Position Progression")

    position_data = laps[
        laps["Driver"].isin(
            [driver1, driver2]
        )
    ].copy()

    position_data = position_data[
        position_data["Position"].notna()
    ].copy()

    fig_position = go.Figure()

    for driver in [driver1, driver2]:

        data = position_data[
            position_data["Driver"] == driver
        ]

        fig_position.add_trace(
            go.Scatter(
                x=data["LapNumber"],
                y=data["Position"],
                mode="lines+markers",
                name=driver,
                hovertemplate=(
                    "Lap: %{x}<br>"
                    "Position: %{y}"
                    "<extra></extra>"
                ),
            )
        )

    fig_position.update_layout(
        xaxis_title="Lap Number",
        yaxis_title="Race Position",
        yaxis=dict(
            autorange="reversed",
            dtick=1,
        ),
        hovermode="x unified",
        height=500,
    )

    st.plotly_chart(
        fig_position,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # RACE PACE EVOLUTION
    # --------------------------------------------------------

    render_section_title("📈 Race Pace Evolution")

    track_data = (
        laps
        .groupby("LapNumber")["LapTimeSeconds"]
        .mean()
        .reset_index()
    )

    fig_track = go.Figure()

    fig_track.add_trace(
        go.Scatter(
            x=track_data["LapNumber"],
            y=track_data["LapTimeSeconds"],
            mode="lines+markers",
            name="Average Race Pace",
            hovertemplate=(
                "Lap: %{x}<br>"
                "Average: %{y:.3f} s"
                "<extra></extra>"
            ),
        )
    )

    fig_track.update_layout(
        xaxis_title="Lap Number",
        yaxis_title="Average Lap Time (seconds)",
        hovermode="x unified",
        height=500,
    )

    st.plotly_chart(
        fig_track,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # AUTOMATIC INSIGHT
    # --------------------------------------------------------

    if not track_data.empty:

        first_laps = (
            track_data
            .head(min(5, len(track_data)))
            ["LapTimeSeconds"]
            .mean()
        )

        last_laps = (
            track_data
            .tail(min(5, len(track_data)))
            ["LapTimeSeconds"]
            .mean()
        )

        if first_laps > last_laps:

            improvement = (
                first_laps - last_laps
            )

            insight = (
                f"Average lap pace improved by "
                f"{improvement:.2f} seconds between "
                f"the opening and closing stages "
                f"of the race."
            )

        else:

            insight = (
                "Average race pace did not show a "
                "simple improving trend across the race."
            )

        render_insight(
            "Key Insight",
            insight,
        )


# ============================================================
# DRIVER BATTLE TAB
# ============================================================

with driver_tab:

    # --------------------------------------------------------
    # LAP TIME COMPARISON
    # --------------------------------------------------------

    render_section_title("📈 Lap Time Comparison")

    fig_lap = go.Figure()

    for driver, data in [
        (driver1, d1),
        (driver2, d2),
    ]:

        fig_lap.add_trace(
            go.Scatter(
                x=data["LapNumber"],
                y=data["LapTimeSeconds"],
                mode="lines+markers",
                name=driver,
                hovertemplate=(
                    "Lap: %{x}<br>"
                    "Lap Time: %{y:.3f} s"
                    "<extra></extra>"
                ),
            )
        )

    fig_lap.update_layout(
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        hovermode="x unified",
        height=500,
    )

    st.plotly_chart(
        fig_lap,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # DRIVER METRICS
    # --------------------------------------------------------

    render_section_title("⚡ Driver Metrics")

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        render_kpi(
            f"{driver1} Performance",
            f"{d1_fastest:.3f} s",
            (
                f"Fastest lap • "
                f"Median {d1_median:.3f} s • "
                f"{d1_laps} valid laps"
            ),
        )

    with metric_col2:
        render_kpi(
            f"{driver2} Performance",
            f"{d2_fastest:.3f} s",
            (
                f"Fastest lap • "
                f"Median {d2_median:.3f} s • "
                f"{d2_laps} valid laps"
            ),
        )


    # --------------------------------------------------------
    # SECTOR PERFORMANCE
    # --------------------------------------------------------

    render_section_title("🏎️ Sector Performance")

    sector_columns = [
        "Sector1Time",
        "Sector2Time",
        "Sector3Time",
    ]

    sector_names = [
        "Sector 1",
        "Sector 2",
        "Sector 3",
    ]

    sector_results = []

    for column, name in zip(
        sector_columns,
        sector_names,
    ):

        for driver, data in [
            (driver1, d1),
            (driver2, d2),
        ]:

            if column not in data.columns:
                continue

            values = (
                data[column]
                .dropna()
                .dt.total_seconds()
            )

            if len(values) == 0:
                continue

            sector_results.append(
                {
                    "Sector": name,
                    "Driver": driver,
                    "Average": values.mean(),
                }
            )

    sector_df = pd.DataFrame(
        sector_results
    )

    if not sector_df.empty:

        fig_sector = go.Figure()

        for driver in [
            driver1,
            driver2,
        ]:

            data = sector_df[
                sector_df["Driver"] == driver
            ]

            fig_sector.add_trace(
                go.Bar(
                    x=data["Sector"],
                    y=data["Average"],
                    name=driver,
                    text=[
                        f"{value:.3f}s"
                        for value in data["Average"]
                    ],
                    textposition="auto",
                )
            )

        fig_sector.update_layout(
            xaxis_title="Sector",
            yaxis_title="Average Sector Time (seconds)",
            barmode="group",
            height=450,
        )

        st.plotly_chart(
            fig_sector,
            use_container_width=True,
        )

        st.caption(
            "Lower sector time indicates faster pace."
        )


        # ----------------------------------------------------
        # SECTOR INSIGHT
        # ----------------------------------------------------

        sector_insights = []

        for sector in sector_names:

            values = (
                sector_df[
                    sector_df["Sector"] == sector
                ]
                .set_index("Driver")["Average"]
            )

            if (
                driver1 in values.index
                and driver2 in values.index
            ):

                difference = (
                    values[driver1]
                    - values[driver2]
                )

                if difference < 0:

                    sector_insights.append(
                        f"{driver1} is faster in {sector}"
                    )

                elif difference > 0:

                    sector_insights.append(
                        f"{driver2} is faster in {sector}"
                    )

        if sector_insights:

            sector_text = " • ".join(
                sector_insights
            )

            render_insight(
                "Sector Insight",
                sector_text,
            )


# ============================================================
# TYRE STRATEGY TAB
# ============================================================

with tyre_tab:

    strategy_driver = st.selectbox(
        "Select Driver",
        [driver1, driver2],
        key="strategy_driver",
    )

    strategy_data = laps[
        laps["Driver"] == strategy_driver
    ].copy()


    # --------------------------------------------------------
    # TYRE PERFORMANCE
    # --------------------------------------------------------

    render_section_title("🛞 Tyre Performance")

    tyre_data = strategy_data[
        strategy_data["TyreLife"].notna()
    ].copy()

    fig_tyre = go.Figure()

    for compound in (
        tyre_data["Compound"]
        .dropna()
        .unique()
    ):

        compound_data = tyre_data[
            tyre_data["Compound"] == compound
        ]

        fig_tyre.add_trace(
            go.Scatter(
                x=compound_data["TyreLife"],
                y=compound_data["LapTimeSeconds"],
                mode="lines+markers",
                name=compound,
                hovertemplate=(
                    "Tyre Age: %{x}<br>"
                    "Lap Time: %{y:.3f} s"
                    "<extra></extra>"
                ),
            )
        )

    fig_tyre.update_layout(
        xaxis_title="Tyre Age (laps)",
        yaxis_title="Lap Time (seconds)",
        hovermode="x unified",
        height=500,
    )

    st.plotly_chart(
        fig_tyre,
        use_container_width=True,
    )

    st.caption(
        "Lower lap time indicates faster pace. "
        "Tyre age alone does not isolate degradation."
    )


    # --------------------------------------------------------
    # STINT STRATEGY
    # --------------------------------------------------------

    render_section_title("🛞 Race Stint Strategy")

    stint_data = strategy_data[
        strategy_data["Stint"].notna()
        & strategy_data["Compound"].notna()
    ].copy()

    stint_summary = (
        stint_data
        .groupby(
            ["Stint", "Compound"]
        )
        .agg(
            Start_Lap=("LapNumber", "min"),
            End_Lap=("LapNumber", "max"),
            Laps=("LapNumber", "count"),
        )
        .reset_index()
    )

    if not stint_summary.empty:

        fig_strategy = go.Figure()

        for _, row in stint_summary.iterrows():

            stint = int(row["Stint"])
            start = row["Start_Lap"]
            end = row["End_Lap"]
            compound = row["Compound"]
            length = int(row["Laps"])

            fig_strategy.add_trace(
                go.Scatter(
                    x=[start, end],
                    y=[stint, stint],
                    mode="lines+markers",
                    name=(
                        f"Stint {stint} • "
                        f"{compound}"
                    ),
                    line=dict(width=16),
                    marker=dict(size=11),
                    hovertemplate=(
                        f"Stint: {stint}<br>"
                        f"Compound: {compound}<br>"
                        f"Start Lap: {start}<br>"
                        f"End Lap: {end}<br>"
                        f"Length: {length} laps"
                        "<extra></extra>"
                    ),
                )
            )

        fig_strategy.update_layout(
            xaxis_title="Lap Number",
            yaxis_title="Stint",
            height=420,
        )

        st.plotly_chart(
            fig_strategy,
            use_container_width=True,
        )


        # ----------------------------------------------------
        # STINT TABLE
        # ----------------------------------------------------

        st.dataframe(
            stint_summary[
                [
                    "Stint",
                    "Compound",
                    "Start_Lap",
                    "End_Lap",
                    "Laps",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )


        # ----------------------------------------------------
        # STRATEGY INSIGHT
        # ----------------------------------------------------

        compounds = stint_summary[
            "Compound"
        ].tolist()

        strategy_text = (
            f"{strategy_driver} used "
            f"{len(compounds)} stint(s): "
            f"{' → '.join(compounds)}."
        )

        render_insight(
            "Strategy Insight",
            strategy_text,
        )

    else:

        st.info(
            f"No tyre stint data is available "
            f"for {strategy_driver}."
        )


# ============================================================
# RACE DATA TAB
# ============================================================

with data_tab:

    # --------------------------------------------------------
    # CLEANED DATASET
    # --------------------------------------------------------

    render_section_title("📊 Cleaned Race Dataset")

    st.write(
        f"Showing {len(laps):,} cleaned lap records."
    )

    display_columns = [
        "Driver",
        "LapNumber",
        "LapTimeSeconds",
        "Compound",
        "TyreLife",
        "Stint",
        "Position",
        "TrackStatus",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in laps.columns
    ]

    st.dataframe(
        laps[available_columns],
        use_container_width=True,
        hide_index=True,
    )


    # --------------------------------------------------------
    # RACE INFORMATION
    # --------------------------------------------------------

    render_section_title("ℹ️ Race Information")

    info1, info2, info3 = st.columns(3)

    with info1:
        render_kpi(
            "Total Race Laps",
            str(total_laps),
            "Completed race distance",
        )

    with info2:
        driver_count = laps["Driver"].nunique()

        render_kpi(
            "Drivers",
            str(driver_count),
            "Drivers with lap data",
        )

    with info3:
        render_kpi(
            "Lap Records",
            f"{len(laps):,}",
            "Cleaned telemetry records",
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="app-footer">'
    '<strong>F1 Race Intelligence</strong><br>'
    'Powered by FastF1 • Built with Python & Streamlit'
    '</div>',
    unsafe_allow_html=True,
)
