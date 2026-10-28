from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DAILY_PATH = BASE_DIR / "main_data_daily.csv"
HOURLY_PATH = BASE_DIR / "main_data.csv"

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.markdown(
    """
    <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
        h1, h2, h3 {color: #1D3557;}
        [data-testid="stMetricValue"] {font-size: 1.6rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

COLORS = {
    "primary": "#2A6F97",
    "secondary": "#61A5C2",
    "accent": "#F4A261",
    "danger": "#C44536",
    "muted": "#8D99AE",
    "dark": "#1D3557",
}
DAY_ORDER = ["Hari Kerja", "Akhir Pekan/Libur"]
SEASON_ORDER = ["Spring (Jan-Mar)", "Summer (Apr-Jun)", "Fall (Jul-Sep)", "Winter (Oct-Dec)"]
WEATHER_ORDER = ["Cerah/Berawan", "Berkabut/Mendung", "Hujan/Salju Ringan"]
WEEKDAY_ORDER = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
SEG_ORDER = ["Low", "Medium", "High", "Very High"]
TIME_BLOCK_ORDER = ["Malam (00-05)", "Pagi (06-09)", "Siang (10-15)", "Sore (16-19)", "Malam (20-23)"]

DAY_COLORS = {"Hari Kerja": COLORS["primary"], "Akhir Pekan/Libur": COLORS["accent"]}
WEATHER_COLORS = {
    "Cerah/Berawan": COLORS["primary"],
    "Berkabut/Mendung": COLORS["secondary"],
    "Hujan/Salju Ringan": COLORS["danger"],
    "Hujan/Salju Lebat": COLORS["dark"],
}
SEASON_COLORS = {
    "Spring (Jan-Mar)": "#8AB17D",
    "Summer (Apr-Jun)": "#E9C46A",
    "Fall (Jul-Sep)": "#F4A261",
    "Winter (Oct-Dec)": "#457B9D",
}
SEG_COLORS = {
    "Low": COLORS["muted"],
    "Medium": COLORS["secondary"],
    "High": COLORS["primary"],
    "Very High": COLORS["danger"],
}


@st.cache_data(show_spinner=False)
def load_data():
    if not DAILY_PATH.exists() or not HOURLY_PATH.exists():
        raise FileNotFoundError("File main_data.csv / main_data_daily.csv tidak ditemukan.")
    daily = pd.read_csv(DAILY_PATH, parse_dates=["dteday"])
    hourly = pd.read_csv(HOURLY_PATH, parse_dates=["dteday", "datetime"])
    daily["demand_segment"] = pd.Categorical(daily["demand_segment"], categories=SEG_ORDER, ordered=True)
    return daily, hourly


try:
    daily_df, hourly_df = load_data()
except FileNotFoundError as error:
    st.error(str(error))
    st.stop()

st.sidebar.title("Filter Data")
min_date = daily_df["dteday"].min().date()
max_date = daily_df["dteday"].max().date()
date_range = st.sidebar.date_input(
    "Rentang tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if not date_range:
    st.warning("Silakan pilih rentang tanggal terlebih dahulu.")
    st.stop()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range

selected_seasons = st.sidebar.multiselect("Musim", SEASON_ORDER, default=SEASON_ORDER)
selected_day_types = st.sidebar.multiselect("Tipe hari", DAY_ORDER, default=DAY_ORDER)
selected_weather = st.sidebar.multiselect("Kondisi cuaca", WEATHER_ORDER, default=WEATHER_ORDER)

st.sidebar.markdown("---")
st.sidebar.caption("Sumber: Bike Sharing Dataset (Fanaee-T & Gama, 2013).")
st.sidebar.info(
    "Segmentasi permintaan dihitung dari kuartil cnt harian seluruh periode. "
    "Filter hanya membatasi data yang ditampilkan, bukan ambang segmen."
)

start_ts = pd.Timestamp(start_date)
end_ts = pd.Timestamp(end_date)
if start_ts > end_ts:
    st.sidebar.error("Tanggal mulai harus lebih kecil atau sama dengan tanggal akhir.")
    st.stop()

if not selected_seasons or not selected_day_types or not selected_weather:
    st.warning("Pilih minimal satu musim, tipe hari, dan kondisi cuaca.")
    st.stop()

daily_mask = (
    daily_df["dteday"].between(start_ts, end_ts)
    & daily_df["season_label"].isin(selected_seasons)
    & daily_df["day_type"].isin(selected_day_types)
    & daily_df["weather_label"].isin(selected_weather)
)
hourly_mask = (
    hourly_df["dteday"].between(start_ts, end_ts)
    & hourly_df["season_label"].isin(selected_seasons)
    & hourly_df["day_type"].isin(selected_day_types)
    & hourly_df["weather_label"].isin(selected_weather)
)
daily = daily_df.loc[daily_mask].copy()
hourly = hourly_df.loc[hourly_mask].copy()

if daily.empty or hourly.empty:
    st.warning("Tidak ada data yang sesuai dengan kombinasi filter. Silakan ubah filter.")
    st.stop()

st.title("Bike Sharing Dashboard")
st.markdown("**Analisis permintaan penyewaan sepeda Capital Bikeshare, Washington D.C. (2011–2012)**")
st.caption(
    f"Periode data: {daily['dteday'].min():%d %b %Y} – {daily['dteday'].max():%d %b %Y} | "
    f"{len(daily):,} hari | {len(hourly):,} observasi per jam"
)

total_rentals = daily["cnt"].sum()
avg_daily = daily["cnt"].mean()
casual_share = daily["casual"].sum() / total_rentals * 100
registered_share = daily["registered"].sum() / total_rentals * 100

metric_cols = st.columns(4)
metric_cols[0].metric("Total penyewaan", f"{total_rentals:,.0f}")
metric_cols[1].metric("Rata-rata per hari", f"{avg_daily:,.0f}")
metric_cols[2].metric("Registered", f"{registered_share:.1f}%")
metric_cols[3].metric("Casual", f"{casual_share:.1f}%")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Ringkasan", "Pola Jam", "Cuaca", "Segmen Pengguna", "Segmentasi Permintaan", "Kesimpulan"]
)

with tab1:
    st.subheader("Tren dan distribusi permintaan")
    monthly = daily.groupby(["year", "month"], as_index=False).agg(total=("cnt", "sum"))
    monthly["bulan"] = pd.to_datetime(dict(year=monthly["year"], month=monthly["month"], day=1))
    monthly["tahun"] = monthly["year"].astype(str)
    fig_monthly = px.line(
        monthly,
        x="bulan",
        y="total",
        color="tahun",
        markers=True,
        color_discrete_sequence=[COLORS["secondary"], COLORS["primary"]],
        labels={"bulan": "Bulan", "total": "Total penyewaan", "tahun": "Tahun"},
    )
    fig_monthly.update_layout(
        title="Tren Total Penyewaan Bulanan",
        template="plotly_white",
        hovermode="x unified",
        legend_title_text="Tahun",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_monthly.update_xaxes(dtick="M1", tickformat="%b %Y")
    fig_monthly.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_monthly, width="stretch")

    daily_sorted = daily.sort_values("dteday").copy()
    daily_sorted["rolling_7"] = daily_sorted["cnt"].rolling(7, min_periods=1).mean()
    fig_daily = go.Figure()
    fig_daily.add_trace(
        go.Scatter(
            x=daily_sorted["dteday"],
            y=daily_sorted["cnt"],
            mode="lines",
            name="Penyewaan harian",
            line=dict(color=COLORS["secondary"], width=1),
            opacity=0.55,
        )
    )
    fig_daily.add_trace(
        go.Scatter(
            x=daily_sorted["dteday"],
            y=daily_sorted["rolling_7"],
            mode="lines",
            name="Rata-rata 7 hari",
            line=dict(color=COLORS["primary"], width=2.5),
        )
    )
    fig_daily.update_layout(
        title="Penyewaan Harian dan Rata-rata Bergerak 7 Hari",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_daily.update_yaxes(title="Jumlah penyewaan", rangemode="tozero")
    st.plotly_chart(fig_daily, width="stretch")

    left, right = st.columns(2)
    with left:
        season_totals = (
            daily.groupby("season_label", as_index=False)
            .agg(total=("cnt", "sum"))
            .assign(season_label=lambda x: pd.Categorical(x["season_label"], categories=SEASON_ORDER, ordered=True))
            .sort_values("season_label")
        )
        fig_season = px.bar(
            season_totals,
            x="season_label",
            y="total",
            color="season_label",
            color_discrete_map=SEASON_COLORS,
            text=season_totals["total"].map(lambda value: f"{value:,.0f}"),
            labels={"season_label": "Musim", "total": "Total penyewaan"},
        )
        fig_season.update_layout(
            title="Total Penyewaan per Musim",
            template="plotly_white",
            showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10),
        )
        fig_season.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig_season, width="stretch")
    with right:
        heat = (
            hourly.pivot_table(index="weekday_name", columns="hr", values="cnt", aggfunc="mean")
            .reindex(WEEKDAY_ORDER)
        )
        fig_heat = px.imshow(
            heat,
            aspect="auto",
            color_continuous_scale="Blues",
            labels={"x": "Jam", "y": "Hari", "color": "Rata-rata penyewaan"},
        )
        fig_heat.update_layout(
            title="Rata-rata Penyewaan per Hari dan Jam",
            template="plotly_white",
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig_heat, width="stretch")
    st.caption("Sumber: Bike Sharing Dataset (2011–2012). Filter di sidebar memengaruhi seluruh tab.")

with tab2:
    st.subheader("Pola permintaan per jam")
    hourly_pattern = (
        hourly.groupby(["day_type", "hr"], as_index=False)
        .agg(avg_rentals=("cnt", "mean"), avg_casual=("casual", "mean"), avg_registered=("registered", "mean"))
    )
    fig_hour = px.line(
        hourly_pattern,
        x="hr",
        y="avg_rentals",
        color="day_type",
        markers=True,
        color_discrete_map=DAY_COLORS,
        category_orders={"day_type": DAY_ORDER},
        labels={"hr": "Jam dalam sehari", "avg_rentals": "Rata-rata penyewaan per jam", "day_type": "Tipe hari"},
    )
    for day_type in DAY_ORDER:
        subset = hourly_pattern[hourly_pattern["day_type"] == day_type]
        if subset.empty:
            continue
        peak = subset.loc[subset["avg_rentals"].idxmax()]
        fig_hour.add_annotation(
            x=peak["hr"],
            y=peak["avg_rentals"],
            text=f"Puncak {peak['hr']:.0f}:00<br>{peak['avg_rentals']:,.0f}/jam",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(color=DAY_COLORS[day_type], size=10),
        )
    fig_hour.update_layout(
        title="Rata-rata Penyewaan per Jam: Hari Kerja vs Akhir Pekan/Libur",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_hour.update_xaxes(dtick=1, range=[-0.5, 23.5])
    fig_hour.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_hour, width="stretch")

    block_pattern = (
        hourly.groupby(["day_type", "time_block"], observed=True, as_index=False)
        .agg(avg_rentals=("cnt", "mean"))
    )
    fig_block = px.bar(
        block_pattern,
        x="time_block",
        y="avg_rentals",
        color="day_type",
        barmode="group",
        color_discrete_map=DAY_COLORS,
        category_orders={"time_block": TIME_BLOCK_ORDER, "day_type": DAY_ORDER},
        labels={"time_block": "Blok waktu", "avg_rentals": "Rata-rata penyewaan per jam", "day_type": "Tipe hari"},
    )
    fig_block.update_layout(
        title="Rata-rata Penyewaan per Blok Waktu",
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_block.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_block, width="stretch")

    peak_table = (
        hourly_pattern.sort_values(["day_type", "avg_rentals"], ascending=[True, False])
        .groupby("day_type", as_index=False)
        .head(5)
        .sort_values(["day_type", "avg_rentals"], ascending=[True, False])
    )
    peak_table["jam"] = peak_table["hr"].map(lambda value: f"{value:.0f}:00")
    st.markdown("**Lima jam dengan rata-rata penyewaan tertinggi**")
    st.dataframe(
        peak_table[["day_type", "jam", "avg_rentals"]].rename(
            columns={"day_type": "Tipe hari", "jam": "Jam", "avg_rentals": "Rata-rata penyewaan/jam"}
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption("Sumber: Bike Sharing Dataset (2011–2012). Rata-rata dihitung dari cnt per jam.")

with tab3:
    st.subheader("Pengaruh cuaca terhadap permintaan")
    weather_avg = (
        daily.groupby("weather_label", as_index=False)
        .agg(rata_rata=("cnt", "mean"), jumlah_hari=("cnt", "size"))
        .assign(weather_label=lambda x: pd.Categorical(x["weather_label"], categories=WEATHER_ORDER, ordered=True))
        .sort_values("weather_label")
    )
    fig_weather = px.bar(
        weather_avg,
        x="weather_label",
        y="rata_rata",
        color="weather_label",
        color_discrete_map=WEATHER_COLORS,
        text=weather_avg["rata_rata"].map(lambda value: f"{value:,.0f}"),
        labels={"weather_label": "Kondisi cuaca", "rata_rata": "Rata-rata penyewaan per hari"},
    )
    fig_weather.update_layout(
        title="Rata-rata Penyewaan Harian berdasarkan Kondisi Cuaca",
        template="plotly_white",
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_weather.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig_weather, width="stretch")

    left, right = st.columns(2)
    with left:
        fig_temp = px.scatter(
            daily,
            x="temp_c",
            y="cnt",
            color="weather_label",
            color_discrete_map=WEATHER_COLORS,
            category_orders={"weather_label": WEATHER_ORDER},
            opacity=0.65,
            labels={"temp_c": "Suhu udara rata-rata (°C)", "cnt": "Penyewaan harian", "weather_label": "Cuaca"},
        )
        if len(daily) > 1:
            coef = np.polyfit(daily["temp_c"], daily["cnt"], 1)
            x_line = np.linspace(daily["temp_c"].min(), daily["temp_c"].max(), 100)
            fig_temp.add_trace(
                go.Scatter(
                    x=x_line,
                    y=np.polyval(coef, x_line),
                    mode="lines",
                    name="Tren linear",
                    line=dict(color=COLORS["dark"], dash="dash", width=2),
                )
            )
        fig_temp.update_layout(
            title="Hubungan Suhu dan Penyewaan Harian",
            template="plotly_white",
            margin=dict(l=10, r=10, t=50, b=10),
        )
        fig_temp.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig_temp, width="stretch")
    with right:
        corr_cols = ["cnt", "temp_c", "atemp_c", "hum_pct", "windspeed_kmh"]
        if len(daily) > 1:
            corr = daily[corr_cols].corr()["cnt"].drop("cnt").dropna().sort_values()
            if not corr.empty:
                corr_df = corr.reset_index()
                corr_df.columns = ["variabel", "korelasi"]
                fig_corr = px.bar(
                    corr_df,
                    x="korelasi",
                    y="variabel",
                    orientation="h",
                    color="korelasi",
                    color_continuous_scale=["#C44536", "#F4A261", "#2A6F97"],
                    range_color=[-1, 1],
                    text=corr_df["korelasi"].map(lambda value: f"{value:.2f}"),
                    labels={"korelasi": "Koefisien korelasi Pearson", "variabel": "Variabel cuaca"},
                )
                fig_corr.update_layout(
                    title="Korelasi Faktor Cuaca dengan Jumlah Penyewaan",
                    template="plotly_white",
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=50, b=10),
                )
                st.plotly_chart(fig_corr, width="stretch")
            else:
                st.info("Korelasi tidak dapat dihitung pada subset data ini.")
        else:
            st.info("Korelasi membutuhkan minimal dua hari data.")
    st.caption(
        "Sumber: Bike Sharing Dataset (2011–2012). Korelasi menunjukkan hubungan, bukan kausalitas."
    )

with tab4:
    st.subheader("Segmen pengguna casual vs registered")
    season_user = daily.groupby("season_label", as_index=False).agg(
        casual=("casual", "sum"), registered=("registered", "sum")
    )
    season_user["total"] = season_user["casual"] + season_user["registered"]
    season_user["registered_pct"] = season_user["registered"] / season_user["total"] * 100
    season_user["casual_pct"] = season_user["casual"] / season_user["total"] * 100
    season_user["season_label"] = pd.Categorical(
        season_user["season_label"], categories=SEASON_ORDER, ordered=True
    )
    season_user = season_user.sort_values("season_label")

    fig_user_season = go.Figure()
    fig_user_season.add_trace(
        go.Bar(
            x=season_user["season_label"].astype(str),
            y=season_user["registered_pct"],
            name="Registered",
            marker_color=COLORS["primary"],
            text=season_user["registered_pct"].map(lambda value: f"{value:.1f}%"),
            textposition="inside",
            textfont=dict(color="white"),
        )
    )
    fig_user_season.add_trace(
        go.Bar(
            x=season_user["season_label"].astype(str),
            y=season_user["casual_pct"],
            name="Casual",
            marker_color=COLORS["accent"],
            text=season_user["casual_pct"].map(lambda value: f"{value:.1f}%"),
            textposition="inside",
            textfont=dict(color=COLORS["dark"]),
        )
    )
    fig_user_season.update_layout(
        title="Komposisi Penyewaan Registered vs Casual per Musim",
        barmode="stack",
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_user_season.update_yaxes(title="Proporsi penyewaan (%)", range=[0, 100])
    st.plotly_chart(fig_user_season, width="stretch")

    hourly_users = hourly.melt(
        id_vars=["day_type", "hr"],
        value_vars=["casual", "registered"],
        var_name="user_type",
        value_name="rentals",
    )
    hourly_users = hourly_users.groupby(["day_type", "hr", "user_type"], as_index=False).rentals.mean()
    hourly_users["user_type"] = hourly_users["user_type"].str.capitalize()
    fig_user_hour = px.line(
        hourly_users,
        x="hr",
        y="rentals",
        color="user_type",
        facet_col="day_type",
        markers=True,
        color_discrete_map={"Registered": COLORS["primary"], "Casual": COLORS["accent"]},
        category_orders={"day_type": DAY_ORDER, "user_type": ["Registered", "Casual"]},
        labels={"hr": "Jam", "rentals": "Rata-rata penyewaan per jam", "user_type": "Tipe pengguna", "day_type": "Tipe hari"},
    )
    fig_user_hour.for_each_annotation(lambda annotation: annotation.update(text=annotation.text.split("=")[-1]))
    fig_user_hour.update_xaxes(dtick=2)
    fig_user_hour.update_yaxes(rangemode="tozero")
    fig_user_hour.update_layout(
        title="Pola Harian Registered vs Casual",
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig_user_hour, width="stretch")

    yoy = daily.groupby("year", as_index=False).agg(
        total=("cnt", "sum"), casual=("casual", "sum"), registered=("registered", "sum")
    )
    fig_yoy = go.Figure()
    fig_yoy.add_trace(go.Bar(x=yoy["year"].astype(str), y=yoy["registered"], name="Registered", marker_color=COLORS["primary"]))
    fig_yoy.add_trace(go.Bar(x=yoy["year"].astype(str), y=yoy["casual"], name="Casual", marker_color=COLORS["accent"]))
    fig_yoy.update_layout(
        title="Total Penyewaan per Tahun berdasarkan Tipe Pengguna",
        barmode="stack",
        template="plotly_white",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig_yoy.update_yaxes(title="Total penyewaan", rangemode="tozero")
    st.plotly_chart(fig_yoy, width="stretch")
    st.caption("Sumber: Bike Sharing Dataset (2011–2012). Registered mencakup pengguna berlangganan; casual membayar per perjalanan.")

with tab5:
    st.subheader("Segmentasi permintaan harian (binning kuartil)")
    seg_profile = (
        daily.groupby("demand_segment", observed=True)
        .agg(
            jumlah_hari=("cnt", "size"),
            min_cnt=("cnt", "min"),
            max_cnt=("cnt", "max"),
            rata_rata=("cnt", "mean"),
            rata_rata_suhu=("temp_c", "mean"),
            rata_rata_kelembapan=("hum_pct", "mean"),
            rata_rata_angin=("windspeed_kmh", "mean"),
            pct_hari_kerja=("workingday", "mean"),
        )
        .reindex(SEG_ORDER)
        .dropna(how="all")
    )
    if seg_profile.empty:
        st.info("Tidak ada segmen pada kombinasi filter ini.")
    else:
        seg_profile["pct_hari_kerja"] = seg_profile["pct_hari_kerja"] * 100
        left, right = st.columns(2)
        with left:
            fig_seg_avg = px.bar(
                x=seg_profile.index.astype(str),
                y=seg_profile["rata_rata"],
                color=seg_profile.index.astype(str),
                color_discrete_map=SEG_COLORS,
                text=seg_profile["rata_rata"].map(lambda value: f"{value:,.0f}"),
                labels={"x": "Segmen permintaan", "y": "Rata-rata penyewaan per hari", "color": "Segmen"},
            )
            fig_seg_avg.update_layout(
                title="Rata-rata Penyewaan per Segmen",
                template="plotly_white",
                showlegend=False,
                margin=dict(l=10, r=10, t=50, b=10),
            )
            fig_seg_avg.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_seg_avg, width="stretch")
        with right:
            fig_seg_days = px.bar(
                x=seg_profile.index.astype(str),
                y=seg_profile["jumlah_hari"],
                color=seg_profile.index.astype(str),
                color_discrete_map=SEG_COLORS,
                text=seg_profile["jumlah_hari"],
                labels={"x": "Segmen permintaan", "y": "Jumlah hari", "color": "Segmen"},
            )
            fig_seg_days.update_layout(
                title="Jumlah Hari per Segmen",
                template="plotly_white",
                showlegend=False,
                margin=dict(l=10, r=10, t=50, b=10),
            )
            fig_seg_days.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_seg_days, width="stretch")

        profile_table = seg_profile.reset_index().rename(
            columns={
                "demand_segment": "Segmen",
                "jumlah_hari": "Jumlah hari",
                "min_cnt": "Min cnt",
                "max_cnt": "Max cnt",
                "rata_rata": "Rata-rata cnt",
                "rata_rata_suhu": "Rata-rata suhu (°C)",
                "rata_rata_kelembapan": "Rata-rata kelembapan (%)",
                "rata_rata_angin": "Rata-rata angin (km/jam)",
                "pct_hari_kerja": "Hari kerja (%)",
            }
        )
        st.markdown("**Profil setiap segmen**")
        st.dataframe(
            profile_table.style.format(
                {
                    "Min cnt": "{:,.0f}",
                    "Max cnt": "{:,.0f}",
                    "Rata-rata cnt": "{:,.0f}",
                    "Rata-rata suhu (°C)": "{:.1f}",
                    "Rata-rata kelembapan (%)": "{:.1f}",
                    "Rata-rata angin (km/jam)": "{:.1f}",
                    "Hari kerja (%)": "{:.1f}",
                }
            ),
            hide_index=True,
            width="stretch",
        )

        season_seg = pd.crosstab(daily["demand_segment"], daily["season_label"], normalize="index") * 100
        season_seg = season_seg.reindex(seg_profile.index).reindex(columns=SEASON_ORDER).fillna(0)
        fig_seg_season = go.Figure()
        for season in SEASON_ORDER:
            fig_seg_season.add_trace(
                go.Bar(
                    x=season_seg.index.astype(str),
                    y=season_seg[season],
                    name=season,
                    marker_color=SEASON_COLORS[season],
                )
            )
        fig_seg_season.update_layout(
            title="Komposisi Musim per Segmen Permintaan",
            barmode="stack",
            template="plotly_white",
            margin=dict(l=10, r=10, t=50, b=10),
        )
        fig_seg_season.update_yaxes(title="Proporsi hari (%)", range=[0, 100])
        st.plotly_chart(fig_seg_season, width="stretch")
    st.caption(
        "Sumber: Bike Sharing Dataset (2011–2012). Segmen Low/Medium/High/Very High dibentuk dari kuartil cnt harian."
    )

with tab6:
    st.subheader("Kesimpulan dan rekomendasi")
    st.info(
        "**Pola jam:** hari kerja memiliki dua puncak (08.00 dan 17.00), sedangkan akhir pekan "
        "memiliki satu puncak siang (13.00). Kapasitas armada perlu disesuaikan dengan jam sibuk masing-masing tipe hari."
    )
    st.info(
        "**Cuaca:** dibanding cuaca cerah/berawan, cuaca berkabut/mendung menurunkan permintaan sekitar 17%, "
        "sedangkan hujan/salju ringan menurunkan sekitar 63%. Suhu memiliki korelasi positif kuat (r ≈ 0,63)."
    )
    st.info(
        "**Segmen pengguna:** registered mendominasi sekitar 81% penyewaan, tetapi casual lebih tinggi pada "
        "akhir pekan dan musim Summer/Fall. Pengguna casual adalah target utama kampanye konversi membership."
    )
    st.info(
        "**Segmentasi permintaan:** hari Very High didominasi cuaca cerah, suhu hangat, dan musim Fall/Summer, "
        "tetapi sebagian besar tetap berupa hari kerja. Perencanaan armada perlu mempertimbangkan cuaca, bukan hanya akhir pekan."
    )

    st.markdown("### Action item prioritas")
    st.success(
        "1. **Rebalancing armada dan staf** pada hari kerja pukul 07.00–09.00 dan 16.00–19.00, serta akhir pekan pukul 10.00–16.00. "
        "Pantau ketersediaan sepeda per stasiun dan waktu tunggu."
    )
    st.success(
        "2. **Rencana operasional berbasis cuaca:** kurangi repositioning saat hujan/salju ringan, alihkan ke perawatan; "
        "tambah armada pada hari cerah dan hangat."
    )
    st.success(
        "3. **Kampanye konversi casual → registered** pada akhir pekan dan musim Summer/Fall melalui trial membership, "
        "diskon perpanjangan, atau poin loyalitas."
    )
    st.success(
        "4. **Perencanaan armada musiman:** tambah armada sebelum hari Very High dan jadwalkan perawatan pada hari Low."
    )
    st.markdown(
        "**Catatan:** angka pada tab ini merangkum seluruh periode 2011–2012. Gunakan filter di sidebar "
        "untuk mengeksplorasi subset data; hasil pada tab lain akan menyesuaikan filter."
    )

st.markdown("---")
st.caption(
    "Sumber data: Bike Sharing Dataset — Fanaee-T & Gama (2013) | "
    "Dibuat untuk proyek akhir kelas Belajar Analisis Data dengan Python, Dicoding."
)
