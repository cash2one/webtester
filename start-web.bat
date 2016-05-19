cd jspagecrawler
start node crawler.js 10 0.0.0.0 10080
cd ..
start celery -A webtester worker
python manage.py runserver 0.0.0.0:8080