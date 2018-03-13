rm db.sqlite3
python manage.py migrate --noinput
echo "Recreated the database."
