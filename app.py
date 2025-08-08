# app.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io

# --------------------------
# Streamlit Page Config
# --------------------------
st.set_page_config(page_title="Superstore EDA Dashboard", layout="wide")
st.title("📊 Superstore Sales EDA Dashboard")

# --------------------------
# Load Data Function
# --------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Attachment.xlsx", sheet_name="Orders")
        return df
    except FileNotFoundError:
        st.error("❌ File not found. Please ensure 'Attachment.xlsx' is in the app directory.")
        return pd.DataFrame()
    except ValueError as e:
        st.error(f"❌ Error reading Excel file: {e}")
        return pd.DataFrame()

df = load_data()

# --------------------------
# Sidebar Navigation
# --------------------------
step = st.sidebar.radio(
    "Select Step",
    ["Step 1: Data Loading", "Step 2: Data Cleaning",
     "Step 3: Visualization", "Step 4: Outlier Detection"]
)

# --------------------------
# STEP 1 - Data Loading
# --------------------------
if step == "Step 1: Data Loading":
    if df.empty:
        st.warning("⚠ No data loaded.")
    else:
        st.subheader("First 10 Rows")
        st.dataframe(df.head(10))

        st.write("**Shape:**", df.shape)
        st.write("**Column Names:**", list(df.columns))

        st.write("**Data Info:**")
        buf = io.StringIO()
        df.info(buf=buf)
        info_str = buf.getvalue()
        st.text(info_str)

# --------------------------
# STEP 2 - Data Cleaning
# --------------------------
elif step == "Step 2: Data Cleaning":
    if df.empty:
        st.warning("⚠ No data to clean.")
    else:
        st.subheader("Missing Values Before Cleaning")
        st.write(df.isnull().sum())

        # Drop duplicates
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            df = df.drop_duplicates()
            st.info(f"Removed {dup_count} duplicate rows.")

        # Drop missing Postal Code rows
        if df['Postal Code'].isnull().sum() > 0:
            missing_postal = df['Postal Code'].isnull().sum()
            df = df.dropna(subset=['Postal Code'])
            st.info(f"Dropped {missing_postal} rows with missing Postal Code.")

        # Convert numeric columns
        numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit', 'Postal Code']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        st.subheader("Missing Values After Cleaning")
        st.write(df.isnull().sum())

        st.success("✅ Data cleaning completed.")
        st.dataframe(df.head(10))

# --------------------------
# STEP 3 - Visualization
# --------------------------
elif step == "Step 3: Visualization":
    if df.empty:
        st.warning("⚠ No data to visualize.")
    else:
        st.sidebar.header("Filters")
        category_filter = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())
        region_filter = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())

        filtered_df = df[(df['Category'].isin(category_filter)) & (df['Region'].isin(region_filter))]

        if filtered_df.empty:
            st.warning("⚠ No data after applying filters.")
        else:
            tab1, tab2, tab3, tab4 = st.tabs(["Bar Charts", "Scatter Plots", "Histograms", "Heatmap"])

            # Bar Charts
            with tab1:
                st.subheader("Category Count")
                cat_counts = filtered_df['Category'].value_counts().reset_index()
                cat_counts.columns = ['Category', 'Count']
                fig = px.bar(cat_counts, x='Category', y='Count')
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Sub-Category Count")
                subcat_counts = filtered_df['Sub-Category'].value_counts().reset_index()
                subcat_counts.columns = ['Sub-Category', 'Count']
                fig = px.bar(subcat_counts, x='Sub-Category', y='Count')
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Segment Count")
                seg_counts = filtered_df['Segment'].value_counts().reset_index()
                seg_counts.columns = ['Segment', 'Count']
                fig = px.bar(seg_counts, x='Segment', y='Count')
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Region Count")
                reg_counts = filtered_df['Region'].value_counts().reset_index()
                reg_counts.columns = ['Region', 'Count']
                fig = px.bar(reg_counts, x='Region', y='Count')
                st.plotly_chart(fig, use_container_width=True)

            # Scatter Plots
            with tab2:
                st.subheader("Sales vs Profit")
                fig = px.scatter(filtered_df, x='Sales', y='Profit', color='Category', hover_data=['State'])
                st.plotly_chart(fig, use_container_width=True)

                st.subheader("Discount vs Profit")
                fig = px.scatter(filtered_df, x='Discount', y='Profit', color='Category', hover_data=['State'])
                st.plotly_chart(fig, use_container_width=True)

            # Histograms
            with tab3:
                numeric_cols = ['Sales', 'Profit', 'Quantity', 'Discount']
                for col in numeric_cols:
                    st.subheader(f"Distribution of {col}")
                    fig = px.histogram(filtered_df, x=col, nbins=50, marginal="box", color='Category')
                    st.plotly_chart(fig, use_container_width=True)

            # Heatmap
            with tab4:
                st.subheader("Correlation Heatmap")
                corr = filtered_df[['Sales', 'Profit', 'Discount', 'Quantity']].corr()
                fig, ax = plt.subplots()
                sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

# --------------------------
# STEP 4 - Outlier Detection
# --------------------------
elif step == "Step 4: Outlier Detection":
    if df.empty:
        st.warning("⚠ No data to detect outliers.")
    else:
        st.subheader("Outlier Detection with Boxplots & Stats")
        num_cols = ['Sales', 'Profit', 'Discount']

        for col in num_cols:
            if col in df.columns:
                st.write(f"### {col}")

                # Calculate IQR
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                # Find outliers
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
                num_outliers = len(outliers)
                perc_outliers = (num_outliers / len(df)) * 100

                st.write(f"- **Q1:** {Q1:.2f}")
                st.write(f"- **Q3:** {Q3:.2f}")
                st.write(f"- **IQR:** {IQR:.2f}")
                st.write(f"- **Lower Bound:** {lower_bound:.2f}")
                st.write(f"- **Upper Bound:** {upper_bound:.2f}")
                st.write(f"- **Number of Outliers:** {num_outliers}")
                st.write(f"- **Percentage of Outliers:** {perc_outliers:.2f}%")

                # Plot boxplot
                fig, ax = plt.subplots()
                sns.boxplot(x=df[col], ax=ax)
                st.pyplot(fig)
            else:
                st.warning(f"⚠ Column '{col}' not found in data.")
