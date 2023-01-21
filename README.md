<p align="center"><a href="https://welel-noted.site/"><img src="frontend/static/img/noted_logo2.png" alt="header-logo-noted" width="210" border="0"></a></p>

<hr>
<p>
  <img src="https://img.shields.io/badge/python-v3.8-blue" >
  <img src="https://img.shields.io/badge/django-v4.1-blue">
  <img src="https://img.shields.io/badge/code%20style-black-black">
</p>

<h3 align="center">The website helps to make, store, search and share notes.</h3>

This website helps to create personal notes, share them public, search for notes on a specific information source or interesting topics and save them, follow users and be followed by others. The project was created for my educational purposes, but has a practical application.

<p align="center"><a href="https://welel-noted.site/"><img src="https://i.ibb.co/JxX9Tqm/screely-1671564299536.png" alt="NoteD."  border="0" /></a></p>

**Link on the website:** https://welel-noted.site/

</br>

## 🔍 About

**The goal of the project is to develop a system for creating, storing notes and searching for notes by sources of information.**

A note is a summary of some material, for example: a book, video, course, article, etc. A source is a some information material.
The user can search for public notes or notes by the name of the Source. The user can create public notes and drafts, subscribe to other users.

**The benefit of this project** is that a person studying any material reduces the time for taking notes. 

Users can:
- look for notes of other people;
- start writing notes from other people's notes;
- to study the material in a short form, according to other people's notes;
- skimming over existing notes to find a Source to study something
- etc.

<p align="center"><img src="https://i.ibb.co/rtX98KM/screely-1671564311882.png" alt="NoteD. Home"  border="0" /></p>


**Main useful features**:

- Create public notes (and drafts)
- Create a note on a specific source
- Copy (fork) and edit other's notes
- Search notes
- Search notes by a specific source
- Search for sources and list of notes on them
- Download notes [md, pdf, html]

**Additional features**:

- Add tags to notes
- Search notes by tags
- Subscribe to tags
- Follow users
- Pin your important notes
- Add notes to bookmarks

<p align="center"><img src="https://i.ibb.co/FY8JrJw/screely-1671564251678.png" alt="NoteD. Form"  border="0" /></p>

Notes are created in the markdown editor. The editor supports preview, split editing, full screen editing, hotkeys.

Dark mode / code highlight / code full-screen / mobile version.

<p>
  <code><img width="40%" src="https://i.ibb.co/zR73qnJ/screely-1671641709714.png"></code>
  <code><img width="40%" src="https://i.ibb.co/QJCZk42/screely-1671564364437.png"></code>
  <br>
  <code><img width="40%" src="https://i.ibb.co/JRmRVjF/screely-1671630742282.png"></code>
  <code><img width="40%" src="https://i.ibb.co/86NxJQ4/screely-1671630946911.png"></code>
    <br>
  <code><img width="35%" src="https://i.ibb.co/fvGJFwN/Screen-Shot-2022-12-21-at-19-46-17-iphone13pink-portrait.png"></code>
  <code><img width="35%" src="https://i.ibb.co/Vx7scdn/Screen-Shot-2022-12-21-at-19-46-51-iphone13blue-portrait.png"></code>
</p>


## 🔥 Features

* Registration, authentication, authorization
  * with socials (google, github, yandex)
* WYSIWYG Markdown editing
* Internationalization (English, Russian)
* User profile
* Following system
* Tagging
* Search
* Bookmarks
* Likes
* Sharing content (twitter, whatsapp, telegram)
* Download posts (md, pdf, html)
* Twitter Bootstrap integration
* Responsive (modile) design
* Dark mode
* Code documentation
* GitHub API Integration (markdown)

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
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/linux/linux-ar21.svg"></code></br>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/nginx/nginx-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/gunicorn/gunicorn-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/docker/docker-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/jenkins/jenkins-ar21.svg"></code><br/>
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

5. Make migrations and migrate with a custom command.

```
python manage.py makemigrate
```

6. [Set up a cache backend.](https://docs.djangoproject.com/en/4.1/topics/cache/)

7. Run the development server.

```
python manage.py runserver
```


</br>

### 👨‍💻 Team

- [Pavel Loginov](https://github.com/welel) (Backend/Frontend)
- [Eduard Antadze](https://github.com/eantdz) (DevOps)
