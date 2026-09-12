from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu


BASE_DIR = Path(__file__).resolve().parent
#BASE_DIR = Path('/Users/brianxiong/Desktop/Data_Science_Stuff/Mobile Apps')
DATA_FILE = BASE_DIR / "data" / "mobile_apps_unified.csv"
IOS_FILE = BASE_DIR / "data" / "ios_apps_clean.csv"
ANDROID_FILE = BASE_DIR / "data" / "android_apps_clean.csv"
QUALITY_FILE = BASE_DIR / "data_quality_summary.json"
HERO_IMAGE = BASE_DIR / "assets" / "mobile-market-hero.png"
OPPORTUNITY_IMAGE = BASE_DIR / "assets" / "category-opportunities.png"
ECOSYSTEM_IMAGE = BASE_DIR / "assets" / "cross-platform-ecosystem.png"
MARKET_GAP_IMAGE = BASE_DIR / "assets" / "market-gap-lens.png"

FRIENDLY_NAMES = {
    "platform": "App store",
    "app_id": "Store app ID",
    "app_key": "Unique app key",
    "app_name": "App name",
    "category": "Category",
    "content_rating": "Store age/content rating",
    "content_rating_normalized": "Age/content rating",
    "price": "Price",
    "currency": "Currency used",
    "is_free": "Is free",
    "user_rating": "User rating (0–5)",
    "rating_count": "Number of ratings",
    "review_count": "Written reviews",
    "reviews_per_1k_installs": "Reviews per 1K installs",
    "app_size_mb": "App size (MB)",
    "min_installs": "Lower install estimate",
    "max_installs": "Upper install estimate",
    "supported_languages_count": "Supported language count",
    "supported_devices_count": "Supported device count",
    "contains_ads": "Shows ads",
    "in_app_purchases": "In-app purchases",
    "developer": "Developer",
    "updated_at": "Updated date",
}

SECTIONS = [
    "Home",
    "About the Study",
    "How Data Was Prepared",
    "View the Data",
    "Explore the Data",
    "Popularity & Ratings",
    "Reviews & Competition",
    "Checks & Limitations",
    "What to Do Next",
]

SECTION_ICONS = [
    "bookmark",
    "book",
    "database-check",
    "table",
    "bar-chart",
    "activity",
    "people",
    "shield-check",
    "check2-circle",
]

EXPLORATION_PAGES = [
    "Overview",
    "Compare with Bars",
    "Compare Ranges",
    "Compare Two Measures",
    "Parts of a Whole",
    "Explore by Rings",
    "View App List",
]

EXPLORATION_ICONS = [
    "speedometer2",
    "bar-chart-steps",
    "box",
    "graph-up",
    "pie-chart",
    "bullseye",
    "table",
]

ACCENT_COLOR = "#f45b5b"

COLOR_PALETTES = {
    "Plotly": px.colors.qualitative.Plotly,
    "Color-safe": px.colors.qualitative.Safe,
    "Vivid": px.colors.qualitative.Vivid,
    "Pastel": px.colors.qualitative.Pastel,
}

QUALITY_CHECK_NAMES = {
    "ios_unique_app_ids": "Every iPhone app has a unique ID",
    "android_unique_app_ids": "Every Android app has a unique ID",
    "unified_unique_app_keys": "Every app in the combined list is unique",
    "ios_rating_range_valid": "All iPhone ratings are between 0 and 5",
    "android_rating_range_valid": "All Android ratings are between 0 and 5",
    "prices_nonnegative": "No app has a price below zero",
    "free_price_consistency": "Apps marked free have a zero price",
    "row_reconciliation": "No apps were lost when the two lists were combined",
}

CLEANING_CHANGE_NAMES = {
    "Renamed columns to descriptive snake_case names.": "Gave columns clear, consistent names.",
    "Renamed chart-relevant columns to descriptive snake_case names.": "Gave chart columns clear, consistent names.",
    "Trimmed leading and trailing whitespace in text fields.": "Removed accidental spaces before and after text.",
    "Added platform, app_size_mb, is_free, and normalized content-rating fields.": "Added store, app size, free/paid, and consistent age-rating information.",
    "Converted the volume-purchase indicator to a Boolean field.": "Changed the bulk-purchase field into a simple yes/no value.",
    "Retained same-name apps because their app IDs are different.": "Kept apps with the same name when their store IDs were different.",
    "Removed nine columns that were entirely empty.": "Removed nine columns that contained no information.",
    "Trimmed outer whitespace and removed HTML tags from descriptions and summaries.": "Removed accidental spaces and webpage formatting from descriptions.",
    "Converted ratings, reviews, and install counts to nullable numeric types.": "Prepared ratings, reviews, and install numbers for calculations while keeping unknown values blank.",
    "Converted Unix/update and scrape timestamps to ISO 8601 UTC text.": "Changed update and collection dates into one consistent date format.",
    "Added platform, normalized content-rating, and text-length fields.": "Added store, consistent age-rating, and description-length information.",
    "Retained missing ratings and installs as missing; no statistical imputation was used.": "Left unknown ratings and install numbers blank instead of guessing them.",
}


def label(column: str) -> str:
    return FRIENDLY_NAMES.get(column, column.replace("_", " ").title())


def friendly_option(value: str) -> str:
    """Format dataset column choices without changing their underlying values."""
    return value if value.startswith("(") else label(value)


def preferred_index(options: list[str], *preferred: str) -> int:
    for choice in preferred:
        if choice in options:
            return options.index(choice)
    return 0


def query_value(name: str) -> str:
    """Return one query-string value across Streamlit and AppTest representations."""
    value = st.query_params.get(name, "")
    if isinstance(value, list):
        return value[0] if value else ""
    return value


def navigation_index(
    options: list[str],
    state_key: str,
    query_parameter: str,
) -> int:
    """Use a valid link target first, then fall back to the saved page."""
    requested = query_value(query_parameter)
    if requested in options:
        return options.index(requested)
    selected = st.session_state.get(state_key)
    if selected in options:
        return options.index(selected)
    return 0


def option_menu_styles(mode: str, *, horizontal: bool = False) -> dict:
    """Create readable option-menu colors for the selected appearance."""
    if mode == "Dark":
        surface, text, hover = "#1b1f2a", "#f4f6fb", "#292f3e"
    else:
        surface, text, hover = "#ffffff", "#172033", "#eef2f8"

    return {
        "container": {
            "padding": "4px",
            "background-color": surface,
            # The sidebar menu lives in an iframe. Square inner corners prevent
            # the iframe's default background from showing through in dark mode.
            "border-radius": "12px" if horizontal else "0px",
        },
        # Let icons inherit the link color so selected icons become white.
        "icon": {"font-size": "16px"},
        "nav-link": {
            "color": text,
            "font-size": "14px",
            "font-weight": "500",
            "text-align": "center" if horizontal else "left",
            "margin": "2px",
            "border-radius": "9px",
            "--hover-color": hover,
        },
        "nav-link-selected": {
            "background-color": ACCENT_COLOR,
            "color": "#ffffff",
            "font-weight": "650",
        },
    }


@st.cache_data
def load_data() -> pd.DataFrame:
    frame = pd.read_csv(DATA_FILE, low_memory=False)
    frame = exclude_other_category(frame)
    for column in [
        "price",
        "user_rating",
        "rating_count",
        "review_count",
        "app_size_mb",
        "min_installs",
        "max_installs",
        "supported_languages_count",
        "supported_devices_count",
    ]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    for column in ["is_free", "contains_ads", "in_app_purchases"]:
        frame[column] = frame[column].astype("boolean")
    return frame


@st.cache_data
def load_quality_report() -> dict:
    with QUALITY_FILE.open(encoding="utf-8") as source:
        return json.load(source)


@st.cache_data
def load_cleaned_sources() -> tuple[pd.DataFrame, pd.DataFrame]:
    return (
        exclude_other_category(pd.read_csv(IOS_FILE, low_memory=False)),
        exclude_other_category(pd.read_csv(ANDROID_FILE, low_memory=False)),
    )


