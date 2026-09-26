from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# Page configuration
st.set_page_config(
    page_title="US Top 50 Playlist Analysis",
    page_icon="🎵",
    layout="wide"
)


# Project paths
project_root = Path(__file__).resolve().parent

processed_path = (
    project_root
    / "data"
    / "processed"
    / "Atlantic_United_States_processed.csv"
)

tables_path = project_root / "outputs" / "tables"


# Load processed dataset
@st.cache_data
def load_data():
    data = pd.read_csv(processed_path)

    data["date"] = pd.to_datetime(data["date"])

    return data


df = load_data()


# Load supporting KPI tables
@st.cache_data
def load_supporting_tables():

    kpi_summary = pd.read_csv(
        tables_path / "kpi_summary.csv"
    )

    artist_kpi = pd.read_csv(
        tables_path / "artist_kpi.csv"
    )

    song_kpi = pd.read_csv(
        tables_path / "song_kpi.csv"
    )

    content_kpi = pd.read_csv(
        tables_path / "content_kpi.csv"
    )

    return (
        kpi_summary,
        artist_kpi,
        song_kpi,
        content_kpi
    )


kpi_summary, artist_kpi, song_kpi, content_kpi = (
    load_supporting_tables()
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎵 United States Top 50 Playlist Performance Analysis")

st.markdown(
    """
This dashboard analyzes historical United States Top 50 playlist
performance, song longevity, artist presence, ranking behavior,
popularity, and content characteristics.

**Analysis period:** May 2024 – November 2025

The dashboard is descriptive and focuses on observed playlist behavior.
"""
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")


min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

else:

    start_date = pd.Timestamp(min_date)
    end_date = pd.Timestamp(max_date)


rank_range = st.sidebar.slider(
    "Chart position range",
    min_value=1,
    max_value=50,
    value=(1, 50)
)


artists = sorted(df["artist"].dropna().unique())

selected_artist = st.sidebar.selectbox(
    "Artist",
    ["All Artists"] + artists
)


album_types = sorted(
    df["album_type"].dropna().unique()
)

selected_album_type = st.sidebar.multiselect(
    "Album type",
    album_types,
    default=album_types
)


# Apply filters
filtered_df = df[
    (df["date"] >= start_date)
    & (df["date"] <= end_date)
    & (df["position"] >= rank_range[0])
    & (df["position"] <= rank_range[1])
].copy()


if selected_artist != "All Artists":

    filtered_df = filtered_df[
        filtered_df["artist"] == selected_artist
    ]


if selected_album_type:

    filtered_df = filtered_df[
        filtered_df["album_type"].isin(selected_album_type)
    ]


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Observations",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Unique Songs",
    f"{filtered_df[['song', 'artist']].drop_duplicates().shape[0]:,}"
)

col3.metric(
    "Unique Artists",
    f"{filtered_df['artist'].nunique():,}"
)

col4.metric(
    "Average Popularity",
    f"{filtered_df['popularity'].mean():.1f}"
)


col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Average Chart Position",
    f"{filtered_df['position'].mean():.1f}"
)

col6.metric(
    "Average Duration",
    f"{filtered_df['duration_minutes'].mean():.2f} min"
)

col7.metric(
    "Explicit Share",
    f"{filtered_df['is_explicit'].mean() * 100:.1f}%"
)

col8.metric(
    "Maximum Days on Chart",
    f"{filtered_df['days_on_chart'].max():.0f}"
)


# --------------------------------------------------
# PLAYLIST TIMELINE
# --------------------------------------------------

st.header("📈 Playlist Timeline")

daily_stats = (
    filtered_df
    .groupby("date")
    .agg(
        average_position=("position", "mean"),
        average_popularity=("popularity", "mean"),
        position_volatility=("position", "std"),
        unique_artists=("artist", "nunique"),
        unique_songs=("song", "nunique")
    )
    .reset_index()
)


timeline_metric = st.selectbox(
    "Select timeline metric",
    [
        "Average Chart Position",
        "Average Popularity",
        "Position Volatility",
        "Unique Artists",
        "Unique Songs"
    ]
)


metric_map = {
    "Average Chart Position": "average_position",
    "Average Popularity": "average_popularity",
    "Position Volatility": "position_volatility",
    "Unique Artists": "unique_artists",
    "Unique Songs": "unique_songs"
}


selected_metric = metric_map[timeline_metric]


fig_timeline = px.line(
    daily_stats,
    x="date",
    y=selected_metric,
    markers=False,
    title=timeline_metric
)

fig_timeline.update_layout(
    xaxis_title="Date",
    yaxis_title=timeline_metric,
    hovermode="x unified"
)

st.plotly_chart(
    fig_timeline,
    use_container_width=True
)


# --------------------------------------------------
# SONG RANKING TREND
# --------------------------------------------------

st.header("🎶 Song Ranking Trend")

available_songs = (
    filtered_df["song"]
    + " — "
    + filtered_df["artist"]
).drop_duplicates().sort_values().tolist()


if available_songs:

    selected_song_display = st.selectbox(
        "Select a song",
        available_songs
    )

    selected_song, selected_song_artist = (
        selected_song_display.split(" — ", 1)
    )

    song_data = filtered_df[
        (filtered_df["song"] == selected_song)
        & (filtered_df["artist"] == selected_song_artist)
    ].sort_values("date")


    fig_song = px.line(
        song_data,
        x="date",
        y="position",
        markers=True,
        title=f"{selected_song} — {selected_song_artist}"
    )

    fig_song.update_yaxes(
        autorange="reversed",
        title="Chart Position"
    )

    fig_song.update_xaxes(
        title="Date"
    )

    st.plotly_chart(
        fig_song,
        use_container_width=True
    )

