# What is this?

This repo shows how to set up the Channels structure with a chat application without an interface. In this structure, redis backend service is used.
<br><br><br>
<b>Custom development</b><br>
By default, Channels supports Django's session-based authentication structure, but special middleware has been written for token-based authentication used for restframework here.

## Installation

1. Clone the repository
2. Install redis in your computer and start redis
3. Install required packages
   ```
   pip3 install django
   pip3 install django-redis
   pip3 install channels
   pip3 install channels-redis
   pip3 install djangorestframework
   ```





## Usage

You can review the document I described Channels for use.<br>
[Medium Document](https://tarkkabasakal.medium.com/python-django-ile-channels-kullan%C4%B1m%C4%B1-6797928087b8)



## License
[MIT](https://choosealicense.com/licenses/mit/)