def exclude_other_category(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove rows whose source category is the uninformative Other label."""
    if "category" not in frame.columns:
        return frame
    is_other = frame["category"].astype("string").str.strip().str.casefold().eq("other")
    return frame.loc[~is_other.fillna(False)].copy()


def numeric_columns(frame: pd.DataFrame) -> list[str]:
    excluded = {"app_id"}
    return [
        column
        for column in frame.columns
        if column not in excluded
        and pd.api.types.is_numeric_dtype(frame[column])
        and not pd.api.types.is_bool_dtype(frame[column])
        and frame[column].notna().any()
    ]


def categorical_columns(frame: pd.DataFrame) -> list[str]:
    excluded = {"app_id", "app_key", "app_name", "developer", "icon_url", "updated_at"}
    candidates = []
    for column in frame.columns:
        unique_count = frame[column].nunique(dropna=True)
        if column not in excluded and 1 < unique_count <= 80:
            candidates.append(column)
    return candidates


def limit_categories(frame: pd.DataFrame, column: str, limit: int) -> pd.DataFrame:
    result = frame.copy()
    values = result[column].astype("string").fillna("(Missing)")
    top_values = values.value_counts().head(limit).index
    return result.loc[values.isin(top_values)].copy()


def demand_proxy_correlations(frame: pd.DataFrame) -> tuple[pd.DataFrame, float, float, float]:
    """Return comparable Android demand fields and their key correlations."""
    valid = frame.loc[
        frame["platform"].eq("Android"),
        ["rating_count", "max_installs"],
    ].dropna()
    if len(valid) < 2:
        return valid, float("nan"), float("nan"), float("nan")
    raw = valid["rating_count"].corr(valid["max_installs"])
    log_scaled = valid["rating_count"].map(math.log1p).corr(
        valid["max_installs"].map(math.log1p)
    )
    ranked = valid["rating_count"].rank().corr(valid["max_installs"].rank())
    return valid, raw, log_scaled, ranked


def category_rating_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarize apps rated from 2 up to 4 while preserving demand context."""
    rated = frame.dropna(subset=["category", "user_rating", "rating_count"]).copy()
    rated = rated.loc[
        rated["user_rating"].ge(2.0)
        & rated["user_rating"].lt(4.0)
        & rated["rating_count"].gt(0)
    ]
    rated["weighted_rating_total"] = rated["user_rating"] * rated["rating_count"]
    summary = (
        rated.groupby("category", as_index=False)
        .agg(
            app_count=("app_key", "size"),
            total_rating_count=("rating_count", "sum"),
            weighted_rating_total=("weighted_rating_total", "sum"),
            platform_count=("platform", "nunique"),
        )
    )
    summary["weighted_user_rating"] = (
        summary["weighted_rating_total"] / summary["total_rating_count"]
    )
    return summary.loc[
        summary["app_count"].ge(10) & summary["total_rating_count"].ge(10_000)
    ].copy()


def finish_figure(figure, title: str):
    mode = st.session_state.get("appearance_mode", "Dark")
    is_dark = mode == "Dark"
    template = "plotly_dark" if is_dark else "plotly_white"
    text_color = "#f4f6fb" if is_dark else "#172033"
    grid_color = "#343b4a" if is_dark else "#d9e0eb"
    figure.update_layout(
        template=template,
        title=title,
        font=dict(color=text_color),
        title_font=dict(color=text_color),
        legend_font=dict(color=text_color),
        margin=dict(l=20, r=20, t=70, b=20),
        legend_title_text="",
        hoverlabel=dict(namelength=-1, font=dict(color=text_color)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        uirevision=f"appearance-{mode}",
        height=st.session_state.get("chart_height", 520),
        showlegend=st.session_state.get("show_chart_legend", True),
    )
    figure.update_xaxes(color=text_color, gridcolor=grid_color, zerolinecolor=grid_color)
    figure.update_yaxes(color=text_color, gridcolor=grid_color, zerolinecolor=grid_color)
    for trace_type in ["pie", "sunburst"]:
        figure.update_traces(
            textfont=dict(color=text_color),
            insidetextfont=dict(color=text_color),
            outsidetextfont=dict(color=text_color),
            selector=dict(type=trace_type),
        )
    return figure


def apply_appearance(mode: str) -> None:
    if mode == "Dark":
        background = "#0a0d14"
        sidebar = "#111521"
        surface = "#151a26"
        surface_alt = "#1b2130"
        text = "#f4f6fb"
        muted = "#9ca7ba"
        border = "#2a3242"
        accent_soft = "rgba(244, 91, 91, .14)"
        shadow = "0 18px 45px rgba(0, 0, 0, .22)"
        color_scheme = "dark"
    else:
        background = "#f5f6fa"
        sidebar = "#fbfbfd"
        surface = "#ffffff"
        surface_alt = "#f8f3f4"
        text = "#172033"
        muted = "#667085"
        border = "#e2e5ec"
        accent_soft = "rgba(244, 91, 91, .10)"
        shadow = "0 18px 45px rgba(31, 38, 54, .08)"
        color_scheme = "light"

    st.markdown(
        f"""
        <style>
        :root {{ color-scheme: {color_scheme}; }}
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        [data-testid="stDecoration"] {{ display: none !important; }}
        [data-testid="stAppViewContainer"], .stApp {{
            background:
                radial-gradient(circle at 82% 4%, {accent_soft}, transparent 27rem),
                {background} !important;
            color: {text} !important;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            background: {sidebar} !important;
            border-right: 1px solid {border};
        }}
        .block-container {{
            max-width: 1440px;
            padding-top: 1.4rem;
            padding-bottom: 4rem;
        }}
        .stApp h1 {{
            font-size: clamp(2.25rem, 4vw, 4.25rem);
            line-height: 1.02;
            letter-spacing: -.045em;
            font-weight: 780;
        }}
        .stApp h2 {{
            margin-top: 1.5rem;
            letter-spacing: -.025em;
            font-weight: 720;
        }}
        .stApp h3 {{ letter-spacing: -.015em; }}
        [data-testid="stMetric"], [data-testid="stExpander"] {{
            background: {surface} !important;
            border: 1px solid {border};
            border-radius: 1.15rem;
            box-shadow: {shadow};
        }}
        [data-testid="stMetric"] {{
            padding: 1rem 1.1rem;
            min-height: 112px;
            overflow: visible;
        }}
        [data-testid="stMetricLabel"] p {{
            color: {muted} !important;
            font-size: .78rem !important;
            letter-spacing: .045em;
            text-transform: uppercase;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.35 !important;
        }}
        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] > div {{
            color: {text} !important;
            letter-spacing: -.035em;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
            line-height: 1.15 !important;
        }}
        [data-testid="stMetricDelta"] {{
            color: {muted} !important;
            white-space: normal !important;
            overflow: visible !important;
            text-overflow: clip !important;
        }}
        [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] {{
            background: {surface};
            border: 1px solid {border};
            border-radius: 1.15rem;
            box-shadow: {shadow};
            overflow: hidden;
        }}
        [data-testid="stImage"] img {{
            border: 1px solid {border};
            border-radius: 1.35rem;
            box-shadow: {shadow};
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p,
        .stApp label, [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {{
            color: {text} !important;
        }}
        .stApp small, .stApp [data-testid="stCaptionContainer"] p {{
            color: {muted} !important;
        }}
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"],
        [data-testid="stTextInputRootElement"] {{
            background: {surface} !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stSelectbox"]
        .react-aria-ComboBox > div,
        [data-testid="stSidebar"] [data-testid="stMultiSelect"]
        .react-aria-ComboBox > div,
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {{
            background: {surface} !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stSidebar"] [role="combobox"] {{
            color: {text} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {{
            background: {surface} !important;
            color: {text} !important;
            border: 1px solid {border} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {{
            color: {text} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] {{
            background: #f45b5b !important;
            color: #ffffff !important;
            border: 1px solid #f45b5b !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p {{
            color: #ffffff !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-segmented_control"] {{
            background: {surface} !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-segmented_control"] p {{
            color: {text} !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-segmented_controlActive"] {{
            background: #f45b5b !important;
            color: #ffffff !important;
            border-color: #f45b5b !important;
        }}
        [data-testid="stSidebar"] [data-testid="stBaseButton-segmented_controlActive"] p {{
            color: #ffffff !important;
        }}
        [data-testid="stSidebar"] [role="radiogroup"]
        button[role="radio"][aria-checked="false"] {{
            background: {surface} !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stSidebar"] [role="radiogroup"]
        button[role="radio"][aria-checked="false"] p {{
            color: {text} !important;
        }}
        [data-testid="stSidebar"] [role="radiogroup"]
        button[role="radio"][aria-checked="true"] {{
            background: #f45b5b !important;
            color: #ffffff !important;
            border-color: #f45b5b !important;
        }}
        [data-testid="stSidebar"] [role="radiogroup"]
        button[role="radio"][aria-checked="true"] p {{
            color: #ffffff !important;
        }}
        .stButton > button, .stDownloadButton > button {{
            border-radius: .8rem !important;
            border: 1px solid {border} !important;
            min-height: 2.75rem;
            font-weight: 650;
            transition: transform .16s ease, border-color .16s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            border-color: #f45b5b !important;
            transform: translateY(-1px);
        }}
        [data-baseweb="tab-list"] {{
            gap: .35rem;
            background: {surface};
            border: 1px solid {border};
            border-radius: .9rem;
            padding: .3rem;
        }}
        [data-baseweb="tab"] {{ border-radius: .65rem; }}
        [data-baseweb="tab-highlight"] {{ background-color: #f45b5b; }}
        .hero-kicker {{
            display: inline-flex;
            align-items: center;
            gap: .45rem;
            padding: .45rem .75rem;
            margin-bottom: .8rem;
            border: 1px solid rgba(244, 91, 91, .3);
            border-radius: 999px;
            background: {accent_soft};
            color: #f45b5b;
            font-size: .73rem;
            font-weight: 750;
            letter-spacing: .11em;
            text-transform: uppercase;
        }}
        .hero-subtitle {{
            max-width: 820px;
            margin: -.55rem 0 1.35rem;
            color: {muted} !important;
            font-size: clamp(1rem, 1.55vw, 1.2rem);
            line-height: 1.65;
        }}
        .sidebar-brand {{
            padding: .95rem 1rem;
            margin: .2rem 0 1rem;
            background: linear-gradient(135deg, {accent_soft}, transparent);
            border: 1px solid {border};
            border-radius: 1rem;
        }}
        .sidebar-brand strong {{
            display: block;
            color: {text} !important;
            font-size: 1rem;
            letter-spacing: -.01em;
        }}
        .sidebar-brand span {{ color: {muted}; font-size: .76rem; }}
        .insight-card {{
            padding: 1.15rem 1.25rem;
            margin: .75rem 0 1.1rem;
            background: linear-gradient(135deg, {accent_soft}, {surface_alt});
            border: 1px solid rgba(244, 91, 91, .28);
            border-radius: 1.1rem;
        }}
        .insight-card p {{ margin: 0; line-height: 1.65; }}
        .insight-card strong {{ color: #f45b5b; }}
        .summary-card {{
            min-height: 188px;
            height: 100%;
            padding: 1.15rem 1.25rem;
            background: {surface};
            border: 1px solid {border};
            border-radius: 1.1rem;
            box-shadow: {shadow};
        }}
        .summary-card .summary-label {{
            display: block;
            color: {muted};
            font-size: .76rem;
            font-weight: 700;
            letter-spacing: .055em;
            line-height: 1.35;
            text-transform: uppercase;
        }}
        .summary-card strong {{
            display: block;
            margin: .55rem 0 .35rem;
            color: {text};
            font-size: clamp(1.9rem, 3vw, 2.65rem);
            letter-spacing: -.04em;
            line-height: 1;
        }}
        .summary-card p {{
            margin: .25rem 0 0;
            color: {muted} !important;
            font-size: .88rem;
            line-height: 1.45;
            overflow-wrap: anywhere;
        }}
        .framework-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .8rem;
            margin: .8rem 0 1.5rem;
        }}
        .framework-card {{
            min-height: 158px;
            padding: 1rem;
            background: {surface};
            border: 1px solid {border};
            border-radius: 1rem;
            box-shadow: {shadow};
        }}
        .framework-card .framework-icon {{
            display: block;
            margin-bottom: .65rem;
            font-size: 1.35rem;
        }}
        .framework-card strong {{ display: block; margin-bottom: .3rem; }}
        .framework-card span {{ color: {muted}; font-size: .88rem; line-height: 1.5; }}
        @media (max-width: 900px) {{
            .framework-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        }}
        @media (max-width: 560px) {{
            .framework-grid {{ grid-template-columns: 1fr; }}
        }}
        hr {{ border-color: {border} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_text(value: float | int | None, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    if abs(float(value)) >= 1_000_000:
        return f"{float(value) / 1_000_000:,.{digits}f}M"
    if abs(float(value)) >= 1_000:
        return f"{float(value) / 1_000:,.{digits}f}K"
    return f"{float(value):,.{digits}f}"


def format_table_for_display(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply friendly headings and readable number formats without changing downloads."""
    display = frame.copy()
    whole_number_columns = [
        "rating_count",
        "review_count",
        "min_installs",
        "max_installs",
        "supported_languages_count",
        "supported_devices_count",
    ]
    decimal_formats = {
        "price": 2,
        "user_rating": 2,
        "app_size_mb": 1,
        "reviews_per_1k_installs": 3,
    }
    for column in whole_number_columns:
        if column in display.columns:
            display[column] = display[column].map(
                lambda value: None if pd.isna(value) else f"{float(value):,.0f}"
            )
    for column, digits in decimal_formats.items():
        if column in display.columns:
            display[column] = display[column].map(
                lambda value, digits=digits: (
                    None if pd.isna(value) else f"{float(value):,.{digits}f}"
                )
            )
    return display.rename(columns={column: label(column) for column in display.columns})


def render_page_kicker(text: str) -> None:
    """Render a compact editorial label above a primary page heading."""
    st.markdown(
        f'<div class="hero-kicker">{text}</div>',
        unsafe_allow_html=True,
    )


def render_cleaned_dataset(
    frame: pd.DataFrame,
    source_file: Path,
    store_name: str,
) -> None:
    """Show one cleaned dataset with consistent metrics and download controls."""
    row_metric, column_metric, missing_metric = st.columns(3)
    row_metric.metric("Apps", f"{len(frame):,}")
    column_metric.metric("Details available", f"{len(frame.columns):,}")
    missing_metric.metric("Blank entries", f"{int(frame.isna().sum().sum()):,}")
    display = format_table_for_display(frame)
    st.dataframe(display, width="stretch", height=560, hide_index=True)
    st.download_button(
        f"Download cleaned {store_name} CSV",
        source_file.read_bytes(),
        file_name=source_file.name,
        mime="text/csv",
    )


def category_market_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Return category demand, satisfaction, competition, and concentration signals."""
    apps = (
        frame.dropna(subset=["category"])
        .groupby("category", as_index=False)
        .agg(app_count=("app_key", "size"), platform_count=("platform", "nunique"))
    )
    rated = frame.dropna(
        subset=["category", "user_rating", "rating_count"]
    ).copy()
    rated = rated.loc[rated["rating_count"].gt(0)]
    rated["weighted_rating_total"] = rated["user_rating"] * rated["rating_count"]
    demand = (
        rated.groupby("category", as_index=False)
        .agg(
            rated_app_count=("app_key", "size"),
            total_rating_count=("rating_count", "sum"),
            weighted_rating_total=("weighted_rating_total", "sum"),
        )
    )
    demand["weighted_user_rating"] = (
        demand["weighted_rating_total"] / demand["total_rating_count"]
    )
    leaders = (
        rated.sort_values("rating_count", ascending=False)
        .groupby("category", as_index=False)
        .first()[["category", "app_name", "rating_count"]]
        .rename(
            columns={
                "app_name": "leading_app",
                "rating_count": "leading_rating_count",
            }
        )
    )
    summary = apps.merge(demand, on="category", how="left").merge(
        leaders, on="category", how="left"
    )
    summary["leading_app_share"] = (
        summary["leading_rating_count"] / summary["total_rating_count"] * 100
    )
    return summary


def render_demand_satisfaction(frame: pd.DataFrame) -> None:
    render_page_kicker("Question one · do people want it?")
    st.title("Popularity & Ratings")
    st.caption(
        "First check whether rating totals are a useful sign of popularity. Then look for popular apps with weaker ratings."
    )

    validation, raw, log_scaled, ranked = demand_proxy_correlations(frame)
    st.info(
        f"Across **{len(validation):,} Android apps**, the relationship between the number of "
        f"ratings and the upper install estimate is **{raw:.2f}** in a direct comparison, "
        f"**{log_scaled:.2f}** when very large apps are scaled down, and **{ranked:.2f}** when "
        "apps are compared by popularity order. Values closer to 1 mean a stronger match. This "
        "makes rating totals a useful sign of relative popularity, but they are not a user count."
    )
    metric_columns = st.columns(4)
    metric_columns[0].metric("Android apps", f"{len(validation):,}")
    metric_columns[1].metric("Direct relationship", f"{raw:.2f}")
    metric_columns[2].metric("Across app sizes", f"{log_scaled:.2f}")
    metric_columns[3].metric("Popularity-order match", f"{ranked:.2f}")

    positive = frame.loc[
        frame["platform"].eq("Android")
        & frame["rating_count"].gt(0)
        & frame["max_installs"].gt(0)
    ].dropna(subset=["rating_count", "max_installs"]).copy()
    display = positive.sample(5_000, random_state=42) if len(positive) > 5_000 else positive
    figure = px.scatter(
        display,
        x="rating_count",
        y="max_installs",
        hover_name="app_name",
        hover_data={"category": True, "user_rating": ":.1f"},
        log_x=True,
        log_y=True,
        opacity=0.35,
        labels={column: label(column) for column in display.columns},
    )
    figure.update_traces(marker=dict(color=ACCENT_COLOR, size=7))
    st.plotly_chart(
        finish_figure(figure, "Do Android ratings rise with estimated installs?"),
        width="stretch",
        theme=None,
    )
    st.caption(
        "The chart compresses very large values so small and large apps can be seen together. "
        "Apps with zero ratings or installs are left out of the chart but included in the "
        "relationship scores above. Showing a sample of points does not change those scores."
    )

    st.divider()
    st.subheader("Popularity compared with user rating")
    controls, plot = st.columns([1, 3], gap="large")
    demand_floor = controls.select_slider(
        "Ratings needed to count as popular",
        options=[1_000, 10_000, 100_000, 1_000_000, 10_000_000],
        value=100_000,
        format_func=lambda value: metric_text(value, 0),
    )
    rating_ceiling = controls.slider(
        "Rating that counts as room for improvement", 2.5, 4.5, 3.5, 0.1
    )
    controls.markdown(
        "**Top left:** popular, with room to improve  \n"
        "**Top right:** popular and highly rated  \n"
        "**Bottom:** less evidence of popularity"
    )
    quadrant = frame.dropna(
        subset=["rating_count", "user_rating", "category", "app_name"]
    ).copy()
    quadrant = quadrant.loc[quadrant["rating_count"].gt(0)]
    quadrant = limit_categories(quadrant, "category", 12)
    candidates = quadrant.loc[
        quadrant["rating_count"].ge(demand_floor)
        & quadrant["user_rating"].le(rating_ceiling)
    ].nlargest(12, "rating_count")
    quadrant["chart_label"] = quadrant["app_name"].where(
        quadrant.index.isin(candidates.index), ""
    )
    if len(quadrant) > 5_000:
        keep = candidates.index
        sampled = quadrant.drop(index=keep, errors="ignore").sample(
            min(5_000 - len(keep), len(quadrant.drop(index=keep, errors="ignore"))),
            random_state=42,
        )
        quadrant = pd.concat([quadrant.loc[quadrant.index.intersection(keep)], sampled])
    quadrant_figure = px.scatter(
        quadrant,
        x="rating_count",
        y="user_rating",
        color="category",
        text="chart_label",
        hover_name="app_name",
        hover_data=["platform", "developer"],
        log_x=True,
        opacity=0.62,
        labels={column: label(column) for column in quadrant.columns},
    )
    quadrant_figure.add_vline(x=demand_floor, line_dash="dash", line_color="#ffd166")
    quadrant_figure.add_hline(y=rating_ceiling, line_dash="dash", line_color=ACCENT_COLOR)
    quadrant_figure.update_traces(textposition="top center", textfont_size=10)
    plot.plotly_chart(
        finish_figure(quadrant_figure, "Number of ratings compared with user rating"),
        width="stretch",
        theme=None,
    )
    st.markdown(
        f"**What this shows:** {len(candidates):,} labeled apps in the 12 largest categories "
        "meet both choices above. They are ideas worth checking—not proof that customers need "
        "a new product."
    )

    st.divider()
    st.subheader("Category overview and differences between apps")
    summary = category_market_summary(frame).dropna(
        subset=["weighted_user_rating", "total_rating_count"]
    )
    summary = summary.loc[
        summary["rated_app_count"].ge(10) & summary["total_rating_count"].ge(10_000)
    ].copy()
    summary["chart_label"] = summary["category"].where(
        summary["category"].isin(["Food & Drink", "Tools", "Communication"]), ""
    )
    bubble = px.scatter(
        summary,
        x="weighted_user_rating",
        y="total_rating_count",
        size="app_count",
        color="weighted_user_rating",
        text="chart_label",
        hover_name="category",
        hover_data={"app_count": ":,", "rated_app_count": ":,"},
        log_y=True,
        size_max=42,
        color_continuous_scale="RdYlGn",
        range_color=[2.5, 5.0],
        labels={
            "weighted_user_rating": "Overall rating, with popular apps counting more",
            "total_rating_count": "Total number of ratings",
            "app_count": "Apps",
        },
    )
    bubble.update_traces(textposition="top center")
    st.plotly_chart(
        finish_figure(bubble, "Category popularity, user rating, and number of apps"),
        width="stretch",
        theme=None,
    )
    st.info(
        "The overall ratings are strong for all three highlighted categories. The possible opening "
        "is narrower: many ratings belong to apps rated from 2.0 up to, but not including, 4.0. "
        "That suggests looking for specific problems to fix, not calling the whole category poor."
    )

    focus = frame.loc[
        frame["category"].isin(["Food & Drink", "Tools", "Communication"])
    ].dropna(subset=["user_rating"])
    box = px.box(
        focus,
        x="category",
        y="user_rating",
        color="category",
        points="outliers",
        labels={"category": "Category", "user_rating": label("user_rating")},
    )
    st.plotly_chart(
        finish_figure(box, "App ratings differ within each highlighted category"),
        width="stretch",
        theme=None,
    )
    st.caption(
        "This chart shows the spread of app ratings so one category average does not hide weaker "
        "apps. The stores use different category names, so the original names are kept."
    )


def render_engagement_competition(frame: pd.DataFrame) -> None:
    render_page_kicker("Question two · do people respond, and can a newcomer compete?")
    st.title("Reviews & Competition")
    st.caption(
        "Written reviews show one kind of user response. The number of competing apps and the "
        "largest app's share show how hard a category may be to enter."
    )
    android = frame.loc[
        frame["platform"].eq("Android")
        & frame["max_installs"].gt(0)
        & frame["review_count"].notna()
    ].copy()
    android["reviews_per_1k_installs"] = (
        android["review_count"] / android["max_installs"] * 1_000
    )
    cap = android["reviews_per_1k_installs"].quantile(0.99)
    engagement = android.loc[android["reviews_per_1k_installs"].le(cap)].copy()
    engagement = limit_categories(engagement, "category", 12)
    if len(engagement) > 5_000:
        engagement = engagement.sample(5_000, random_state=42)
    engagement_figure = px.scatter(
        engagement,
        x="max_installs",
        y="reviews_per_1k_installs",
        color="category",
        size="rating_count",
        hover_name="app_name",
        hover_data={"review_count": ":,", "user_rating": ":.1f"},
        log_x=True,
        size_max=28,
        opacity=0.62,
        labels={column: label(column) for column in engagement.columns},
    )
    st.plotly_chart(
        finish_figure(engagement_figure, "Android installs compared with written-review activity"),
        width="stretch",
        theme=None,
    )
    st.caption(
        "The install scale is compressed so apps of very different sizes can be compared. The "
        "most extreme 1% of review rates are hidden to keep the main pattern readable. Written "
        "reviews show only one kind of user response."
    )

    summary = category_market_summary(frame).dropna(
        subset=["total_rating_count", "weighted_user_rating"]
    )
    selected_names = set(summary.nlargest(22, "total_rating_count")["category"]) | {
        "Food & Drink",
        "Tools",
        "Communication",
    }
    competition = summary.loc[summary["category"].isin(selected_names)].copy()
    competition["chart_label"] = competition["category"].where(
        competition["category"].isin(["Food & Drink", "Tools", "Communication"]), ""
    )
    competition_figure = px.scatter(
        competition,
        x="app_count",
        y="total_rating_count",
        size="weighted_user_rating",
        color="platform_count",
        text="chart_label",
        hover_name="category",
        hover_data={"weighted_user_rating": ":.2f", "leading_app_share": ":.1f"},
        log_x=True,
        log_y=True,
        size_max=40,
        labels={
            "app_count": "Number of competing apps",
            "total_rating_count": "Total number of ratings",
            "weighted_user_rating": "Overall rating, with popular apps counting more",
            "platform_count": "App stores included",
            "leading_app_share": "Largest app's share (%)",
        },
    )
    competition_figure.update_traces(textposition="top center")
    st.plotly_chart(
        finish_figure(competition_figure, "Number of competing apps compared with popularity"),
        width="stretch",
        theme=None,
    )

    concentration = summary.loc[
        summary["category"].isin(selected_names)
    ].nlargest(15, "leading_app_share").sort_values("leading_app_share")
    concentration_figure = px.bar(
        concentration,
        x="leading_app_share",
        y="category",
        orientation="h",
        color="total_rating_count",
        hover_data={"leading_app": True, "total_rating_count": ":,"},
        labels={
            "leading_app_share": "Largest app's share of category ratings (%)",
            "category": "Category",
            "total_rating_count": "Total rating activity",
            "leading_app": "Leading app",
        },
    )
    st.plotly_chart(
        finish_figure(concentration_figure, "Categories where one app receives many of the ratings"),
        width="stretch",
        theme=None,
    )
    st.markdown(
        "**What this means:** A large market is not always easy to enter. Communication apps often "
        "depend on existing contacts, trust, and habits. The chart measures how much of each "
        "category's rating activity belongs to its largest app. It cannot measure how difficult "
        "it would be to persuade people to switch."
    )


def render_robustness_limitations(frame: pd.DataFrame) -> None:
    render_page_kicker("Question three · do the findings hold when the rules change?")
    st.title("Checks & Limitations")
    st.caption(
        "Try several cutoffs, compare the stores where the information matches, and look at how apps make money."
    )
    summary = category_rating_summary(frame)
    focus_names = ["Food & Drink", "Tools", "Communication"]
    focus = summary.loc[summary["category"].isin(focus_names)].copy()
    sensitivity_rows = []
    for rating_limit in [3.2, 3.3, 3.4, 3.5, 3.6]:
        for demand_limit in [5_000_000, 10_000_000, 20_000_000, 50_000_000]:
            matches = focus.loc[
                focus["weighted_user_rating"].le(rating_limit)
                & focus["total_rating_count"].ge(demand_limit),
                "category",
            ].tolist()
            sensitivity_rows.append(
                {
                    "rating_limit": f"≤ {rating_limit:.1f}",
                    "demand_limit": metric_text(demand_limit, 0),
                    "candidate_count": len(matches),
                    "candidates": ", ".join(matches) if matches else "None",
                }
            )
    sensitivity = pd.DataFrame(sensitivity_rows)
    sensitivity_figure = px.scatter(
        sensitivity,
        x="demand_limit",
        y="rating_limit",
        color="candidate_count",
        text="candidate_count",
        hover_data={"candidates": True, "candidate_count": False},
        color_continuous_scale="YlOrRd",
        labels={
            "demand_limit": "Fewest total ratings allowed",
            "rating_limit": "Highest adjusted rating allowed",
            "candidate_count": "Highlighted categories that qualify",
            "candidates": "Categories that qualify",
        },
    )
    sensitivity_figure.update_traces(marker=dict(symbol="square", size=30), textfont_size=12)
    st.plotly_chart(
        finish_figure(sensitivity_figure, "Does the shortlist change when the cutoffs change?"),
        width="stretch",
        theme=None,
    )
    st.caption(
        "Each square counts how many of Food & Drink, Tools, and Communication meet both cutoffs "
        "among apps rated from 2.0 up to, but not including, 4.0. Point to a square to see the "
        "names. A category that appears only under one set of rules is a less reliable choice."
    )

    st.divider()
    st.subheader("Do both app stores tell a similar story?")
    comparable = frame.loc[
        frame["category"].isin(focus_names)
    ].dropna(subset=["user_rating", "rating_count"]).copy()
    comparable = comparable.loc[comparable["rating_count"].gt(0)]
    comparable["weighted_total"] = comparable["user_rating"] * comparable["rating_count"]
    platform_summary = (
        comparable.groupby(["category", "platform"], as_index=False)
        .agg(
            total_rating_count=("rating_count", "sum"),
            weighted_total=("weighted_total", "sum"),
            rated_apps=("app_key", "size"),
        )
    )
    platform_summary["weighted_user_rating"] = (
        platform_summary["weighted_total"] / platform_summary["total_rating_count"]
    )
    platform_tab, activity_tab = st.tabs(["Overall user rating", "Number of ratings"])
    with platform_tab:
        platform_figure = px.bar(
            platform_summary,
            x="category",
            y="weighted_user_rating",
            color="platform",
            barmode="group",
            range_y=[0, 5],
            text_auto=".2f",
            labels={
                "category": "Category",
                "weighted_user_rating": "Overall rating, with popular apps counting more",
                "platform": "Platform",
            },
        )
        st.plotly_chart(
            finish_figure(platform_figure, "Overall user rating by app store"),
            width="stretch",
            theme=None,
        )
    with activity_tab:
        activity_figure = px.bar(
            platform_summary,
            x="category",
            y="total_rating_count",
            color="platform",
            barmode="group",
            log_y=True,
            labels={
                "category": "Category",
                "total_rating_count": "Total number of ratings",
                "platform": "Platform",
            },
        )
        st.plotly_chart(
            finish_figure(activity_figure, "Number of ratings by app store"),
            width="stretch",
            theme=None,
        )
    st.caption(
        "Ratings can be compared broadly across both stores. Android install and review numbers "
        "have no matching iPhone measure here, and iPhone app size has no matching Android field. "
        "The store information may also have been collected at different times."
    )

    st.divider()
    st.subheader("How these apps make money")
    model_rows = []
    for category, group in frame.loc[frame["category"].isin(focus_names)].groupby("category"):
        known = group.dropna(subset=["is_free"])
        if not known.empty:
            free_share = known["is_free"].mean() * 100
            model_rows.extend(
                [
                    {"category": category, "model": "Free", "share": free_share},
                    {"category": category, "model": "Paid", "share": 100 - free_share},
                ]
            )
    model_summary = pd.DataFrame(model_rows)
    model_figure = px.bar(
        model_summary,
        x="category",
        y="share",
        color="model",
        barmode="stack",
        text_auto=".0f",
        labels={"category": "Category", "share": "Share of apps (%)", "model": "Price model"},
    )
    st.plotly_chart(
        finish_figure(model_figure, "Share of free and paid apps"),
        width="stretch",
        theme=None,
    )

    feature_rows = []
    android_focus = frame.loc[
        frame["platform"].eq("Android") & frame["category"].isin(focus_names)
    ]
    for category, group in android_focus.groupby("category"):
        for column, name in [("contains_ads", "Shows ads"), ("in_app_purchases", "Offers in-app purchases")]:
            known = group.dropna(subset=[column])
            if not known.empty:
                feature_rows.append(
                    {"category": category, "feature": name, "share": known[column].mean() * 100}
                )
    feature_summary = pd.DataFrame(feature_rows)
    if not feature_summary.empty:
        feature_figure = px.bar(
            feature_summary,
            x="category",
            y="share",
            color="feature",
            barmode="group",
            text_auto=".0f",
            labels={"category": "Category", "share": "Share of Android apps (%)", "feature": "Feature"},
        )
        st.plotly_chart(
            finish_figure(feature_figure, "How Android apps may earn money"),
            width="stretch",
            theme=None,
        )

    st.warning(
        "**What these numbers cannot prove:** The number of ratings is only a rough sign of "
        "popularity. It does not tell us the number of users, revenue, repeat use, or whether people "
        "need a new app. Written reviews represent only people who chose to comment. The stores use "
        "different categories, the information may come from different dates, and these charts "
        "cannot show development cost, marketing cost, or why a pattern exists."
    )


def render_final_recommendation(frame: pd.DataFrame) -> None:
    render_page_kicker("Question four · what should be prioritized?")
    st.title("What to Do Next")
    st.caption("A practical next step based on the evidence above—not proof that one factor caused another.")
    visual_column, summary_column = st.columns([1.25, 1], gap="large")
    with visual_column:
        st.image(OPPORTUNITY_IMAGE, width="stretch")
    with summary_column:
        st.markdown(
            '<div class="insight-card"><p><strong>Prioritize a focused Food &amp; Drink or Tools '
            'product for the next round of testing.</strong> Both categories have many ratings and '
            'opportunities to improve specific, repeated tasks. Treat broad '
            'Communication products as a higher-barrier comparison case.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "The best opening is a **small, focused app that is useful right away**, not an attempt "
            "to replace an established service or ask people to move all their contacts."
        )

    lower_summary = category_rating_summary(frame).set_index("category")
    market_summary = category_market_summary(frame).set_index("category")
    cards = st.columns(3)
    for column, category in zip(cards, ["Food & Drink", "Tools", "Communication"]):
        if category in lower_summary.index:
            row = lower_summary.loc[category]
            column.markdown(
                '<div class="summary-card">'
                f'<span class="summary-label">{category}</span>'
                f'<strong>{row["weighted_user_rating"]:.2f}</strong>'
                '<p>Overall rating for apps rated 2.0 to under 4.0</p>'
                f'<p>{metric_text(row["total_rating_count"])} ratings in this group</p>'
                '</div>',
                unsafe_allow_html=True,
            )

    evidence, judgment = st.columns(2, gap="large")
    with evidence:
        st.markdown("#### What the data directly shows")
        st.markdown(
            "- Number of ratings and ratings adjusted for app popularity\n"
            "- How widely app ratings vary within each category\n"
            "- Android install and review activity\n"
            "- Number of competing apps, the largest app's share, and ways apps make money"
        )
    with judgment:
        st.markdown("#### What requires human judgment")
        st.markdown(
            "- Focused food and utility tasks may be easier to improve in a noticeable way\n"
            "- Communication carries stronger network, trust, and switching barriers\n"
            "- A small, focused first product is more realistic than challenging an established all-purpose app"
        )

    comparison_rows = []
    for category in ["Food & Drink", "Tools", "Communication"]:
        if category in lower_summary.index and category in market_summary.index:
            lower_row = lower_summary.loc[category]
            market_row = market_summary.loc[category]
            comparison_rows.append(
                {
                    "Category": category,
                    "All apps": f"{int(market_row['app_count']):,}",
                    "Lower-rated apps": f"{int(lower_row['app_count']):,}",
                    "Ratings for lower-rated apps": f"{int(lower_row['total_rating_count']):,}",
                    "Overall rating": f"{lower_row['weighted_user_rating']:.2f}",
                    "Largest app's share of all ratings": f"{market_row['leading_app_share']:.1f}%",
                    "Suggested next step": "Test first" if category != "Communication" else "Harder to enter",
                }
            )
    st.dataframe(pd.DataFrame(comparison_rows), width="stretch", hide_index=True)
    st.caption(
        "The lower-rating figures include only apps rated from 2.0 up to, but not including, 4.0. "
        "They show how much activity belongs to weaker-rated apps, not the average for the whole category."
    )

    st.subheader("What to check next")
    st.markdown(
        "1. Read and group written reviews to find problems that appear repeatedly.\n"
        "2. Compare apps that solve the same problem or a closely related one.\n"
        "3. Interview likely users to learn whether the problem happens often and matters enough.\n"
        "4. Test a simple early version and see whether people complete the task and return.\n"
        "5. Estimate marketing cost, repeat use, possible income, and development difficulty before investing."
    )
    st.info(
        "**Bottom line:** This analysis suggests what to investigate next. On its own, it does "
        "not prove that people need a new app or justify launching one."
    )


st.set_page_config(
    page_title="Mobile App Explorer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

data = load_data()

with st.sidebar:
    appearance = st.segmented_control(
        "Appearance",
        ["Light", "Dark"],
        default="Dark",
        width="stretch",
        key="appearance_mode",
    )
    st.markdown(
        '<div class="sidebar-brand"><strong>📱 Mobile Market Lab</strong>'
        '<span>App opportunity explorer</span></div>',
        unsafe_allow_html=True,
    )
    section = option_menu(
        menu_title=None,
        options=SECTIONS,
        icons=SECTION_ICONS,
        default_index=navigation_index(SECTIONS, "selected_section", "section"),
        styles=option_menu_styles(appearance),
        key=f"main_navigation_v3_{appearance.lower()}",
    )
    st.session_state["selected_section"] = section
    if query_value("section") != section:
        st.query_params["section"] = section

    filtered = data.copy()
    if section == "Explore the Data":
        st.divider()
        st.markdown("#### Choose app store")
        dataset_view = st.selectbox(
            "Choose the store data to explore",
            ["Both stores", "Apple App Store", "Google Play"],
            format_func=lambda value: {
                "Both stores": f"🌎 Both · {len(data):,}",
                "Apple App Store": f"🍎 Apple · {data['platform'].eq('iOS').sum():,}",
                "Google Play": f"🤖 Google Play · {data['platform'].eq('Android').sum():,}",
            }[value],
            help="Switch between the combined data and either individual app store.",
        )
        platform_for_view = {
            "Apple App Store": "iOS",
            "Google Play": "Android",
        }.get(dataset_view)
        if platform_for_view:
            filtered = filtered.loc[filtered["platform"].eq(platform_for_view)].copy()
        selected_total = len(filtered)

        with st.expander("Filters for all charts", expanded=True):
            currencies = sorted(filtered["currency"].dropna().astype(str).unique())
            selected_currencies = st.multiselect(
                "Currencies",
                currencies,
                default=currencies,
                help="Clear the selection to include every currency.",
            )
            if selected_currencies and set(selected_currencies) != set(currencies):
                filtered = filtered.loc[filtered["currency"].isin(selected_currencies)].copy()

            price_type = st.segmented_control(
                "Price type",
                ["All", "Free", "Paid"],
                default="All",
                width="stretch",
            )
            if price_type == "Free":
                filtered = filtered.loc[filtered["is_free"].eq(True)].copy()
            elif price_type == "Paid":
                filtered = filtered.loc[filtered["is_free"].eq(False)].copy()

            available_categories = sorted(filtered["category"].dropna().astype(str).unique())
            selected_categories = st.multiselect("Categories (blank = all)", available_categories)
            if selected_categories:
                filtered = filtered.loc[filtered["category"].isin(selected_categories)].copy()

            apply_rating_filter = st.toggle("Filter by rating")
            if apply_rating_filter and filtered["user_rating"].notna().any():
                rating_range = st.slider("Rating range", 0.0, 5.0, (0.0, 5.0), 0.1)
                filtered = filtered.loc[
                    filtered["user_rating"].between(*rating_range, inclusive="both")
                ].copy()

        with st.expander("Change how charts look"):
            palette_name = st.selectbox(
                "Chart colors",
                list(COLOR_PALETTES),
                index=0,
                key="chart_palette_name",
            )
            st.slider(
                "Chart height on screen",
                min_value=400,
                max_value=800,
                value=520,
                step=40,
                key="chart_height",
            )
            st.toggle("Show chart legends", value=True, key="show_chart_legend")

        px.defaults.color_discrete_sequence = COLOR_PALETTES[palette_name]

        st.caption(f"{len(filtered):,} of {selected_total:,} selected apps shown")

apply_appearance(appearance)

if section == "Home":
    st.markdown(
        f'<div class="hero-kicker">App market overview · {len(data):,} apps</div>',
        unsafe_allow_html=True,
    )
    st.title("Where could the next useful app win?")
    st.markdown(
        '<p class="hero-subtitle">A study of popularity, user ratings, written reviews, and competition '
        'across the Apple App Store and Google Play.</p>',
        unsafe_allow_html=True,
    )
    st.image(HERO_IMAGE, width="stretch")
    st.markdown(
        "This study looks for **app needs that current products may not serve well**. One useful "
        "clue is an Android app with many estimated installs but a lower user rating or few written "
        "reviews. The number of competing apps, prices, and age ratings add context. The site helps "
        "explore these clues and suggests what to research next; it cannot explain why a pattern exists."
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Prepared iPhone apps", f"{data['platform'].eq('iOS').sum():,}")
    col2.metric("Prepared Android apps", f"{data['platform'].eq('Android').sum():,}")
    col3.metric("Apps in combined list", f"{len(data):,}")

    st.subheader("What is included")
    st.markdown(
        "- A comparison of popularity, ratings, and written-review activity\n"
        "- Adjustable cutoffs for Android install estimates\n"
        "- Filters for app store, category, price, rating, and currency\n"
        "- Three ways to compare values with bar charts\n"
        "- Tools for building box, dot, pie, and ring charts\n"
        "- Samples and downloads of the prepared app lists\n"
        "- App images provided by Google Play"
    )
    icons = data.dropna(subset=["icon_url", "app_name"])[["icon_url", "app_name"]]
    if not icons.empty:
        with st.expander("Optional sample app images"):
            st.caption("Images are loaded from the Android store URLs and require internet access.")
            sample = icons.sample(min(8, len(icons)), random_state=7)
            st.image(sample["icon_url"].tolist(), caption=sample["app_name"].tolist(), width=72)
    st.info(
        "Use the navigation pane to review the data preparation, explore the charts, then follow "
        "the next four sections from popularity through suggested next steps."
    )
    st.stop()

if section == "About the Study":
    render_page_kicker("About the study · what the numbers can tell us")
    st.title("About the Study")
    st.markdown(
        '<p class="hero-subtitle">Before looking for an app idea, this study establishes what the '
        'available signals can reveal, how the two stores differ, and why popularity alone does not '
        'equal opportunity.</p>',
        unsafe_allow_html=True,
    )

    st.image(ECOSYSTEM_IMAGE, width="stretch")
    st.caption(
        "The two stores organize their information differently. The combined list connects only "
        "details that truly mean the same thing."
    )

    st.subheader("The question behind the study")
    question_column, context_column = st.columns([1.05, 1], gap="large")
    with question_column:
        st.markdown(
            '<div class="insight-card"><p><strong>Which needs may not be served well by current '
            'apps?</strong><br>A useful opening may exist where many people use these apps, '
            'yet current products earn weaker ratings or fewer written reviews than that popularity '
            'would lead us to expect.</p></div>',
            unsafe_allow_html=True,
        )
    with context_column:
        st.markdown(
            "This is a search for **problems that current apps may not solve well**, not simply the "
            "biggest category. Large markets can be attractive, but they can also have powerful "
            "competitors, products that become more useful when friends join, and high marketing costs. Smaller, focused tasks "
            "may offer a more realistic entry point when a new app can solve one recurring problem "
            "noticeably better."
        )

    app_total = len(data)
    rated_total = int(data["user_rating"].notna().sum())
    category_total = int(data["category"].nunique(dropna=True))
    free_share = data["is_free"].mean() * 100
    scope_columns = st.columns(4)
    scope_columns[0].metric("Apps studied", f"{app_total:,}")
    scope_columns[1].metric("Categories", f"{category_total:,}")
    scope_columns[2].metric("Apps with ratings", f"{rated_total:,}")
    scope_columns[3].metric("Apps that are free", f"{free_share:.1f}%")

    st.subheader("Four clues to a possible opening")
    st.markdown(
        "No one number proves that an opening exists. The study considers four clues together "
        "so one impressive number does not control the conclusion."
    )
    st.markdown(
        '<div class="framework-grid">'
        '<div class="framework-card"><span class="framework-icon">↗️</span>'
        '<strong>Popularity</strong><span>The number of ratings and estimated Android installs show whether '
        'people already use this kind of product.</span></div>'
        '<div class="framework-card"><span class="framework-icon">★</span>'
        '<strong>Satisfaction</strong><span>User ratings help surface areas where the existing '
        'experience may be falling short.</span></div>'
        '<div class="framework-card"><span class="framework-icon">◌</span>'
        '<strong>User response</strong><span>Written reviews compared with installs show one way '
        'Android users respond to an app.</span></div>'
        '<div class="framework-card"><span class="framework-icon">◇</span>'
        '<strong>Competition</strong><span>The number of apps and the largest app\'s share help show '
        'whether a category is crowded.</span></div></div>',
        unsafe_allow_html=True,
    )

    lens_visual, lens_copy = st.columns([1.25, 1], gap="large")
    with lens_visual:
        st.image(MARKET_GAP_IMAGE, width="stretch")
        st.caption("A possible opening needs several clues to point in the same direction.")
    with lens_copy:
        st.markdown("### How to recognize a possible opening")
        st.markdown(
            "An idea becomes more interesting when several conditions overlap:\n\n"
            "1. **People already use it.** The category or app attracts meaningful installs or ratings.\n"
            "2. **Current apps leave room to improve.** Ratings are weaker than the activity level might suggest.\n"
            "3. **The problem can be narrowed.** A new app can serve a specific group or task.\n"
            "4. **People can try it easily.** They do not have to move their contacts or leave a service they already rely on."
        )
        st.info(
            "These clues identify ideas worth checking. Interviews, competitor research, testing an "
            "early version, and estimating marketing costs are still needed before building."
        )

    st.subheader("Why every Apple number does not have an Android match")
    st.markdown(
        "The stores organize similar app information in different ways and publish different details. "
        "The combined table matches shared information and leaves a space blank when the other store "
        "has no true equivalent. This avoids comparisons that look useful but are not fair."
    )
    ios_context, android_context = st.columns(2, gap="large")
    with ios_context:
        st.markdown("#### Apple App Store")
        st.markdown(
            "The iPhone list includes app size, how many languages and devices are supported, price, "
            "ratings, categories, and developer information. It does **not** provide install or "
            "matching written-review totals in this collection."
        )
    with android_context:
        st.markdown("#### Google Play")
        st.markdown(
            "The Android list includes install estimates, written-review totals, whether an app shows "
            "ads or offers in-app purchases, ratings, categories, and developer information. Install values "
            "are broad estimates rather than exact downloads."
        )

    with st.expander("Guide to the information in the combined app list"):
        st.caption("This guide explains what each piece of information means in the study.")
        definitions = pd.DataFrame(
            [
                ("App store", "Whether the app comes from Apple or Google Play."),
                ("Unique app key", "A unique label made from the app store and store ID."),
                ("Category", "The app's main store category or genre."),
                ("User rating", "The store rating from 0 to 5; unknown ratings stay blank."),
                ("Number of ratings", "How many user ratings the source recorded."),
                ("Written reviews", "Android written-review total, used as one sign of user response."),
                ("Price and currency", "The listed price and money type; compare prices using the same currency."),
                ("Install estimates", "Android-only lower and upper install estimates."),
                ("App size", "iPhone-only app size in megabytes."),
            ],
            columns=["Information", "Meaning"],
        )
        st.dataframe(definitions, width="stretch", hide_index=True)

    st.subheader("Important boundaries")
    st.warning(
        "This information is a saved picture of the market, not a live update. Install estimates and written-review totals are "
        "Android-only, the stores use different category names, prices must use the same currency "
        "for a fair comparison, and unknown values stay blank. The analysis can prioritize "
        "questions, but it cannot measure how hard switching would be, development effort, profit, or "
        "future demand directly."
    )
    st.markdown(
        "The next sections document the cleaning process and make the evidence explorable. The "
        "four analysis sections then move from popularity and ratings through competition, "
        "checks and limits, and a practical recommendation."
    )
    st.caption(
        "Case-study structure inspired by Jeson Wu's Streamlit project."
    )
    st.stop()

if section == "How Data Was Prepared":
    render_page_kicker("Preparing the data · clear and trustworthy")
    st.title("How the Data Was Prepared")
    st.markdown(
        "The original files were kept unchanged. The prepared copies use consistent names and "
        "formats, check that app IDs and number ranges make sense, and leave unknown values blank "
        "instead of guessing."
    )
    report = load_quality_report()
    check_frame = pd.DataFrame(
        {
            "Data check": [QUALITY_CHECK_NAMES.get(name, name.replace("_", " ").title()) for name in report["validation"]],
            "Result": ["Passed" if value else "Needs attention" for value in report["validation"].values()],
        }
    )
    st.dataframe(check_frame, width="stretch", hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader("iOS")
        st.metric("Apps kept", f"{report['ios']['cleaned_rows']:,}")
        for change in report["ios"]["changes"]:
            st.write("•", CLEANING_CHANGE_NAMES.get(change, change))
    with right:
        st.subheader("Android")
        st.metric("Apps kept", f"{report['android']['cleaned_rows']:,}")
        st.write("Unknown ratings left blank:", f"{report['android']['missing_ratings_retained']:,}")
        for change in report["android"]["changes"]:
            st.write("•", CLEANING_CHANGE_NAMES.get(change, change))

    ios_clean, android_clean = load_cleaned_sources()
    ios_tab, android_tab = st.tabs(["Prepared iPhone data sample", "Prepared Android data sample"])
    with ios_tab:
        st.dataframe(format_table_for_display(ios_clean.head(100)), width="stretch")
        st.download_button(
            "Download prepared iPhone data (CSV file)",
            IOS_FILE.read_bytes(),
            file_name=IOS_FILE.name,
            mime="text/csv",
        )
    with android_tab:
        st.dataframe(format_table_for_display(android_clean.head(100)), width="stretch")
        st.download_button(
            "Download prepared Android data (CSV file)",
            ANDROID_FILE.read_bytes(),
            file_name=ANDROID_FILE.name,
            mime="text/csv",
        )
    with st.expander("Detailed data-check report (for technical review)"):
        st.json(report)
    st.stop()

if section == "View the Data":
    render_page_kicker("Prepared app lists · view or download")
    st.title("View the Prepared Data")
    st.markdown(
        "The prepared Apple App Store and Google Play lists stay separate so details unique to "
        "each store remain visible. Search the tables, choose columns, or download the full files."
    )
    ios_clean, android_clean = load_cleaned_sources()
    ios_tab, android_tab = st.tabs(
        [
            f"🍎 Apple App Store · {len(ios_clean):,} apps",
            f"🤖 Google Play · {len(android_clean):,} apps",
        ]
    )
    with ios_tab:
        render_cleaned_dataset(ios_clean, IOS_FILE, "Apple App Store")
    with android_tab:
        render_cleaned_dataset(android_clean, ANDROID_FILE, "Google Play")
    st.stop()

if section == "Popularity & Ratings":
    render_demand_satisfaction(data)
    st.stop()

if section == "Reviews & Competition":
    render_engagement_competition(data)
    st.stop()

if section == "Checks & Limitations":
    render_robustness_limitations(data)
    st.stop()

if section == "What to Do Next":
    render_final_recommendation(data)
    st.stop()

page = option_menu(
    menu_title=None,
    options=EXPLORATION_PAGES,
    icons=EXPLORATION_ICONS,
    default_index=navigation_index(
        EXPLORATION_PAGES,
        "selected_exploration_page",
        "page",
    ),
    orientation="horizontal",
    styles=option_menu_styles(appearance, horizontal=True),
    key=f"exploration_navigation_v2_{appearance.lower()}",
)
st.session_state["selected_exploration_page"] = page
if query_value("page") != page:
    st.query_params["page"] = page

if filtered.empty:
    st.error("No rows match the current filters. Change a sidebar filter to continue.")
    st.stop()

numeric = numeric_columns(filtered)
categorical = categorical_columns(filtered)

render_page_kicker("Interactive lab · follow the signals")
st.title("Explore the Data")
st.caption(
    "Compare popularity, user ratings, written reviews, and competition • "
    "then use the next four sections to understand the findings and suggested next steps"
)

if page == "Overview":
    app_count = len(filtered)
    median_rating = filtered["user_rating"].median()
    free_share = filtered["is_free"].mean() * 100
    category_count = filtered["category"].nunique(dropna=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Apps", f"{app_count:,}")
    col2.metric("Typical rating (middle)", metric_text(median_rating, 2))
    col3.metric("Free apps", f"{free_share:.1f}%")
    col4.metric("Categories", f"{category_count:,}")

    st.subheader("What's in the selected data")
    chart_col1, chart_col2 = st.columns(2)
    platform_counts = filtered["platform"].value_counts().rename_axis("platform").reset_index(name="apps")
    platform_figure = px.pie(
        platform_counts,
        names="platform",
        values="apps",
        hole=0.45,
        color="platform",
    )
    chart_col1.plotly_chart(
        finish_figure(platform_figure, "Apps by app store"),
        width="stretch",
        theme=None,
    )

    category_counts = (
        filtered["category"].fillna("(Missing)").value_counts().head(12).sort_values()
    )
    category_figure = px.bar(
        x=category_counts.values,
        y=category_counts.index,
        orientation="h",
        labels={"x": "App count", "y": "Category"},
    )
    chart_col2.plotly_chart(
        finish_figure(category_figure, "12 categories with the most apps"),
        width="stretch",
        theme=None,
    )

    st.subheader("Look for possible openings")
    st.caption(
        "Look for Android apps with many estimated installs but lower user ratings or little "
        "written-review activity. You can change the cutoffs; the results are leads to research, not conclusions."
    )
    gap_data = filtered.loc[
        filtered["platform"].eq("Android")
        & filtered["max_installs"].gt(0)
        & filtered["user_rating"].notna()
    ].copy()
    if gap_data.empty:
        st.info(
            "This view needs Android install estimates. Choose Google Play or Both stores in the sidebar."
        )
    else:
        gap_data["review_count"] = gap_data["review_count"].fillna(0)
        gap_data["reviews_per_1k_installs"] = (
            gap_data["review_count"] / gap_data["max_installs"] * 1_000
        )
        controls, plot = st.columns([1, 3], gap="large")
        with controls:
            st.markdown("#### Choices")
            gap_signal = st.segmented_control(
            "Possible sign of an opening",
                ["Lower rating", "Low review activity"],
                default="Lower rating",
                width="stretch",
            )
            install_floor = st.select_slider(
                "Minimum estimated installs",
                options=[10_000, 100_000, 1_000_000, 10_000_000, 100_000_000],
                value=1_000_000,
                format_func=lambda value: f"{value:,}+",
            )
            if gap_signal == "Lower rating":
                signal_ceiling = st.slider("Maximum user rating", 1.0, 5.0, 4.0, 0.1)
                signal_column = "user_rating"
            else:
                signal_ceiling = st.slider(
                    "Maximum reviews per 1,000 installs", 0.0, 2.0, 0.1, 0.05
                )
                signal_column = "reviews_per_1k_installs"

        candidates = gap_data.loc[
            gap_data["max_installs"].ge(install_floor)
            & gap_data[signal_column].le(signal_ceiling)
        ].copy()
        plot_data = limit_categories(gap_data, "category", 12)
        if len(plot_data) > 5_000:
            plot_data = plot_data.sample(5_000, random_state=42)
        gap_figure = px.scatter(
            plot_data,
            x="max_installs",
            y=signal_column,
            color="category",
            size="review_count",
            hover_name="app_name",
            hover_data=["developer", "user_rating", "review_count", "max_installs"],
            log_x=True,
            size_max=26,
            opacity=0.68,
            labels={column: label(column) for column in plot_data.columns},
        )
        gap_figure.add_vline(x=install_floor, line_dash="dash", line_color="#f45b5b")
        gap_figure.add_hline(y=signal_ceiling, line_dash="dash", line_color="#f45b5b")
        with plot:
            st.plotly_chart(
                finish_figure(gap_figure, f"Estimated installs compared with {label(signal_column).lower()}"),
                width="stretch",
                theme=None,
            )

        st.markdown(f"#### Apps worth a closer look · {len(candidates):,} matches")
        st.caption(
            "These apps meet your current choices. They are starting points for research, not proven opportunities."
        )
        candidate_columns = [
            "app_name",
            "category",
            "developer",
            "max_installs",
            "user_rating",
            "review_count",
            "reviews_per_1k_installs",
        ]
        st.dataframe(
            format_table_for_display(
                candidates.sort_values("max_installs", ascending=False)[candidate_columns]
                .head(100)
            ),
            width="stretch",
            hide_index=True,
        )

    icons = filtered.dropna(subset=["icon_url", "app_name"])[["icon_url", "app_name"]]
    if not icons.empty:
        with st.expander("Optional visual feature: sample Android app icons"):
            st.caption("Images are loaded from the Android store URLs and require internet access.")
            sample = icons.sample(min(8, len(icons)), random_state=42)
            st.image(
                sample["icon_url"].tolist(),
                caption=sample["app_name"].tolist(),
                width=72,
            )

elif page == "View App List":
    st.subheader("Apps matching your filters")
    st.caption(
        "Look at individual apps behind a possible opening. This app list has Android install estimates but no matching iPhone measure."
    )
    default_columns = [
        "platform",
        "app_name",
        "category",
        "max_installs",
        "user_rating",
        "rating_count",
        "review_count",
        "price",
        "currency",
        "is_free",
        "content_rating_normalized",
    ]
    shown_columns = st.multiselect(
        "Information to show",
        filtered.columns.tolist(),
        default=[column for column in default_columns if column in filtered.columns],
        format_func=friendly_option,
    )
    sort_column = st.selectbox(
        "Sort by",
        ["(original order)"] + shown_columns,
        format_func=friendly_option,
    )
    ascending = st.toggle("Sort from smallest to largest or A to Z", value=False)
    display = filtered[shown_columns].copy() if shown_columns else filtered.copy()
    if sort_column != "(original order)":
        display = display.sort_values(sort_column, ascending=ascending, na_position="last")
    friendly_display = format_table_for_display(display)
    st.dataframe(friendly_display, width="stretch", height=520)
    st.download_button(
        "Download these apps (CSV file)",
        display.to_csv(index=False).encode("utf-8"),
        file_name="filtered_mobile_apps.csv",
        mime="text/csv",
    )

elif page == "Compare with Bars":
    st.subheader("Compare groups and number ranges")
    st.caption(
        "Use bars to compare ratings, installs, written reviews, and app groups."
    )
    controls, plot = st.columns([1, 3], gap="large")
    controls.markdown("#### Choices")
    histogram_type = controls.selectbox(
        "What do you want to compare?",
        [
            "Two number-based fields, split into groups",
            "Two groups by app count or percentage",
            "A combined number for two groups",
        ],
    )
    bins = controls.slider("Number of bars", 5, 80, 30)
    log_y = controls.toggle(
        "Compress very large values",
        value=False,
        help="Makes small and large values easier to see together. Bars with a value of zero will not appear.",
        key="histogram_log_y",
    )

    if histogram_type == "Two number-based fields, split into groups":
        num1 = controls.selectbox(
            "First number to compare",
            numeric,
            index=preferred_index(numeric, "user_rating", "rating_count"),
            format_func=friendly_option,
        )
        num2_default = preferred_index(numeric, "max_installs", "rating_count", "price")
        num2 = controls.selectbox(
            "Second number to compare",
            numeric,
            index=num2_default,
            format_func=friendly_option,
        )
        group = controls.selectbox(
            "Split the bars by",
            categorical,
            index=preferred_index(categorical, "category", "platform"),
            format_func=friendly_option,
        )
        y_mode = controls.radio("Show as", ["Counts", "Percent"], horizontal=True)
        comparison = controls.selectbox(
            "How groups should appear",
            ["Side by side", "Overlay", "Stacked"],
            help="Side by side places each colored category next to the others within every bin.",
            key="numeric_histogram_comparison",
        )
        marginal = controls.selectbox(
            "Extra summary beside the bars",
            ["None", "Box", "Violin", "Rug"],
            format_func=lambda value: {"None": "None", "Box": "Range box", "Violin": "Smooth shape", "Rug": "Individual marks"}[value],
        )
        bar_opacity = controls.slider("Bar transparency", 0.3, 1.0, 0.85, 0.05)
        top_n = controls.slider("Most groups to show", 2, 15, 6)
        histnorm = "percent" if y_mode == "Percent" else None
        barmode = {
            "Side by side": "group",
            "Overlay": "overlay",
            "Stacked": "stack",
        }[comparison]
        for column in [num1, num2]:
            chart_data = limit_categories(filtered, group, top_n).dropna(subset=[column])
            figure = px.histogram(
                chart_data,
                x=column,
                color=group,
                nbins=bins,
                histnorm=histnorm,
                barmode=barmode,
                marginal=None if marginal == "None" else marginal.lower(),
                opacity=bar_opacity,
                log_y=log_y,
                labels={column: label(column), group: label(group)},
            )
            figure.update_yaxes(title="Percent" if histnorm else "App count")
            plot.plotly_chart(
                finish_figure(figure, f"{label(column)} by {label(group)}"),
                width="stretch",
                theme=None,
            )

    elif histogram_type == "Two groups by app count or percentage":
        cat1 = controls.selectbox(
            "Main way to group apps",
            categorical,
            index=preferred_index(categorical, "category", "platform"),
            format_func=friendly_option,
        )
        cat2_default = preferred_index(
            categorical, "platform", "content_rating_normalized", "is_free"
        )
        cat2 = controls.selectbox(
            "Split each group by",
            categorical,
            index=cat2_default,
            format_func=friendly_option,
        )
        y_mode = controls.radio("Show as", ["Counts", "Percent"], horizontal=True)
        comparison = controls.selectbox(
            "How groups should appear",
            ["Side by side", "Stacked"],
            help="Side by side makes colored categories easier to compare directly.",
            key="categorical_histogram_comparison",
        )
        top_n = controls.slider("Most groups to show", 2, 20, 10)
        chart_data = limit_categories(filtered, cat1, top_n)
        chart_data = limit_categories(chart_data, cat2, top_n)
        figure = px.histogram(
            chart_data,
            x=cat1,
            color=cat2,
            barmode="group" if comparison == "Side by side" else "stack",
            barnorm="percent" if y_mode == "Percent" else None,
            log_y=log_y,
            labels={cat1: label(cat1), cat2: label(cat2)},
        )
        figure.update_yaxes(title="Percent within each main group" if y_mode == "Percent" else "App count")
        plot.plotly_chart(
            finish_figure(figure, f"{label(cat1)} by {label(cat2)}"),
            width="stretch",
            theme=None,
        )

    else:
        cat1 = controls.selectbox(
            "Main way to group apps",
            categorical,
            index=preferred_index(categorical, "category", "platform"),
            format_func=friendly_option,
        )
        cat2_default = preferred_index(
            categorical, "platform", "content_rating_normalized", "is_free"
        )
        cat2 = controls.selectbox(
            "Split each group by",
            categorical,
            index=cat2_default,
            format_func=friendly_option,
        )
        number = controls.selectbox(
            "Number to combine",
            numeric,
            index=preferred_index(numeric, "max_installs", "user_rating", "rating_count"),
            format_func=friendly_option,
        )
        aggregation = controls.selectbox(
            "How to combine the numbers",
            ["Mean", "Median", "Sum", "Count of nonmissing values"],
            format_func=lambda value: {
                "Mean": "Average",
                "Median": "Middle value",
                "Sum": "Total",
                "Count of nonmissing values": "Count of known values",
            }[value],
        )
        aggregation_label = {
            "Mean": "Average",
            "Median": "Middle value",
            "Sum": "Total",
            "Count of nonmissing values": "Count of known values",
        }[aggregation]
        comparison = controls.selectbox(
            "How groups should appear",
            ["Side by side", "Stacked"],
            key="summary_histogram_comparison",
        )
        top_n = controls.slider("Most groups to show", 2, 20, 10)
        chart_data = limit_categories(filtered, cat1, top_n)
        chart_data = limit_categories(chart_data, cat2, top_n).dropna(subset=[number])
        group_columns = [cat1] if cat1 == cat2 else [cat1, cat2]
        if aggregation == "Count of nonmissing values":
            summary = chart_data.groupby(group_columns, dropna=False)[number].count().reset_index(name="value")
        else:
            method = aggregation.lower()
            summary = chart_data.groupby(group_columns, dropna=False)[number].agg(method).reset_index(name="value")
        figure = px.bar(
            summary,
            x=cat1,
            y="value",
            color=cat2 if cat1 != cat2 else None,
            barmode="group" if comparison == "Side by side" else "stack",
            log_y=log_y,
            labels={cat1: label(cat1), cat2: label(cat2), "value": f"{aggregation_label}: {label(number)}"},
        )
        plot.plotly_chart(
            finish_figure(
                figure,
                f"{aggregation_label} of {label(number)} by {label(cat1)} and {label(cat2)}",
            ),
            width="stretch",
            theme=None,
        )

elif page == "Compare Ranges":
    st.subheader("Compare the range of values")
    st.caption("See the middle, usual range, and unusual values for each group of apps.")
    controls, plot = st.columns([1, 3], gap="large")
    controls.markdown("#### Choices")
    number = controls.selectbox(
        "Number to compare",
        numeric,
        index=preferred_index(numeric, "user_rating", "max_installs", "rating_count"),
        format_func=friendly_option,
    )
    group = controls.selectbox(
        "Group apps by",
        categorical,
        index=preferred_index(categorical, "category", "platform"),
        format_func=friendly_option,
    )
    top_n = controls.slider("Most groups to show", 2, 25, 10)
    point_mode = controls.selectbox(
        "Show individual apps",
        ["Outliers", "All", "None"],
        format_func=lambda value: {"Outliers": "Only unusual values", "All": "All apps", "None": "Do not show"}[value],
    )
    orientation = controls.radio("Chart direction", ["Vertical", "Horizontal"], horizontal=True)
    notched = controls.toggle(
        "Highlight uncertainty around the middle",
        value=False,
        help="Adds a narrow section around the middle value to help compare groups.",
    )
    chart_data = limit_categories(filtered, group, top_n).dropna(subset=[number])
    points = {"Outliers": "outliers", "All": "all", "None": False}[point_mode]
    figure = px.box(
        chart_data,
        x=group if orientation == "Vertical" else number,
        y=number if orientation == "Vertical" else group,
        color=group,
        points=points,
        notched=notched,
        labels={group: label(group), number: label(number)},
    )
    plot.plotly_chart(
        finish_figure(figure, f"Range of {label(number)} by {label(group)}"),
        width="stretch",
        theme=None,
    )

elif page == "Compare Two Measures":
    st.subheader("Compare two measures")
    st.caption("Each dot is an app. Comparing popularity with user rating is a useful place to start.")
    controls, plot = st.columns([1, 3], gap="large")
    controls.markdown("#### Choices")
    x_column = controls.selectbox(
        "Measure across the bottom",
        numeric,
        index=preferred_index(numeric, "max_installs", "rating_count", "review_count"),
        format_func=friendly_option,
    )
    y_default = preferred_index(numeric, "user_rating", "review_count", "rating_count")
    y_column = controls.selectbox(
        "Measure up the side",
        numeric,
        index=y_default,
        format_func=friendly_option,
    )
    color_options = ["(None)"] + categorical
    color_choice = controls.selectbox(
        "Color dots by",
        color_options,
        index=preferred_index(color_options, "category", "platform"),
        format_func=friendly_option,
    )
    size_options = ["(None)"] + numeric
    size_choice = controls.selectbox(
        "Dot size represents",
        size_options,
        index=preferred_index(size_options, "review_count", "rating_count"),
        format_func=friendly_option,
    )
    max_points = controls.slider("Most dots to show", 500, 10_000, 5_000, 500)
    point_opacity = controls.slider("Dot transparency", 0.2, 1.0, 0.7, 0.05)
    bubble_size = controls.slider("Largest dot size", 10, 50, 28, 2)
    log_x = controls.toggle(
        "Compress large values across the bottom",
        value=x_column in {"min_installs", "max_installs", "rating_count", "review_count"},
    )
    log_y = controls.toggle("Compress large values up the side")

    required = [x_column, y_column]
    if size_choice != "(None)":
        required.append(size_choice)
    chart_data = filtered.dropna(subset=required).copy()
    if log_x:
        chart_data = chart_data.loc[chart_data[x_column].gt(0)]
    if log_y:
        chart_data = chart_data.loc[chart_data[y_column].gt(0)]
    if color_choice != "(None)":
        chart_data = limit_categories(chart_data, color_choice, 12)
    if len(chart_data) > max_points:
        chart_data = chart_data.sample(max_points, random_state=42)
    figure = px.scatter(
        chart_data,
        x=x_column,
        y=y_column,
        color=None if color_choice == "(None)" else color_choice,
        size=None if size_choice == "(None)" else size_choice,
        hover_name="app_name",
        hover_data=["platform", "category", "currency"],
        log_x=log_x,
        log_y=log_y,
        size_max=bubble_size,
        opacity=point_opacity,
        labels={column: label(column) for column in chart_data.columns},
    )
    plot.plotly_chart(
        finish_figure(figure, f"{label(y_column)} compared with {label(x_column)}"),
        width="stretch",
        theme=None,
    )

elif page == "Parts of a Whole":
    st.subheader("See parts of a whole")
    st.caption("See how apps or popularity are divided among groups.")
    controls, plot = st.columns([1, 3], gap="large")
    controls.markdown("#### Choices")
    category = controls.selectbox(
        "Group apps by",
        categorical,
        index=preferred_index(categorical, "category", "platform"),
        format_func=friendly_option,
    )
    measure_choice = controls.selectbox("Slice size represents", ["App count"] + [f"Total {label(column)}" for column in numeric])
    top_n = controls.slider("Number of slices", 3, 20, 10)
    hole_size = controls.slider("Empty center size", 0.0, 0.8, 0.35, 0.05)
    chart_data = filtered.copy()
    chart_data[category] = chart_data[category].astype("string").fillna("(Missing)")
    if measure_choice == "App count":
        summary = chart_data.groupby(category, dropna=False).size().reset_index(name="value")
    else:
        selected_number = next(column for column in numeric if measure_choice == f"Total {label(column)}")
        summary = chart_data.groupby(category, dropna=False)[selected_number].sum(min_count=1).reset_index(name="value")
        summary = summary.dropna(subset=["value"])
    summary = summary.sort_values("value", ascending=False)
    summary = summary.head(top_n).copy()
    figure = px.pie(
        summary,
        names=category,
        values="value",
        hole=hole_size,
        labels={category: label(category), "value": measure_choice},
    )
    plot.plotly_chart(
        finish_figure(figure, f"{measure_choice} by {label(category)}"),
        width="stretch",
        theme=None,
    )

elif page == "Explore by Rings":
    st.subheader("Explore groups inside other groups")
    st.caption("Move from broad groups in the center to more specific groups in the outer rings.")
    controls, plot = st.columns([1, 3], gap="large")
    controls.markdown("#### Choices")
    level1 = controls.selectbox(
        "Center group",
        categorical,
        index=preferred_index(categorical, "category", "platform"),
        format_func=friendly_option,
    )
    level2_options = [column for column in categorical if column != level1]
    level2 = controls.selectbox(
        "Middle ring",
        level2_options,
        index=preferred_index(
            level2_options, "content_rating_normalized", "platform", "is_free"
        ),
        format_func=friendly_option,
    )
    level3_options = ["(None)"] + [
        column for column in categorical if column not in {level1, level2}
    ]
    level3 = controls.selectbox("Outer ring", level3_options, format_func=friendly_option)
    value_choice = controls.selectbox("Section size represents", ["App count"] + [f"Total {label(column)}" for column in numeric])
    path = [level1, level2] + ([] if level3 == "(None)" else [level3])
    max_depth = controls.slider("Number of rings to show", 1, len(path), len(path))
    chart_data = filtered.copy()
    for column in path:
        chart_data[column] = chart_data[column].astype("string").fillna("(Missing)")
    if value_choice == "App count":
        summary = chart_data.groupby(path, dropna=False).size().reset_index(name="value")
    else:
        selected_number = next(column for column in numeric if value_choice == f"Total {label(column)}")
        summary = chart_data.groupby(path, dropna=False)[selected_number].sum(min_count=1).reset_index(name="value")
        summary = summary.dropna(subset=["value"])
    figure = px.sunburst(
        summary,
        path=path,
        values="value",
        color=level1,
        maxdepth=max_depth,
        labels={column: label(column) for column in path},
    )
    plot.plotly_chart(
        finish_figure(figure, f"{value_choice}: " + " → ".join(label(column) for column in path)),
        width="stretch",
        theme=None,
    )

else:
    st.subheader("How the data was checked")
    report = load_quality_report()
    ios_report = report["ios"]
    android_report = report["android"]

    left, right = st.columns(2)
    with left:
        st.markdown("### iPhone data preparation")
        st.metric("Apps kept", f"{ios_report['cleaned_rows']:,}")
        st.write("Repeated app IDs found:", ios_report["duplicate_id_rows_detected"])
        st.write("Blank cells after preparation:", ios_report["missing_cells_after_cleaning"])
        for change in ios_report["changes"]:
            st.write("•", CLEANING_CHANGE_NAMES.get(change, change))
    with right:
        st.markdown("### Android data preparation")
        st.metric("Apps kept", f"{android_report['cleaned_rows']:,}")
        st.write("Repeated app IDs found:", android_report["duplicate_id_rows_detected"])
        st.write("Unknown ratings left blank:", f"{android_report['missing_ratings_retained']:,}")
        st.write("Empty columns removed:", len(android_report["all_null_columns_removed"]))
        for change in android_report["changes"]:
            st.write("•", CLEANING_CHANGE_NAMES.get(change, change))

    st.markdown("### Data checks")
    validation = pd.DataFrame(
        {
            "Check": [QUALITY_CHECK_NAMES.get(name, name.replace("_", " ").title()) for name in report["validation"]],
            "Result": ["Passed" if value else "Needs attention" for value in report["validation"].values()],
        }
    )
    st.dataframe(validation, width="stretch", hide_index=True)

    with st.expander("Detailed data-check report (for technical review)"):
        st.json(report)

    st.info(
        "This page explains how the data was prepared and checked. The four analysis sections "
        "explain what the patterns may mean, what the limits are, and what to investigate next."
    )
