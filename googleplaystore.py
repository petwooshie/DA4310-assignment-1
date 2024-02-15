import pandas as pd
import streamlit as st
import altair as alt

df = pd.read_csv('googleplaystore.csv')

# remove non-numeric values from 'Installs' column
df['Installs'] = df['Installs'].str.replace('[^0-9]', '', regex=True)

# convert 'Installs' column to numeric
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')

# remove non-numeric values from 'Size' column
df['Size'] = df['Size'].replace('Varies with device', pd.NA)

# convert 'Size' column to numeric
df['Size'] = pd.to_numeric(df['Size'].str.replace('M', ''), errors='coerce')

# convert 'Reviews' column to numeric
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# set page configuration and add some styling
st.set_page_config(layout='wide')
st.markdown("""
<style>
h1 {
    color: #0066CC;
}
h2 {
    color: #0066CC;
}
</style>
""", unsafe_allow_html=True)

# title
st.title('Google Play Store App Analysis')

# visualization 1: App Category Distribution
st.header('App Category Distribution')

with st.expander("Filter by Category"):
    selected_categories = st.multiselect('Select Category', df['Category'].unique(), key='category_multiselect')
    filtered_df = df[df['Category'].isin(selected_categories)] if selected_categories else df

    category_counts = filtered_df['Category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Number of Apps']

    pie = alt.Chart(category_counts).mark_circle().encode(
        alt.X('Number of Apps', title='Number of Apps'),
        alt.Y('Category', title='Category'),
        size='Number of Apps',
        color='Category',
        tooltip=['Category', 'Number of Apps']
    ).properties(
        width=600,
        height=400,
        title='Distribution of Apps Across Different Categories'
    )

    st.altair_chart(pie)

# visualization 2: App Ratings Distribution
st.header('App Ratings Distribution')

with st.expander("Filter by Rating Range"):
    min_rating = st.slider('Minimum Rating', min_value=float(df['Rating'].min()), max_value=float(df['Rating'].max()), value=float(df['Rating'].min()), key='min_rating_slider')
    max_rating = st.slider('Maximum Rating', min_value=float(df['Rating'].min()), max_value=float(df['Rating'].max()), value=float(df['Rating'].max()), key='max_rating_slider')

    filtered_df = df[(df['Rating'] >= min_rating) & (df['Rating'] <= max_rating)]

    scatter = alt.Chart(filtered_df).mark_circle().encode(
        x='Rating',
        y='Reviews',
        color='Rating',
        tooltip=['Rating', 'Reviews']
    ).properties(
        width=600,
        height=400,
        title='Distribution of App Ratings'
    )

    st.altair_chart(scatter)

# visualization 3: App Installs by Category
st.header('App Installs by Category')

with st.expander("Filter by Category and Number of Installs Range"):
    selected_categories_installs = st.multiselect('Select Category', df['Category'].unique(), key='category_installs_multiselect')
    min_installs = st.slider('Minimum Installs', min_value=0, max_value=int(df['Installs'].max()), value=0, key='min_installs_slider')
    max_installs = st.slider('Maximum Installs', min_value=0, max_value=int(df['Installs'].max()), value=int(df['Installs'].max()), key='max_installs_slider')

    filtered_df_installs = df[(df['Category'].isin(selected_categories_installs)) & (df['Installs'] >= min_installs) & (df['Installs'] <= max_installs)]

    bar = alt.Chart(filtered_df_installs).mark_bar().encode(
        x='Category',
        y='sum(Installs)',
        color='Category',
        tooltip=['Category', 'sum(Installs)']
    ).properties(
        width=600,
        height=400,
        title='App Installs by Category'
    )

    st.altair_chart(bar)

# visualization 4: Average Rating by Content Rating
st.header('Average Rating by Content Rating')

with st.expander("Filter by Content Rating"):
    selected_content_rating = st.multiselect('Select Content Rating', df['Content Rating'].unique(), key='content_rating_multiselect')
    filtered_df_content_rating = df[df['Content Rating'].isin(selected_content_rating)] if selected_content_rating else df

    average_rating_content_rating = filtered_df_content_rating.groupby('Content Rating')['Rating'].mean().reset_index()

    line = alt.Chart(average_rating_content_rating).mark_line().encode(
        x='Content Rating',
        y='Rating',
        tooltip=['Content Rating', 'Rating']
    ).properties(
        width=600,
        height=400,
        title='Average Rating by Content Rating'
    )

    st.altair_chart(line)

# visualization 5: App Size Distribution
st.header('App Size Distribution')

with st.expander("Filter by App Size Range"):
    min_size = st.slider('Minimum Size (MB)', min_value=0, max_value=int(df['Size'].max()), value=0, key='min_size_slider')
    max_size = st.slider('Maximum Size (MB)', min_value=0, max_value=int(df['Size'].max()), value=int(df['Size'].max()), key='max_size_slider')

    filtered_df_size = df[(df['Size'] >= min_size) & (df['Size'] <= max_size)]

    hist = alt.Chart(filtered_df_size).mark_bar().encode(
        alt.X('Size', bin=True),
        y='count()',
        tooltip=['Size', 'count()']
    ).properties(
        width=600,
        height=400,
        title='App Size Distribution'
    )

    st.altair_chart(hist)

# visualization 6: Top 10 Apps by Number of Reviews
st.header('Top 10 Apps by Number of Reviews')

top_10_apps_reviews = df.nlargest(10, 'Reviews')[['App', 'Reviews']]

with st.expander("Top 10 Apps by Number of Reviews"):
    st.table(top_10_apps_reviews)