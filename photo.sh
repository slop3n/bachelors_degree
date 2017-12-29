DATE=$(date +"%H")
if [ "$DATE" -get 7 -a "$DATE" -le 18 ]
  then
    DATE2=$(date +"%Y-%m-%d_%H%M")
    raspistill -o /home/pi/photos/$DATE2.jpg
    curl -F image=@/home/pi/photos/$DATE2.jpg lpetrov.me:8000/tensorflow_api/scan/
fi