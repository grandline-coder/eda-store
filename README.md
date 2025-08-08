# 📊 Superstore Sales EDA Dashboard

An interactive **Streamlit** web application for performing **Exploratory Data Analysis (EDA)** on the Superstore sales dataset.  
The app provides step-by-step analysis, visualizations, and outlier detection to gain insights into sales performance, profitability, and discounts.

---

## 🚀 Features
- **Step-by-step workflow:**
  1. Data Loading – Preview, dataset info, and structure
  2. Data Cleaning – Handle missing values, duplicates, and data types
  3. Visualization – Interactive charts for sales, profit, quantity, and discount
  4. Outlier Detection – Boxplots and IQR-based outlier statistics
- **Interactive Filters** – Filter by category, region, and more
- **Visualizations** using **Plotly**, **Seaborn**, and **Matplotlib**
- **Correlation heatmaps** for numerical columns
- **Automatic outlier stats** including percentage and bounds

---

## 🛠 Tech Stack
- **Python**
- **Streamlit** – Web app framework
- **Pandas** – Data manipulation
- **Plotly Express** – Interactive visualizations
- **Seaborn / Matplotlib** – Statistical plots
- **OpenPyXL** – Excel file support

---

## 📂 Project Structure
```
├── app.py               # Main Streamlit app
├── Attachment.xlsx      # Superstore dataset
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 📦 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Deployment
This app can be deployed to **Streamlit Cloud**:
1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and deploy.
3. Select your repo and `app.py` as the main file.

---

## 📸 Screenshots
*(Add some screenshots of your dashboard here)*

---

## 📜 License
This project is licensed under the MIT License – feel free to use and modify.
