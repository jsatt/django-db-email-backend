Change Log
==========


Under development
~~~~~~~~~~~~~~~~~~
*

2023.02.08 v05.9
~~~~~~~~~~~~~~~~
* Adds arabic translation; Mark strings are translatable.
* Adds check for change permission to send email from admin

2022.07.19 v05.7
~~~~~~~~~~~~~~~~
* Adds `DB_EMAIL_FILTER_FUNCTION_PATH` setting to allow filtering out email from DB recording.
* Enhances in read me and strings translations.

2022.07.18 v05.5
~~~~~~~~~~~~~~~~
* Fixes issues in case of error sending the mail.

2022.04.21 v05.4
~~~~~~~~~~~~~~~~
* Adds `SMTP_EMAIL_FILTER_FUNCTION_PATH` setting to allow filtering out email from smtp sending.
* Enhance apps
* Rename has_error to succeeded for clearer more relaxed visual


2022.04.20 v05.1
~~~~~~~~~~~~~~~~
* Adds `SMTPDBEmailBackend` , a mixture between SMTP and DB mail backend.
* Remove south migrations
* Allow only superusers to access email body.
* Adds has_error, and error ro Email model


2021.11.29
~~~~~~~~~~
* Upgrade compatibility from the main fork to work with Django 3.2 +
* Add option on admin to (re)send the mail using the smtp backend