# Netflix Movies and TV Shows Data Analysis and Web Application

## Overview
This project is a data analysis and web application built with Python and Django, focusing on Netflix Movies and TV Shows. It provides insights into Netflix's content library through data analysis and interactive visualizations.

## Features
- **Data Analysis & Visualization**: Uses Pandas, NumPy, and Matplotlib to analyze and visualize Netflix data.
- **Django Web Application**: Displays analyzed data with interactive charts.
- **Search & Filtering**: Users can search for titles and filter data by category, country, or director.
- **Database Integration**: Stores cleaned Netflix data using Django models.

---

## Setup Instructions

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/netflix_analysis_project.git
cd netflix_analysis_project
```

### **2. Set Up Virtual Environment**
```bash
python -m venv venv
# Activate virtual environment (Windows)
venv\Scripts\activate
# Activate virtual environment (Mac/Linux)
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Download Dataset**
- Visit Kaggle and download the "Netflix Movies and TV Shows Dataset".
- Save the file inside the `data/` folder.

### **5. Run Data Analysis**
```bash
python analysis/netflix_analysis.py
```
This script:
- Loads and cleans the dataset.
- Performs exploratory analysis.
- Generates visualizations.
- Saves cleaned data for the web application.

### **6. Set Up Django Project**
```bash
django-admin startproject netflix_project .
python manage.py startapp netflix_app
```
Update `settings.py` to include `netflix_app` and configure SQLite as the database.

### **7. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **8. Import Cleaned Data into Django Models**
```bash
python manage.py import_netflix_data data/netflix_titles.csv
```

### **9. Start the Development Server**
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/` to view the web application.

---

## Project Structure
```
netflix_analysis_project/
|
analysis/
data/
netflix_project/
├── netflix_project/
|   |-- __pycache__
│   ├── __init__.py
|   |-- asgi
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── netflix_app/
|   |---__pycache__
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
|   |---tests.py
|   |---management
|   |---migrations
│   └── templates/
│       └── netflix_app/
│           ├── base.html
│           ├── home.html
|           |-- title_detail.html
│           ├── title_list.html
│           ├── country_analysis.html
│           ├── director_analysis.html
│           ├── year_analysis.html
│           ├── category_analysis.html
│           ├── search.html
|-- db.sqlite3
├── manage.py
venv/
netflix_analysis_results.png
README.md
report.txt
reqirements.txt
```

---

## Usage
- **Home Page**: Displays general insights and visualizations.
- **Title List**: Browse all Netflix content.
- **Search Functionality**: Find specific movies and TV shows.
- **Category, Release Year & Country Analysis**: View statistics based on content categories, release year and regions.
- **Director Analysis**: Analyze top directors featured on Netflix.

---

## Technologies Used
- **Backend**: Django (Python)
- **Data Analysis**: Pandas, NumPy, Matplotlib
- **Frontend**: Bootstrap, HTML, CSS
- **Database**: SQLite

---

## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Commit changes: `git commit -m 'Add new feature'`.
4. Push to branch: `git push origin feature-branch`.
5. Submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For any inquiries or support, feel free to reach out at email@gmail.com.

