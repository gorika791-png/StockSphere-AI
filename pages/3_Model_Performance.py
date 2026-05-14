# # import streamlit as st
# # import pandas as pd
# # import joblib
# #
# # from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
# # import plotly.graph_objects as go
# #
# # st.title("📊 Model Performance Analysis")
# # # Load dataset
# # df = pd.read_csv("cleaned_apple_stock.csv")
# #
# # # Features (same as prediction page)
# # features = [
# #     'close','volume','sma_50','ema_20','ema_50','rsi_14',
# #     'macd','macd_signal','macd_histogram','bb_width',
# #     'volatility_20d','close_lag_1','close_lag_5',
# #     'volume_lag_1','rsi_signal','macd_signal_cross',
# #     'momentum','trend_strength','price_change'
# # ]
# #
# # X = df[features]
# # y = df['target_direction']
# #
# # # Load models
# # lr_model = joblib.load("lr_model.pkl")
# # rf_model = joblib.load("rf_model.pkl")
# # lr_pred = lr_model.predict(X)
# # rf_pred = rf_model.predict(X)
# # # accuracy comparison
# # st.subheader("📈 Accuracy Comparison")
# #
# # lr_acc = accuracy_score(y, lr_pred)
# # rf_acc = accuracy_score(y, rf_pred)
# # if rf_acc > 90:
# #     st.warning("⚠️ High accuracy detected. Model may be overfitting.")
# #
# # col1, col2 = st.columns(2)
# # col1.metric("Logistic Regression Accuracy", f"{lr_acc*100:.2f}%")
# # col2.metric("Random Forest Accuracy", f"{rf_acc*100:.2f}%")
# # st.subheader("🔍 Confusion Matrix (Random Forest)")
# #
# # cm = confusion_matrix(y, rf_pred)
# #
# # fig = go.Figure(data=go.Heatmap(
# #     z=cm,
# #     x=["Predicted Down", "Predicted Up"],
# #     y=["Actual Down", "Actual Up"]
# # ))
# #
# # fig.update_layout(title="Confusion Matrix")
# # st.plotly_chart(fig)
# # # if rf_acc > 90:
# # # st.warning("⚠️ High accuracy detected. Model may be overfitting.")
# # st.subheader("📄 Classification Report")
# #
# # report = classification_report(y, rf_pred, output_dict=True)
# # report_df = pd.DataFrame(report).transpose()
# #
# # st.dataframe(report_df)
# # # accuracy bar chart
# # import matplotlib.pyplot as plt
# #
# # models = ['Logistic Regression', 'Random Forest']
# # accuracy = [lr_acc, rf_acc]
# #
# # fig, ax = plt.subplots()
# # ax.bar(models, accuracy)
# # ax.set_ylabel("Accuracy")
# # ax.set_title("Model Accuracy Comparison")
# #
# # st.pyplot(fig)
# # st.subheader("🏆 Best Model")
# #
# # if rf_acc > lr_acc:
# #     st.success("Random Forest performs better")
# # else:
# #     st.success("Logistic Regression performs better")
# #
# # st.info("""
# #     📊 Insights:
# #     - Random Forest captures complex patterns better
# #     - Logistic Regression is simpler but less powerful
# #     - Model comparison helps improve prediction reliability
# # """)
# import streamlit as st
# import pandas as pd
# import joblib
# import matplotlib.pyplot as plt
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
#
#
# st.markdown("""
# <style>
# body {
#     background-color: #0E1117;
#     color: #E6EDF3;
# }
# .block-container {
#     padding-top: 2rem;
# }
# .stMetric {
#     background-color: #161B22;
#     padding: 15px;
#     border-radius: 10px;
#     border: 1px solid #30363d;
# }
# </style>
# """, unsafe_allow_html=True)
# st.markdown("## 📈 StockSense AI")
# st.caption("AI-powered stock prediction system")
# st.title("📊 Model Performance Analysis")
#
#
# # Load dataset
# df = pd.read_csv("cleaned_apple_stock.csv")
# def card(title, value, subtitle=""):
#     st.markdown(f"""
#     <div style="
#         background:#161B22;
#         padding:20px;
#         border-radius:12px;
#         border:1px solid #30363d;
#         margin-bottom:10px;">
#         <h4 style="color:#8b949e;">{title}</h4>
#         <h2 style="color:#E6EDF3;">{value}</h2>
#         <p style="color:#6e7681;">{subtitle}</p>
#     </div>
#     """, unsafe_allow_html=True)
#
# # Feature columns (same as training)
# features = [
#     'close','volume','sma_50','ema_20','ema_50','rsi_14',
#     'macd','macd_signal','macd_histogram','bb_width',
#     'volatility_20d','close_lag_1','close_lag_5',
#     'volume_lag_1','rsi_signal','macd_signal_cross',
#     'momentum','trend_strength','price_change'
# ]
#
# X = df[features]
# y = df['target_direction']
#
# # Load models
# lr_model = joblib.load("lr_model.pkl")
# rf_model = joblib.load("rf_model.pkl")
#
# # Predictions
# lr_pred = lr_model.predict(X)
# rf_pred = rf_model.predict(X)
#
# # Accuracy
# lr_acc = accuracy_score(y, lr_pred)
# rf_acc = accuracy_score(y, rf_pred)
#
# # =========================
# # 📈 Accuracy Comparison
# # =========================
# st.subheader("📈 Accuracy Comparison")
#
# col1, col2 = st.columns(2)
#
# with col1:
#         card("Logistic Regression",
#              f"{lr_acc * 100:.2f}%",
#              "Baseline Model")
#
# with col2:
#     card("Random Forest",
#          f"{rf_acc * 100:.2f}%",
#          "Advanced Model")
#
# # Bar Chart
# st.subheader("📊 Accuracy Visualization")
#
# models = ['Logistic Regression', 'Random Forest']
# accuracy = [lr_acc, rf_acc]
#
# import plotly.express as px
#
# acc_df = pd.DataFrame({
#     "Model": ["Logistic Regression", "Random Forest"],
#     "Accuracy": [lr_acc, rf_acc]
# })
#
# fig = px.bar(
#     acc_df,
#     x="Model",
#     y="Accuracy",
#     text="Accuracy",
#     title="📊 Model Accuracy Comparison"
# )
#
# fig.update_layout(template="plotly_dark")
#
# st.plotly_chart(fig, width='stretch')
# from sklearn.metrics import precision_score, recall_score, f1_score
#
# rf_precision = precision_score(y, rf_pred)
# rf_recall = recall_score(y, rf_pred)
# rf_f1 = f1_score(y, rf_pred)
#
# col1, col2, col3 = st.columns(3)
#
# col1.metric("Precision", f"{rf_precision*100:.2f}%")
# col2.metric("Recall", f"{rf_recall*100:.2f}%")
# col3.metric("F1 Score", f"{rf_f1*100:.2f}%")
# # =========================
# # 🏆 Best Model
# # =========================
# st.subheader("🏆 Best Model")
#
# if rf_acc > lr_acc:
#     best_model = "Random Forest"
#     st.success("🏆 Random Forest performs better")
# else:
#     best_model = "Logistic Regression"
#     st.success("🏆 Logistic Regression performs better")
#
# # Overfitting warning
# if rf_acc > 0.90:
#     st.warning("⚠️ High accuracy detected. Model may be overfitting.")
#
# # =========================
# # 🔍 Confusion Matrix
# # =========================
# from sklearn.metrics import confusion_matrix
#
# cm = confusion_matrix(y, rf_pred)
#
# import seaborn as sns
#
# fig, ax = plt.subplots()
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#             xticklabels=['Down', 'Up'],
#             yticklabels=['Down', 'Up'])
#
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
#
# st.pyplot(fig)
# st.info("""
# 📊 Interpretation:
# - True Positives → Model correctly predicted UP trends
# - True Negatives → Model correctly predicted DOWN trends
# - False Positives → Risky predictions (false buy signals)
# - False Negatives → Missed opportunities
#
# 👉 Random Forest reduces false predictions, making it more reliable.
# """)
# # =========================
# # 📄 Classification Report
# # =========================
# st.subheader("📄 Classification Report")
#
# report = classification_report(y, rf_pred, output_dict=True)
# report_df = pd.DataFrame(report).transpose()
#
# # st.dataframe(report_df)
# st.dataframe(
#     report_df.style.format("{:.2f}"),
#     width='stretch'
# )
# comparison_df = pd.DataFrame({
#     "Model": ["Logistic Regression", "Random Forest"],
#     "Accuracy": [lr_acc, rf_acc]
# })
#
# st.dataframe(comparison_df)
# # =========================
# # 📊 Insights Section
# # =========================
# st.subheader("📊 Insights")
#
# st.info("""
# - Random Forest captures complex patterns better using multiple decision trees
# - Logistic Regression is simpler and provides baseline predictions
# - High accuracy may indicate overfitting due to stock market noise
# - Using multiple models improves prediction reliability
# """)
#
# # =========================
# # 📌 Footer Note
# # =========================
# st.warning("⚠️ Model performance is based on historical data and may not reflect real-time market behavior.")
# st.subheader("📌 Final Conclusion")
#
# if rf_acc > lr_acc:
#     st.success("""
# ✅ Random Forest is the best model for this dataset.
#
# ✔ Captures complex patterns
# ✔ Higher accuracy and reliability
# ✔ Better suited for stock prediction
# """)
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, confusion_matrix,
    classification_report, precision_score,
    recall_score, f1_score
)

