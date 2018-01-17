DATE=$(date +"%H")
if [ "$DATE" -ge 9 -a "$DATE" -le 19 ]
  then
    DAY=$(date +"%Y-%m")
    HOUR=$(date +"%H-%M")
    raspistill -o /home/pi/photos/$DAY/$HOUR.jpg
    curl -F image=@/home/pi/photos/$DAY/$HOUR.jpg lpetrov.me:8000/tensorflow_api/scan/
fi
