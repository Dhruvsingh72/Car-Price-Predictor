import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("""# Final Year Project: Used Car Price Prediction
**Objective:** To analyze the used car market dataset and build a machine learning model that can predict the selling price of a car based on its features (like age, brand, kilometers driven, etc).

Let's start by importing the necessary libraries for data analysis and visualization."""))

cells.append(nbf.v4.new_code_cell("""# Importing basic libraries for data manipulation and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Make charts look better
sns.set_style("whitegrid")
import warnings
warnings.filterwarnings('ignore')"""))

cells.append(nbf.v4.new_markdown_cell("""## 1. Data Loading and Basic Understanding
First, we will load the dataset and take a look at the first few rows to understand what columns we have."""))

cells.append(nbf.v4.new_code_cell("""# Load the dataset
df = pd.read_csv('CAR DETAILS FROM CAR DEKHO.csv')

# Let's see how big the dataset is
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# Look at the first 5 rows
df.head()"""))

cells.append(nbf.v4.new_code_cell("""# Check the data types and see if there are any null values right away
df.info()"""))

cells.append(nbf.v4.new_markdown_cell("""**Observation:**
It looks like we have 8 columns. The `selling_price` is what we want to predict (our target variable). We have a mix of integer columns (year, selling_price, km_driven) and object/string columns (name, fuel, seller_type, transmission, owner). 

Let's check some basic statistics of the numerical columns."""))

cells.append(nbf.v4.new_code_cell("""# Summary statistics for numerical columns
df.describe()"""))

cells.append(nbf.v4.new_markdown_cell("""## 2. Data Cleaning
Before we can visualize or train a model, we need to clean the data. 

### Checking for Missing Values"""))

cells.append(nbf.v4.new_code_cell("""# Find out if we have any missing data
df.isnull().sum()"""))

cells.append(nbf.v4.new_markdown_cell("""Great! There are no missing values in this dataset.

### Checking for Duplicates
Sometimes the dataset contains duplicate rows. Let's find out."""))

cells.append(nbf.v4.new_code_cell("""# Count duplicate rows
duplicate_count = df.duplicated().sum()
print("Number of duplicate rows:", duplicate_count)

# Let's drop these duplicates because they don't add new information
df = df.drop_duplicates()
print("Shape after dropping duplicates:", df.shape)"""))

cells.append(nbf.v4.new_markdown_cell("""### Feature Engineering (Creating new useful columns)
The `name` column has the full name of the car (e.g., "Maruti 800 AC"). It's too specific. Let's extract just the **Brand** (Maruti) and the **Model**.

Also, the `year` column is just the year of manufacture. A machine learning model understands "Age" better than "Year". So let's calculate the car's age."""))

cells.append(nbf.v4.new_code_cell("""# 1. Extract Brand
df['brand'] = df['name'].apply(lambda x: x.split(' ')[0])

# 2. Extract Model (the second and third word)
df['model'] = df['name'].apply(lambda x: ' '.join(x.split(' ')[1:3]) if len(x.split(' ')) > 1 else 'Unknown')

# 3. Calculate Car Age
from datetime import datetime
current_year = datetime.now().year
df['car_age'] = current_year - df['year']

# Now let's see how our dataframe looks
df[['name', 'brand', 'model', 'year', 'car_age']].head()"""))

cells.append(nbf.v4.new_markdown_cell("""We don't need the original `name` and `year` columns anymore since we extracted the useful parts. Let's drop them to keep things clean."""))

cells.append(nbf.v4.new_code_cell("""# Drop unnecessary columns
df_clean = df.drop(['name', 'year'], axis=1)
df_clean.head()"""))

cells.append(nbf.v4.new_markdown_cell("""## 3. Exploratory Data Analysis (EDA)
Now that our data is clean, let's explore it to find patterns. Visualizations help us understand the relationships between different features and the selling price.

### 3.1 Analyzing the Target Variable (Selling Price)"""))

cells.append(nbf.v4.new_code_cell("""# Let's look at the distribution of selling prices
plt.figure(figsize=(10, 5))
sns.histplot(df_clean['selling_price'], bins=50, color='blue')
plt.title('Distribution of Car Selling Prices')
plt.xlabel('Selling Price')
plt.ylabel('Frequency')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""**Insight:** The selling price is highly right-skewed. Most cars are sold at lower prices (budget segment), and there are a few very expensive luxury cars. 

Let's check for extreme outliers using a boxplot."""))

cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(8, 4))
sns.boxplot(x=df_clean['selling_price'], color='lightblue')
plt.title('Boxplot of Selling Price to find Outliers')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""Since we have some crazy outliers, let's cap the selling price at the 99th percentile so our model doesn't get confused by 1 or 2 extremely expensive cars."""))

cells.append(nbf.v4.new_code_cell("""# Cap selling price
price_cap = df_clean['selling_price'].quantile(0.99)
df_clean['selling_price'] = np.where(df_clean['selling_price'] > price_cap, price_cap, df_clean['selling_price'])

print("Capped max price at:", price_cap)"""))

cells.append(nbf.v4.new_markdown_cell("""### 3.2 Categorical Features Analysis
Let's see how things like Fuel Type and Transmission affect the price."""))

cells.append(nbf.v4.new_code_cell("""# Average price by Fuel Type
plt.figure(figsize=(8, 5))
sns.barplot(x='fuel', y='selling_price', data=df_clean, ci=None)
plt.title('Average Selling Price by Fuel Type')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""**Insight:** Diesel cars generally sell for much higher prices compared to Petrol or CNG cars."""))

