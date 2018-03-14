clear; python manage.py test $1 2>&1 |grep -v $VENV_ROOT