# ---------------- UI ----------------
st.set_page_config(page_title="Model Performance", layout="wide")

st.markdown("## 📈 StockSense AI")
st.caption("AI-powered stock prediction system")
st.title("📊 Model Performance Analysis")

# ---------------- LOAD ----------------
df = pd.read_csv("cleaned_apple_stock.csv")

features = [
    'close','volume','sma_50','ema_20','ema_50','rsi_14',
    'macd','macd_signal','macd_histogram','bb_width',
    'volatility_20d','close_lag_1','close_lag_5',
    'volume_lag_1','rsi_signal','macd_signal_cross',
    'momentum','trend_strength','price_change'
]

X = df[features]
y = df['target_direction']

lr_model = joblib.load("lr_model.pkl")
rf_model = joblib.load("rf_model.pkl")

lr_pred = lr_model.predict(X)
rf_pred = rf_model.predict(X)

# ---------------- METRICS ----------------
lr_acc = accuracy_score(y, lr_pred)
rf_acc = accuracy_score(y, rf_pred)

rf_precision = precision_score(y, rf_pred)
rf_recall = recall_score(y, rf_pred)
rf_f1 = f1_score(y, rf_pred)

cm = confusion_matrix(y, rf_pred)

report = classification_report(y, rf_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "📈 Metrics", "🔍 Confusion Matrix", "📄 Report & Insights"
])

