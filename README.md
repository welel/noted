<p align="center"><a href="https://noted-eu.herokuapp.com/notes/"><img src="https://i.ibb.co/r3M4k7w/header-logo-noted.png" alt="header-logo-noted" border="0"></a></p>


<p align="center">This is a web service that helps to make and store notes.</p>

**Link on the website:** https://noted-eu.herokuapp.com/notes/



# Features

* Markdown editor
* Adaptive design (for mobile)
* Registration via django-allauth (github, yandex)
* Send emails (confirm registration)
* WYSIWYG editing
* Tagging
* Bootstrap integration
* Tree comments
* Search
* Recommendations
* Sharing content (facebook, twitter)
* Likes
* GitHub API Integration (markdown)


## Tech stack

<p>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/python/python-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/djangoproject/djangoproject-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/postgresql/postgresql-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/w3_html5/w3_html5-ar21.svg"></code><br/>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/netlifyapp_watercss/netlifyapp_watercss-ar21.svg"></code>
<code><img width="10%" src="https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-ar21.svg"></code>
      <code><img width="10%" src="https://www.vectorlogo.zone/logos/git-scm/git-scm-ar21.svg"></code>
  <code><img width="10%" src="https://www.vectorlogo.zone/logos/linux/linux-ar21.svg"></code><br/>
    <code><img width="10%" src="https://www.vectorlogo.zone/logos/github/github-ar21.svg"></code>
    <code><img width="10%" src="https://www.vectorlogo.zone/logos/gunicorn/gunicorn-ar21.svg"></code>
    <code><img width="10%" src="https://www.vectorlogo.zone/logos/heroku/heroku-ar21.svg"></code>
</p>



## Installation

1. [Install PostgreSQL](https://www.postgresql.org/download/) and create new database.

    To use trigrams in PostgreSQL, you will need to install the `pg_trgm`
    extension first. Execute the following command from the shell to connect to your
    database:
    `psql [db_name]`
    Then, execute the following command to install the `pg_trgm` extension:
    `CREATE EXTENSION pg_trgm;`

2. Clone repository.
   
4. Create virtual environment and activate it.

5. Install requirements from the file.

   `pip3 install -r requirements.txt`

6. Fill `.env_sample` with required data and rename the file to `.env`.

7. Make migrations.

8. Run the server `python3 manage.py runserver`.
