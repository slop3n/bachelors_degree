python3 scripts/retrain.py   --bottleneck_dir=tf_files/bottlenecks   --how_many_training_steps=500   --model_dir=tf_files/models/"${ARCHITECTURE}"   --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}"   --output_graph=tf_files/retrained_graph.pb   --output_labels=tf_files/retrained_labels.txt   --architecture="${ARCHITECTURE}"   --image_dir=tf_files/food




python3 scripts/label_image.py --graph=tf_files/retrained_graph.pb --labels=tf_files/retrained_labels.txt --image=the-ultimate-hamburger.jpg 

