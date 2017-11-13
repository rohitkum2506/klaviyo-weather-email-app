sudo apt-get install git-all
git clone "https://github.com/rohitkum2506/klaviyo-weather-email-app.git"
mv klaviyo-weather-email-app klaviyo
docker build -t rohit/dockertest .
docker run -it -p 8000:8000 rohit/dockertest

