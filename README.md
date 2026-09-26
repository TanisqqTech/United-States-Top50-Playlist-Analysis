# United States Top 50 Playlist Performance and Song Popularity Trend Analysis

## Project Overview

This project analyzes historical United States Top 50 playlist snapshots to understand observed song ranking behavior, playlist longevity, artist presence, popularity, and content characteristics.

The project was developed as a descriptive analytics solution. It does not forecast future chart outcomes or generate automated music recommendations.

**Analysis period:** 18 May 2024 – 27 November 2025

---

## Business Context

For a music organization such as Atlantic Recording Corporation, historical playlist data can provide structured evidence about:

- Song longevity and ranking behavior
- Artist visibility and repeated playlist appearances
- Popularity patterns across chart positions
- Content characteristics such as explicit status and duration
- Historical changes in playlist composition

The project converts daily Top 50 snapshots into reusable analytical metrics, tables, visualizations, and an interactive dashboard.

---

## Problem Statement

A daily Top 50 snapshot provides only a point-in-time view of playlist performance. It does not directly show:

- How long a song remains observable on the chart
- Whether a song's ranking is stable or volatile
- Which artists repeatedly occupy playlist positions
- How popularity varies across ranking levels
- How content characteristics relate to observed playlist performance

This project addresses these gaps through song-level, artist-level, content-level, and time-based analysis.

---

## Objectives

1. Validate the daily Top 50 playlist records.
2. Identify and document data-quality anomalies.
3. Measure song longevity and ranking behavior.
4. Measure artist presence and dominance.
5. Examine popularity versus chart position.
6. Compare explicit and non-explicit content.
7. Compare album types, song durations, and album sizes.
8. Create time-based visualizations.
9. Provide an interactive Streamlit dashboard.
10. Produce reusable analytical tables and documentation.

---

## Dataset

The source dataset contains the following fields:

| Field | Description |
|---|---|
| `date` | Playlist snapshot date |
| `position` | Chart position from 1 to 50 |
| `song` | Song title |
| `artist` | Artist name |
| `popularity` | Source popularity score |
| `duration_ms` | Song duration in milliseconds |
| `album_type` | Album, single, or compilation |
| `total_tracks` | Number of tracks in the associated album |
| `is_explicit` | Explicit-content indicator |
| `album_cover_url` | Album artwork URL |

### Final Analytical Dataset

After cleaning:

- **27,700 observations**
- **554 valid chart dates**
- **977 unique song-artist combinations**
- **297 unique artists**
- Exactly **50 records per retained date**

---

## Data Cleaning

The raw dataset contained 27,800 records.

### 01 March 2025 anomaly

The date `01-03-2025` contained 100 records instead of the expected 50.

Investigation showed that every chart position from 1 to 50 occurred twice, indicating that two overlapping snapshots had been merged under the same date.

Because the source did not provide a snapshot identifier or timestamp, the analysis did not arbitrarily select one group of 50 records.

The cleaning process:

1. Removed 10 exact duplicate records.
2. Excluded the remaining anomalous date from the primary analytical dataset.
3. Verified that all retained dates contain exactly 50 records.
4. Used `song + artist` as the song identity.
5. Verified that no duplicate `song + artist + date` combinations remained.

The raw data is preserved separately from the processed analytical data.

---

## Methodology

### Song-Level Metrics

The project calculates:

- Days on Chart
- Average Rank
- Best Rank
- Worst Observed Rank
- Rank Volatility
- Average Popularity
- Popularity Volatility
- First Observed Popularity
- Last Observed Popularity
- Popularity Trend Score
- First Observed Date
- Last Observed Date

### Rank Movement

For each song-artist combination:

- Negative rank change = movement upward in the chart
- Positive rank change = movement downward
- Zero = no observed movement
- First observed record has no previous position

### Artist-Level Metrics

Artist analysis includes:

- Unique Songs
- Total Chart Days
- Total Appearances
- Average Rank
- Best Rank
- Average Popularity
- Artist Dominance Index
- Peak Daily Slots
- Peak Daily Dominance
- Days With Multiple Songs

### Artist Dominance Index

The Artist Dominance Index is defined as:

`artist appearances / total Top 50 observations × 100`

It represents an artist's share of all observed Top 50 song observations in the analytical dataset.

### Content Analysis

The project examines:

- Explicit vs non-explicit content
- Album vs single vs compilation
- Song duration categories
- Album-size categories

### Popularity Analysis

Popularity is examined using:

- Top 10
- Top 20
- Top 50
- Rank bands: 1–10, 11–20, 21–30, 31–40, 41–50
- Observation-level correlation
- Song-level correlation
- Rank/popularity volatility relationships
- Popularity trend categories

---

## Key Performance Indicators

| KPI | Observed Value |
|---|---:|
| Total observations | 27,700 |
| Unique chart dates | 554 |
| Unique songs | 977 |
| Unique artists | 297 |
| Average chart position | 25.5 |
| Average popularity | 87.7 |
| Average song duration | 3.31 minutes |
| Explicit content share | 47.9% |
| Maximum observed song longevity | 535 days |

---

## Visualizations

The project produces time-based visualizations including:

- Artist dominance over time
- Daily average chart position
- Daily average popularity
- Daily position volatility
- Daily Top 10 share
- Daily Top 20 share
- Daily unique artists

Additional analytical tables cover:

- Song longevity
- Peak ranking
- Fast risers
- Largest observed declines
- Popularity
- Volatility
- Artist presence
- Content attributes

---

## Streamlit Dashboard

The project includes an interactive Streamlit dashboard.

### Dashboard Features

- Date range filtering
- Chart position filtering
- Artist filtering
- Album type filtering
- KPI cards
- Playlist timeline
- Song ranking trend
- Artist presence and dominance
- Popularity vs chart position
- Explicit vs non-explicit comparison
- Album type analysis
- Duration analysis
- Song longevity table

### Run Locally

Install the required packages:

```bash
pip install -r requirements.txt