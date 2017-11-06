## 1 Install tensforflow  
## 2 Install bazel  
## 3 Set environment variables   
IMAGE_SIZE=224  
ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}"  
## 4 source tensor flow  
source mytensforflowdirectory/bin/activate  
## start tensorboard in a separate terminalzzzz
tensorboard --logdir tf_files/training_summaries &  
## 5 run use tensorflow_for_poets retrain script / example
python -m scripts.retrain --image_dir ./training_data/ --how_many_training_steps 500 --model_dir=./tf_files/models --architecture="${ARCHITECTURE}" --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt   
## 6 apply label
python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=testing_data/fairway8.jpg  

## Note:   
Had to use converseen to convert png to jpg  


# Online SVM requirements: 
- scikit-learn
- matconvnet
- matlab python hooks