# ================= OVERVIEW =================
with tab1:
    st.subheader("📊 Accuracy Comparison")

    col1, col2 = st.columns(2)

    col1.metric("Logistic Regression", f"{lr_acc*100:.2f}%")
    col2.metric("Random Forest", f"{rf_acc*100:.2f}%")

    # Best model
    st.subheader("🏆 Best Model")

    if rf_acc > lr_acc:
        st.success("Random Forest performs better")
    else:
        st.success("Logistic Regression performs better")

    if rf_acc > 0.90:
        st.warning("⚠️ High accuracy detected → possible overfitting")

# ================= METRICS =================
with tab2:
    st.subheader("📈 Advanced Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Precision", f"{rf_precision*100:.2f}%")
    col2.metric("Recall", f"{rf_recall*100:.2f}%")
    col3.metric("F1 Score", f"{rf_f1*100:.2f}%")

    st.info("""
    ✔ Precision → How accurate positive predictions are  
    ✔ Recall → How well model captures actual positives  
    ✔ F1 Score → Balance of precision & recall  
    """)

# ================= CONFUSION MATRIX =================
with tab3:
    st.subheader("🔍 Confusion Matrix")

    fig, ax = plt.subplots()
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=['Down', 'Up'],
        yticklabels=['Down', 'Up']
    )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    st.pyplot(fig)

    st.info("""
    📊 Interpretation:
    - True Positives → Correct UP predictions  
    - True Negatives → Correct DOWN predictions  
    - False Positives → Risky BUY signals  
    - False Negatives → Missed opportunities  
    """)

# ================= REPORT =================
with tab4:
    st.subheader("📄 Classification Report")

    st.dataframe(
        report_df.style.format("{:.2f}"),
        width='stretch'
    )

    st.subheader("📊 Insights")

    st.success("""
    ✔ Random Forest captures complex patterns  
    ✔ Logistic Regression acts as baseline  
    ✔ Ensemble comparison improves reliability  
    """)

    st.subheader("📌 Final Conclusion")

    if rf_acc > lr_acc:
        st.success("""
        ✅ Random Forest is the best model

        ✔ Higher accuracy  
        ✔ Better pattern recognition  
        ✔ More reliable predictions  
        """)

# ---------------- FOOTER ----------------
st.warning("⚠️ Based on historical data. Real market may differ.")
