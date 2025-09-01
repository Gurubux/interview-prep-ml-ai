# 🛠️ Feature Engineering

This section covers **feature engineering techniques** essential for building robust ML models.  
Each topic will include **theory notes**, **Jupyter notebooks**, and/or **Streamlit demos**.  

---

## 📂 Index  

### 1. Feature Generation & Transformation  
- [Polynomial & interaction features](#)  
- [Datetime features (weekday, month, season, cyclic encoding)](#)  
- [Text features (TF-IDF, bag-of-words, embeddings)](#)  
- [Domain-specific features (healthcare, finance, retail)](#)  

---

### 2. Feature Scaling  
- [Normalization](#)  
- [Standardization](#)  
- [Log scaling](#)  
- [MinMaxScaler](#)  
- [RobustScaler](#)  
- [Power transforms (Box-Cox, Yeo-Johnson)](#)  
- [QuantileTransformer (uniform, normal)](#)  

---

### 3. Feature Selection  
- **Filter methods**  
  - [Chi-square](#)  
  - [Correlation](#)  
- **Wrapper methods**  
  - [RFE (Recursive Feature Elimination)](#)  
- **Embedded methods**  
  - [L1/L2 regularization](#)  
  - [Tree-based feature importance](#)  
  - [SHAP values](#)  
- **Dimensionality reduction**  
  - [PCA](#)  
  - [t-SNE](#)  
  - [UMAP](#)  

---

### 4. Encoding Categorical Features  
- [One-hot encoding](#)  
- [Label encoding](#)  
- [Target encoding](#)  
- [Hashing trick](#)  
- [Frequency encoding](#)  
- [CatBoost encoding](#)  
- [Embeddings](#)  
- [Cyclical encoding (time features) ✅](https://github.com/Gurubux/interview-prep-ml-ai/blob/main/05_Feature_Engineering/notebooks/Encoding/feature_encoding_cyclic_notebook.ipynb)  

---

### 5. Imputation (Missing Values)  
- [Mean/Median/Mode](#)  
- [KNN imputer](#)  
- [MICE (Iterative imputer)](#)  
- [Group-based imputation](#)  
- [Forward/Backward fill](#)  

---

### 6. Feature Augmentation  
- [SMOTE & its variants](#)  
- [GANs for tabular/text/image](#)  
- [Image augmentation (flip, crop, noise)](#)  
- [Time-series augmentation (jittering, window slicing, mixup)](#)  

---

### 7. Feature Stores & Tools  
- [Feast](#)  
- [Tecton](#)  
- [Databricks Feature Store](#)  
- [Featuretools](#)  
  - [Deep Feature Synthesis (DFS)](#)  
  - [Feature primitives](#)  
- [Versioning & lineage](#)  

---

## 🚀 Usage Plan  

- Each link (`[#]`) will be replaced with **Jupyter notebooks, Streamlit demos, or notes**.  
- Practical examples:  
  - Polynomial features with `PolynomialFeatures` in scikit-learn  
  - PCA vs t-SNE visualization on MNIST  
  - One-hot vs Target encoding comparison on categorical datasets  
  - Imputation strategies with KNN & MICE  
  - SMOTE vs GANs for imbalanced classification  
  - Setting up a **Feature Store** with Feast  

---

## 🏆 Goal  

- Gain mastery in **feature creation, scaling, selection, encoding, and augmentation**.  
- Understand and implement **feature stores** for production ML pipelines.  
- Build a **portfolio of hands-on notebooks** to reference in interviews.  

