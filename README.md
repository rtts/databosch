# Databosch

***Django apps that power various public initiatives in ’s-Hertogenbosch***

## Introduction

This repository contains various loosely related Django apps, each with a specific purpose:

<dl>
  <dt>effect</dt>
  <dd>The code that runs [the website of Effect Festival](https://www.effectfestival.nl/)</dd>
  <dt>jadb</dt>
  <dd>Development of a plugin for [Jongeren Ambassadeurs](https://www.jadb.nl/netwerk/)</dd>
  <dt>maakdenbosch</dt>
  <dd>This is the core of Databosch, containing various interesting models and admins (of which the most mysterious one is *Entity*)</dd>
  <dt>mijndenbosch</dt>
  <dd>The code that runs the [MijnDenBosch website](https://www.mijndenbosch.nl/)</dd>
  <dt>rauwkost</dt>
  <dd>The code that runs the [Rauwkost website](https://www.rauwkost.online/)</dd>
</dl>

## Installation

You can install everything [the usual Python
way](https://packaging.python.org/tutorials/installing-packages/). It
should be as simple as running the following commands:

    git clone https://github.com/rtts/databosch
    cd databosch
    python3 -m venv ~/.virtualenvs/databosch
    source ~/.virtualenvs>/bin/activate
    pip install -r requirements.txt

Alright, it should actually even be simpler:

    pip3 install https://github.com/rtts/databosch

But doing it that way won't install the specific dependencies listed
in `requirements.txt`. So I recommend the first way :-)

After installation, you can use the various [Django management
commands](https://docs.djangoproject.com/en/dev/ref/django-admin/) to
setup a database and run a development server.
