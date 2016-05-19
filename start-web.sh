cd jspagecrawler
node crawler.js 10 0.0.0.0 10080 &
cd ..
python manage.py runserver 0.0.0.0:8080 &