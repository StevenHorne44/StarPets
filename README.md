# ⭐🐾 StarPets

** For pet lovers **

---

## 🚀 Getting started 

### 1. Clone the Repoitory 
Open terminal and run: 
```bash
git clone https://github.com/StevenHorne44/StarPets.git
cd StarPets
```

### 2. Set up virtual environment 

```bash
conda create -n starpets_env python=3.11 -y
```
 
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Initialization
```bash
python manage.py migrate 
python manage.py createsuperuser
```

### 5. Populate database 
```bash
python populate_script.py
```

### 6. Launch the server 
```bash
python manage.py runserver
```

## ✨ Key Features

* Pet Discovery and browsing with our category filtering page and out highest rated pets in the community 
* User Experience with personal profiles, secure authentication and personal bookmarks 
* Content management with pet uploads so users can easily add their pets and store a photo and bio with it
* Page is easy to naviagate with clear and bright button for the best user experience 

## Built with 

* Python (Django): The backbone of the project, handling the database logic, user authentication, and star-rating signals.
* HTML: Structured the various pages, from the pet gallery to user profiles.
* CSS: Custom styling to ensure the "StarPets" branding is consistent and clean.
* JavaScript: Enhances the user experience with interactive elements and dynamic button behaviors.
* SQLite: Our development database for storing pet info and user data

## 👥 Contributors 
* **Steven Horne**
* **Alexander Duncan**
* **Vova Voloven**
* **Olivia Swinbank**
* **Julia Leeb**

