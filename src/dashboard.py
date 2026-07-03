import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Google Maps Business Analysis",
    page_icon="📍",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0F172A,#1E293B);
    color:white;
}

h1,h2,h3,h4{
    color:#38BDF8;
}

section[data-testid="stSidebar"]{
    background-color:#020617;
}

div[data-testid="metric-container"]{
    background:linear-gradient(
        135deg,
        #1E293B,
        #0F172A
    );
    border:1px solid #334155;
    border-radius:20px;
    padding:20px;
    box-shadow:0px 8px 25px rgba(
        0,0,0,0.4
    );
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================
df = pd.read_csv(
    "data/cleaned_business_data.csv"
)

df.rename(
    columns={
        "Rating (fill manually)": "Rating",
        "Reviews (fill manually)": "Reviews"
    },
    inplace=True
)

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/854/854878.png",
    width=90
)

st.sidebar.title(
    "📌 Dashboard Filters"
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

rating = st.sidebar.slider(
    "Minimum Rating",
    float(df["Rating"].min()),
    float(df["Rating"].max()),
    float(df["Rating"].min())
)

website = st.sidebar.selectbox(
    "Website Status",
    ["All", "Yes", "No"]
)

search = st.sidebar.text_input(
    "🔍 Search Business"
)

# ==========================================
# FILTER DATA
# ==========================================
filtered_df = df[
    (df["Category"].isin(categories))
    &
    (df["Rating"] >= rating)
]

if website != "All":
    filtered_df = filtered_df[
        filtered_df["Has Website"] == website
    ]

if search:
    filtered_df = filtered_df[
        filtered_df["Shop Name"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

# ==========================================
# DOWNLOAD BUTTON
# ==========================================
st.sidebar.download_button(
    "📥 Download CSV",
    filtered_df.to_csv(index=False),
    "filtered_businesses.csv",
    "text/csv"
)

st.sidebar.markdown("---")

st.sidebar.metric(
    "Businesses",
    len(filtered_df)
)

st.sidebar.metric(
    "Average Rating",
    round(
        filtered_df["Rating"].mean(),
        2
    )
)

# ==========================================
# HEADER
# ==========================================
st.markdown("""
<div style="
padding:25px;
border-radius:25px;
background:
linear-gradient(
90deg,
#0F172A,
#1E3A8A
);
">

<h1 style="
text-align:center;
color:white;
">
📍 Google Maps Business Analysis Dashboard
</h1>

<h4 style="
text-align:center;
color:#CBD5E1;
">
Find • Analyze • Recommend
</h4>

</div>
""",
unsafe_allow_html=True)

st.write("")

# ==========================================
# KPI CARDS
# ==========================================
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🏢 Total Businesses",
    len(filtered_df)
)

c2.metric(
    "🌐 With Website",
    (filtered_df["Has Website"]=="Yes").sum()
)

c3.metric(
    "❌ Without Website",
    (filtered_df["Has Website"]=="No").sum()
)

c4.metric(
    "⭐ Average Rating",
    round(
        filtered_df["Rating"].mean(),
        2
    )
)

st.divider()

# ==========================================
# CHARTS
# ==========================================
col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        filtered_df,
        names="Has Website",
        hole=0.5,
        title="Website Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    category_df = (
        filtered_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_df.columns = [
        "Category",
        "Count"
    ]

    fig = px.bar(
        category_df,
        x="Count",
        y="Category",
        orientation="h",
        title="Business Categories"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================
# TOP 10 BUSINESSES
# ==========================================
st.subheader(
    "🏆 Top 10 Businesses Without Website"
)

top10 = filtered_df[
    filtered_df["Has Website"]=="No"
].sort_values(
    by=["Rating","Reviews"],
    ascending=False
).head(10)

st.dataframe(
    top10[
        [
            "Shop Name",
            "Category",
            "Rating",
            "Reviews"
        ]
    ],
    use_container_width=True
)

st.divider()

# ==========================================
# HIGH OPPORTUNITY
# ==========================================
st.subheader(
    "🚀 High Opportunity Businesses"
)

high = filtered_df[
    (filtered_df["Has Website"]=="No")
    &
    (filtered_df["Rating"]>=4)
]

st.dataframe(
    high[
        [
            "Shop Name",
            "Category",
            "Rating",
            "Reviews"
        ]
    ],
    use_container_width=True
)

st.divider()

# ==========================================
# MAP
# ==========================================
st.subheader(
    "🗺 Business Locations"
)

m = folium.Map(
    location=[25.24,86.97],
    zoom_start=12,
    tiles="CartoDB dark_matter"
)

cluster = MarkerCluster().add_to(m)

colors = {
    "Restaurant":"red",
    "Medical Store":"green",
    "Bank":"blue",
    "General Shop":"orange",
    "Cafe":"purple",
    "Mall":"cadetblue",
    "Electronics":"darkblue"
}

for _, row in filtered_df.iterrows():

    color = colors.get(
        row["Category"],
        "gray"
    )

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=8,
        popup=f"""
        <b>{row['Shop Name']}</b><br>
        Category: {row['Category']}<br>
        Rating: {row['Rating']}⭐<br>
        Website: {row['Has Website']}
        """,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8
    ).add_to(cluster)

st_folium(
    m,
    use_container_width=True,
    height=550
)

# ==========================================
# INSIGHTS
# ==========================================
st.divider()

st.subheader(
    "📈 Key Insights"
)

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
        ✅ Total Businesses: {len(df)}

        ✅ Businesses Without Website:
        {(df["Has Website"]=="No").sum()}

        ✅ Average Rating:
        {round(df["Rating"].mean(),2)}
        """
    )

with col2:

    st.info(
        """
        💡 Opportunity

        Most local businesses do not
        have websites.

        This creates opportunities
        for digital transformation,
        online marketing and website
        development services.
        """
    )

# ==========================================
# FOOTER
# ==========================================
st.markdown("""
<hr>

<center>

Made with ❤️ by Akshay Kumar

B.Tech Data Science | CGC University

</center>
""",
unsafe_allow_html=True)