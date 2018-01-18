Image size can be any of the following: 128,160,192,224, greater size will be more accurate but slower
The mobilenet archiceture can be 0.25, 0.50, 0.75, 1.0, greater scale will be more accurate but slower

```
	IMAGE_SIZE=224
	ARCHITECTURE="mobilenet_1.0_${IMAGE_SIZE}"
```

```
python3 retrain.py   --bottleneck_dir=tf_files/bottlenecks   --how_many_training_steps=4000   --model_dir=tf_files/models/"${ARCHITECTURE}"   --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}"   --output_graph=tf_files/retrained_graph.pb   --output_labels=tf_files/retrained_labels.txt   --architecture="${ARCHITECTURE}"   --image_dir=tf_files/food
```

parameters to pass if the names are changed than those
--graph=tf_files/retrained_graph.pb --labels=tf_files/retrained_labels.txt 

```
	python3 label_image.py --image=the-ultimate-hamburger.jpg 
```
