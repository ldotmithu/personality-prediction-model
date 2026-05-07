# 🧠 Personality Prediction System using Machine Learning

A machine learning-based web service that predicts whether a person is an **Introvert or Extrovert** based on behavioral and social activity features.  
The project includes **data preprocessing, EDA, model training, hyperparameter tuning, and deployment using FastAPI**.

---

## 🚀 Project Overview

This project analyzes human behavioral patterns such as:
- Time spent alone
- Social event attendance
- Friends circle size
- Social media activity
- Stage fear and emotional response

Using these features, the system predicts personality type:
- **0 → Introvert**
- **1 → Extrovert**

---

## 📊 Dataset Features

| Feature | Description |
|--------|-------------|
| Time_spent_Alone | Hours spent alone |
| Stage_fear | Fear of public speaking (Yes/No) |
| Social_event_attendance | Number of social events attended |
| Going_outside | Frequency of going outside |
| Drained_after_socializing | Feeling tired after socializing (Yes/No) |
| Friends_circle_size | Number of close friends |
| Post_frequency | Social media posting frequency |
| Personality | Target variable |

---

## 🧹 Data Preprocessing

- Handled missing values using **median (numeric)** and **mode (categorical)**
- Encoded categorical variables using **Label Encoding**
- Checked and confirmed **no significant outliers**
- Feature scaling using **StandardScaler**

---

## 📈 Exploratory Data Analysis (EDA)

- Distribution analysis using histograms and KDE plots
- Class balance visualization
- Correlation analysis
- Skewness detection

---

## 🤖 Machine Learning Models

The following models were trained:

- XGBoost Classifier (Best Model)

---

## ⚙️ Model Optimization

- Hyperparameter tuning using **GridSearchCV**
- Improved accuracy from ~92% → **92.93%**
- Cross-validation used for stability

---

## 🏆 Final Model Performance

| Metric | Score |
|------|------|
| Accuracy | 92.93% |
| Precision | 0.93 |
| Recall | 0.93 |
| F1-score | 0.93 |

---

## 📦 Tech Stack

- Python 🐍
- Pandas & NumPy
- Scikit-learn
- XGBoost
- Matplotlib & Seaborn
- FastAPI
- Joblib

---

## 🌐 API Deployment (FastAPI)

### Run the API locally:

```bash
uvicorn backend.main:app --reload
```

```bash
streamlit run frontend\app.py
```