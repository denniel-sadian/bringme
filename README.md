# BringMe
A Django project where regular users can post the items they want and have the riders deliver their items to them. A project of Mr. Sadian and Ms. Lastica.

You must have a Linux environment. WSL will work just fine. You must have git installed and configured. You must have MailHog. And, of course, Python3.
How to setup locally:

1. `mkdir bringme`
2. `cd bringme`
3. `git clone https://github.com/denniel-sadian/bringme.git .`
4. `pip install -r requirements.txt`
5. `python manage.py migrate`

Make `bringme/.env`:
```
SECRET_KEY="Sorry, by the secret key is not provided here. Just make your test secret key."
PORT="8080"
DEFAULT_FROM_EMAIL="ladygaga@example.com"
DEBUG="true"
```

Start the server by doing: `honcho start`
