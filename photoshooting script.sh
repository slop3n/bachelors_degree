DAY=$(date +"%Y_%m_%d")
TIME=$(date +"%H_%M")
mkdir -p photos/$DAY
raspistill -o /home/pi/photos/$DAY/$TIME.jpg
curl -F image=@/home/pi/photos/$DAY/$TIME.jpg lpetrov.me:8000/tensorflow_api/scan/
