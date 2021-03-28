Redmine wiki to Wiki.js migrator
================================



Migrate wiki from Redmine to Wiki.js

Does
----

- Per-project migrations
- Migration of wiki pages including history:
  - versions become older commits
  - author names (without email addresses!) are the author/committer names

Requires
--------

- Python >= 3.5
- redmine >= 1.3
- pandoc >= 1.17.0.0
- API token on redmine
- API token on Wiki.js



## Installing Python & pip

https://docs.python-guide.org/starting/installation/

    apt-get install python3

    apt-get install python3-pip

## Python Virtual Envs (optional)

* https://docs.python-guide.org/dev/virtualenvs/

    apt-get install python3

## VSCode 

* https://code.visualstudio.com/docs/python/python-tutorial
* https://code.visualstudio.com/docs/python/environments

## Install module

    python3 setup.py develop

    python3 setup.py install


## Install pandoc

    apt-get install pandoc


## Launch

    mkdir tmp

    git init tmp

    redmine2wikijs pages --wikijs-url <wiki.js graphql endpoint> --wikijs-key <wiki.js key> \
      --redmine-key <redmine api key> --no-history --gitlab-wiki tmp  <redmine project url>

Let's go (OLD)
---------------

You can or can not use
[virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/), that's
up to you.

Install it:

    pip install redmine-gitlab-migrator

or latest version from GitHub:

    pip install git+https://github.com/redmine-gitlab-migrator/redmine-gitlab-migrator

or if you cloned the git:

    python setup.py install

You can then give it a check without touching anything:

    migrate-rg issues --redmine-key xxxx --gitlab-key xxxx \
      <redmine project url> <gitlab project url> --check

The `--check` here prevents any writing , it's available on all
commands.

    migrate-rg --help

Migration process
-----------------

### Migrate wiki pages

First, clone the GitLab wiki repository (go to your project's Wiki on GitLab,
click on "Git Access" and copy the URL) somewhere local to your machine. The
conversion process works even if there are pre-existing wiki pages, however
this is NOT recommended.

    migrate-rg pages --redmine-key xxxx --gitlab-wiki xxxx \
      https://redmine.example.com/projects/myproject \

where gitlab-wiki should be the path to the cloned repository (must be local
to your machine). Add "--no-history" if you do not want the old versions of
each page to be converted, too.

After conversion, verify that everything is correct (a copy of the original
wiki page is included in the repo, however not added/committed), and then
simply push it back to GitLab.

Unit testing
------------

Use the standard way:

    python setup.py test

Or use whatever test runner you fancy.

Using Docker container (TODO)
-----------------------------

### Start up GitLab with migrator

cf. [GitLab Docs](https://docs.gitlab.com/) > Omnibus GitLab Doc > [GitLab Docker images](https://docs.gitlab.com/omnibus/docker/)

    export GITLAB_HOME=$PWD/srv/gitlab
    docker-compose up -d
    docker-compose logs -f  # You can watch logs and stop with Ctrl+C

After starting a container you can access GitLab http://localhost:8081

- Create group/project and users
- Create Access Token

### Migrate with docker-compose command

#### Roadmap

    docker-compose exec migrator \
      migrate-rg roadmap --redmine-key xxxx --gitlab-key xxxx \
      https://redmine.example.com/projects/myproject \
      http://localhost:8081/mygroup/myproject

#### Issues

    docker-compose exec migrator \
      migrate-rg issues --redmine-key xxxx --gitlab-key xxxx \
      https://redmine.example.com/projects/myproject \
      http://localhost:8081/mygroup/myproject

#### Issues ID (iid)

    docker-compose exec migrator \
      migrate-rg iid --gitlab-key xxxx \
      http://localhost:8081/mygroup/myproject

### Export/Import to production system

cf. GitLab Docs
GitLab Docs > User Docs > Projects > Project settings > [Project import/export](https://docs.gitlab.com/ee/user/project/settings/import_export.html)

Credits
----------------------
Many thanks to the @oasiswork team for the good work they have done with the project redmine-gitlab-migrator on which this project is based on.
