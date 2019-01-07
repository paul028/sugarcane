import tensorflow as tf
import os
# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
'''
Classify the captured image stored in the test folder
'''
winner="Unknown"
def classify_image():
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("trained_model/retrained_labels.txt")]
    with tf.gfile.GFile("trained_model/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    file='capture.JPG'
    print('Classifying Captured Image... Please Wait...')
    with tf.Session() as sess:
        # Read the image_data
        image_data = tf.gfile.GFile('test/'+file, 'rb').read()
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                                       {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        records = []
        row_dict = {}
        head, tail = os.path.split(file)
        row_dict['id'] = tail.split('.')[0]
        winner=label_lines[top_k[0]]
        winner = winner.replace(" ", "_")
        if (winner == 'anguilla_bicolor'):
            winner = 'Anguilla_Bicolor'
        if (winner == 'anguilla_marmorata'):
            winner = 'Anguilla_Marmorata'
        if (winner == 'bicolor'):
            winner = 'Bicolor'
        if (winner == 'marmorata'):
            winner = 'Marmorata'

        print("Classification: "+winner)
        for node_id in top_k: #show the raw score of the classification
            human_string = label_lines[node_id]
            human_string = human_string.replace(" ","_")
            if(human_string == 'downy_mildew'):
                human_string = 'Downy_Mildew'
            if(human_string == 'normal_leaves'):
                human_string = 'Normal_Leaves'
            if(human_string == 'smut'):
                human_string = 'Smut'
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
            row_dict[human_string] = score
        records.append(row_dict.copy())

    f.close()

def main():
    classify_image()
if __name__ == '__main__':
    main()