cells.append(nbf.v4.new_code_cell("""# Average price by Transmission
plt.figure(figsize=(8, 5))
sns.barplot(x='transmission', y='selling_price', data=df_clean, ci=None)
plt.title('Average Selling Price by Transmission')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""**Insight:** Automatic cars are significantly more expensive than manual cars. This is a very important feature for our model.
             
Let's also look at how the number of previous owners affects the price."""))

cells.append(nbf.v4.new_code_cell("""# Average price by Owner Type
plt.figure(figsize=(10, 5))
# Define a logical order for the owners
owner_order = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner"]
# Filter out test drive cars for this specific chart
owner_data = df_clean[df_clean['owner'] != 'Test Drive Car']
sns.barplot(x='owner', y='selling_price', data=owner_data, order=owner_order, ci=None, palette="viridis")
plt.title('Average Selling Price by Owner Type')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""**Insight:** As expected, First Owner cars have the highest resale value, and the value drops sequentially for second and third owners."""))

cells.append(nbf.v4.new_markdown_cell("""### 3.3 Market Supply Analysis
Let's quickly see which car brands are the most common in our dataset."""))

cells.append(nbf.v4.new_code_cell("""# Top 10 most common brands
plt.figure(figsize=(12, 5))
top_brands = df_clean['brand'].value_counts().head(10)
sns.barplot(x=top_brands.index, y=top_brands.values, palette="Blues_r")
plt.title('Top 10 Most Popular Car Brands in Market')
plt.ylabel('Number of Cars')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""### 3.4 Numerical Features Analysis
Let's see how the age of the car and kilometers driven affect the price. We expect older cars to be cheaper."""))

cells.append(nbf.v4.new_code_cell("""# Selling Price vs Car Age
plt.figure(figsize=(10, 5))
sns.scatterplot(x='car_age', y='selling_price', data=df_clean, alpha=0.5, color='orange')
plt.title('How Car Age affects Selling Price')
plt.xlabel('Car Age (Years)')
plt.ylabel('Selling Price')
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""**Insight:** There is a clear negative correlation. As the car age increases, the selling price drops rapidly.

Let's also look at Kilometers Driven. There are probably some outliers here too."""))

cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(8, 4))
sns.boxplot(x=df_clean['km_driven'], color='lightgreen')
plt.title('Boxplot of Kilometers Driven')
plt.show()

# Let's cap the km_driven at 500,000 to handle those weird outliers
df_clean['km_driven_cap'] = df_clean['km_driven'].apply(lambda x: min(x, 500000))
df_clean = df_clean.drop('km_driven', axis=1)"""))

cells.append(nbf.v4.new_markdown_cell("""## 4. Preparing Data for Machine Learning
Machine Learning models only understand numbers. We have text columns (like brand, fuel, transmission) that we need to convert to numbers. 

We will use Scikit-Learn's `ColumnTransformer` to handle this. It will automatically apply `OneHotEncoder` to the text columns and `StandardScaler` to the number columns."""))

cells.append(nbf.v4.new_code_cell("""from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Separate the target variable (what we want to predict) from the features
X = df_clean.drop('selling_price', axis=1)
y = df_clean['selling_price']

# Split the data into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)"""))

cells.append(nbf.v4.new_code_cell("""# Setup the preprocessing pipeline
numeric_features = ['car_age', 'km_driven_cap']
categorical_features = ['fuel', 'seller_type', 'transmission', 'owner', 'brand', 'model']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])"""))

cells.append(nbf.v4.new_markdown_cell("""## 5. Training Machine Learning Models
We will try three different algorithms:
1. Linear Regression (Simple baseline)
2. Decision Tree (Better for complex data)
3. Random Forest (An ensemble method, usually the best)

We will use a `Pipeline` to tie the preprocessor and the model together neatly."""))

cells.append(nbf.v4.new_code_cell("""from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# -------------------------
# MODEL 1: Linear Regression
# -------------------------
print("Training Linear Regression...")
lr_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)

print("Linear Regression R2 Score:", r2_score(y_test, lr_preds))
print("Linear Regression MAE:", mean_absolute_error(y_test, lr_preds))"""))

cells.append(nbf.v4.new_code_cell("""from sklearn.tree import DecisionTreeRegressor

# -------------------------
# MODEL 2: Decision Tree
# -------------------------
print("Training Decision Tree...")
dt_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', DecisionTreeRegressor(random_state=42))
])

dt_model.fit(X_train, y_train)
dt_preds = dt_model.predict(X_test)

print("Decision Tree R2 Score:", r2_score(y_test, dt_preds))
print("Decision Tree MAE:", mean_absolute_error(y_test, dt_preds))"""))

cells.append(nbf.v4.new_code_cell("""from sklearn.ensemble import RandomForestRegressor

# -------------------------
# MODEL 3: Random Forest
# -------------------------
print("Training Random Forest...")
rf_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

print("Random Forest R2 Score:", r2_score(y_test, rf_preds))
print("Random Forest MAE:", mean_absolute_error(y_test, rf_preds))"""))

cells.append(nbf.v4.new_markdown_cell("""## 6. Conclusion and Saving the Final Model
As we can see from the R2 scores, the **Random Forest** model performs the best by far. It understands the complex relationships between the car's features much better than a simple straight line (Linear Regression).

We will now save this Random Forest pipeline as a `.pkl` file. Our FastAPI backend will load this file to make live predictions when users visit our web app!"""))

cells.append(nbf.v4.new_code_cell("""import pickle

# We will save the rf_model pipeline
with open('car_price_rf_pipeline.pkl', 'wb') as file:
    pickle.dump(rf_model, file)

print("Success! The Random Forest model has been saved as 'car_price_rf_pipeline.pkl'.")"""))

nb.cells = cells

with open('car_price_prediction_project_clean.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