else:

    st.info("No songs match the selected filters.")


# --------------------------------------------------
# ARTIST DOMINANCE
# --------------------------------------------------

st.header("👤 Artist Presence and Dominance")

artist_filtered = (
    filtered_df
    .groupby("artist")
    .agg(
        unique_songs=("song", "nunique"),
        total_appearances=("song", "count"),
        average_rank=("position", "mean"),
        average_popularity=("popularity", "mean")
    )
    .reset_index()
)


artist_filtered["dominance_percent"] = (
    artist_filtered["total_appearances"]
    / len(filtered_df)
) * 100


artist_filtered = artist_filtered.sort_values(
    "dominance_percent",
    ascending=False
)


fig_artist = px.bar(
    artist_filtered.head(20),
    x="dominance_percent",
    y="artist",
    orientation="h",
    title="Artist Share of Observed Chart Appearances"
)

fig_artist.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Share of Observations (%)",
    yaxis_title="Artist"
)

st.plotly_chart(
    fig_artist,
    use_container_width=True
)


st.dataframe(
    artist_filtered.head(20),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# POPULARITY VS RANK
# --------------------------------------------------

st.header("⭐ Popularity vs Chart Position")

fig_scatter = px.scatter(
    filtered_df,
    x="position",
    y="popularity",
    hover_name="song",
    hover_data=["artist", "album_type"],
    title="Popularity and Chart Position"
)

fig_scatter.update_layout(
    xaxis_title="Chart Position",
    yaxis_title="Popularity"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# --------------------------------------------------
# EXPLICIT CONTENT
# --------------------------------------------------

st.header("🔞 Explicit vs Non-Explicit Content")

explicit_analysis = (
    filtered_df
    .groupby("is_explicit")
    .agg(
        observations=("song", "count"),
        unique_songs=("song", "nunique"),
        average_rank=("position", "mean"),
        average_popularity=("popularity", "mean"),
        average_duration=("duration_minutes", "mean"),
        average_days_on_chart=("days_on_chart", "mean")
    )
    .reset_index()
)


explicit_analysis["content_type"] = (
    explicit_analysis["is_explicit"]
    .map({
        True: "Explicit",
        False: "Non-Explicit"
    })
)


col1, col2 = st.columns(2)


with col1:

    fig_explicit = px.bar(
        explicit_analysis,
        x="content_type",
        y="average_popularity",
        title="Average Popularity"
    )

    st.plotly_chart(
        fig_explicit,
        use_container_width=True
    )


with col2:

    fig_explicit_duration = px.bar(
        explicit_analysis,
        x="content_type",
        y="average_duration",
        title="Average Song Duration"
    )

    st.plotly_chart(
        fig_explicit_duration,
        use_container_width=True
    )


st.dataframe(
    explicit_analysis,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# ALBUM TYPE
# --------------------------------------------------

st.header("💿 Album Type Analysis")

album_analysis = (
    filtered_df
    .groupby("album_type")
    .agg(
        observations=("song", "count"),
        unique_songs=("song", "nunique"),
        average_rank=("position", "mean"),
        average_popularity=("popularity", "mean"),
        average_duration=("duration_minutes", "mean"),
        average_album_tracks=("total_tracks", "mean")
    )
    .reset_index()
)


col1, col2 = st.columns(2)


with col1:

    fig_album_popularity = px.bar(
        album_analysis,
        x="album_type",
        y="average_popularity",
        title="Popularity by Album Type"
    )

    st.plotly_chart(
        fig_album_popularity,
        use_container_width=True
    )


with col2:

    fig_album_rank = px.bar(
        album_analysis,
        x="album_type",
        y="average_rank",
        title="Average Chart Position by Album Type"
    )

    st.plotly_chart(
        fig_album_rank,
        use_container_width=True
    )


st.dataframe(
    album_analysis,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# DURATION ANALYSIS
# --------------------------------------------------

st.header("⏱️ Song Duration Analysis")

duration_analysis = (
    filtered_df
    .groupby("duration_category", observed=False)
    .agg(
        observations=("song", "count"),
        average_rank=("position", "mean"),
        average_popularity=("popularity", "mean"),
        average_days_on_chart=("days_on_chart", "mean")
    )
    .reset_index()
)


fig_duration = px.bar(
    duration_analysis,
    x="duration_category",
    y="average_popularity",
    title="Average Popularity by Song Duration"
)

st.plotly_chart(
    fig_duration,
    use_container_width=True
)


st.dataframe(
    duration_analysis,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# LONGEVITY LEADERBOARD
# --------------------------------------------------

st.header("🏆 Song Longevity")

longevity = (
    filtered_df[
        [
            "song",
            "artist",
            "days_on_chart",
            "average_rank",
            "best_rank",
            "average_popularity",
            "popularity_trend_score"
        ]
    ]
    .drop_duplicates(["song", "artist"])
    .sort_values(
        ["days_on_chart", "average_rank"],
        ascending=[False, True]
    )
)


st.dataframe(
    longevity.head(25),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "United States Top 50 Playlist Performance Analysis | "
    "Historical descriptive analytics | "
    "Primary analytical period: May 2024 – November 2025"
)