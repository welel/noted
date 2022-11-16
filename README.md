<p align="center"><a href="https://noted-eu.herokuapp.com/notes/"><img src="frontend/static/img/noted_logo2.png" alt="header-logo-noted" width="350" border="0"></a></p>

<hr>
<p>
  <img src="https://img.shields.io/badge/python-v3.8-blue" >
  <img src="https://img.shields.io/badge/django-v3.2-blue">
</p>

<h3 align="center">This is a web service that helps to make, store and share notes.</h3>

This website helps to create personal notes, share them public, search notes for interesting topics and save them, follow users and be followed by others. The project was created for my educational purposes. 

<p align="center"><a href="https://noted-eu.herokuapp.com/"><img src="https://s4.gifyu.com/images/ezgif.com-gif-makerd1278193c866c2fa.gif" alt="ezgif.com-gif-makerd1278193c866c2fa.gif"  border="0" /></a></p>

**Link on the website:** https://noted-eu.herokuapp.com/notes/


</br>
## 🔥 Features

* Markdown editor
* WYSIWYG editing
* GitHub API Integration (markdown)
* Registration via django-allauth (github, yandex)
* User profile
* Following system
* Sharing content (facebook, twitter)
* Tagging
* Search
* Bookmarks
* Likes
* Recommendations
* Tree comments
* Send emails (confirm registration)
* Bootstrap integration
* Code documentation
* Adaptive design (for mobile)

</br>
## 🛠️ Tech stack

<p>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/python/python-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/djangoproject/djangoproject-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/postgresql/postgresql-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-ar21.svg"></code><br/>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/netlifyapp_watercss/netlifyapp_watercss-ar21.svg"></code>
<code><img width="10%" src="https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-ar21.svg"></code>
      <code><img width="10%" src="https://www.vectorlogo.zone/logos/git-scm/git-scm-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/linux/linux-ar21.svg"></code>
</p>


</br>
## 🏗️ Installation

1. [Install PostgreSQL](https://www.postgresql.org/download/) and create new database.

    To use trigrams in PostgreSQL, you will need to install the `pg_trgm`
    extension first. Execute the following command from the shell to connect to your
    database:
    `psql [db_name]`
    Then, execute the following command to install the `pg_trgm` extension:
    `CREATE EXTENSION pg_trgm;`

2. Clone or download the repository.
   
3. Create [virtual environment and install requirements](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) from `requirements.txt`.

4. Fill `env_sample` file with required data and rename it to `.env`.

5. Make migrations and migrate.

6. Run the server `python manage.py runserver`.


</br>
### 👨‍💻 Team

- [Pavel Loginov](https://github.com/welel) (Backend/Frontend)
- [Eduard Antadze](https://github.com/eantdz) (DevOps)
