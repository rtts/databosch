# Databosch

***Django apps for various public initiatives in ’s-Hertogenbosch***

![Screenshot of www.rauwkost.online](2020.png)

## Introduction

This repository contains various loosely related Django apps:

<dl>
  <dt>effect</dt>
  <dd>The code that (used to) power https://www.effectfestival.nl/<br>
  An archive will remain available at https://effect.created.today/</dd>
  <dt>jadb</dt>
  <dd>Development of a plugin for https://www.jadb.nl/</dd>
  <dt>maakdenbosch</dt>
  <dd>The core of Databosch, containing all models shared between these websites.</dd>
  <dt>mijndenbosch</dt>
  <dd>The code that (used to) power https://www.mijndenbosch.nl/<br>
  An archive will remain available at https://mijndenbosch.created.today/</dd>
  <dt>rauwkost</dt>
  <dd>The code that (used to) power https://www.rauwkost.online/<br>
  Archives will remain available at
  <ul>
    <li>https://rauwkost.created.today/2018/
    <li>https://rauwkost.created.today/2019/
    <li>https://rauwkost.created.today/2020/
  </ul></dd>
</dl>

## Installation

Install Python and run the following commands:

    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

This will make the Django admin that is shared between all these
websites available at http://localhost:8000/
