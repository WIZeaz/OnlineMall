python3 manage.py makemigrations
python3 manage.py migrate
nohup python3 manage.py runserver_plus --cert server.crt 0.0.0.0:443 > server.stdout 2> server.stderr & disown
