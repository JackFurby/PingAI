import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data #test dataset

'''
tensor input (this is the data being used), add game data in tensor form here
(a tensor is simmalar to a array), use a ML algorithm to put game data into
correct format.

one_hot is saying for the output only one element is 'hot' (on)
0 = [1,0,0,0,0,0,0,0,0]
1 = [0,1,0,0,0,0,0,0,0]
2 = [0,0,1,0,0,0,0,0,0]
3 = [0,0,0,1,0,0,0,0,0]

'''
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

#nodes in each layer
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10 #classes the data set has
batch_size = 100 #batches split dataset into managable chunks, each batch will be trained seperatly.

#height * width
x = tf.placeholder('float',[None, 784]) #[none, 784] is optional, it specifies shape of input accepted (error thrown if input is out of shape)
y = tf.placeholder('float')

def neural_network_model(data):
    #defines weights and biases (both randow at first)
    #biases are added to each sum (helps if all nodes are off as it can help some to still fire. Bias will need to be optimized)
    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([784, n_nodes_hl1])), 'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}
    hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])), 'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}
    hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])), 'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}
    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])), 'biases':tf.Variable(tf.random_normal([n_classes]))}

    #(input_data * weights) + biases
    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])  #(raw data * weights) + biases
    l1 = tf.nn.relu(l1) #result = 0 if input is negative, else input itself

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases']) #(layer 1 * weights) + biases
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases']) #(layer 2 * weights) + biases
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases'] #(layer 3 * weights) + biases
    return output #network output (model is done)

def train_neural_network(in_data):
    prediction = neural_network_model(in_data)
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost) #default learning rate = 0.01

    hm_epochs = 10 #how many cycles of feeding forward and back propagation

    with tf.Session() as sess: #launches the model
        sess.run(tf.global_variables_initializer()) #init opperation

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(mnist.train.num_examples / batch_size)):
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict = {x: epoch_x, y: epoch_y}) #c = cost (how wrong the result is)
                epoch_loss += c
            print('Epoc', epoch, 'completed out of', hm_epochs, 'loss:', epoch_loss)

        correct  = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1)) #return max values in arrays
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuiracy:', accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

train_neural_network(x)
