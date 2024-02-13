from PyQt5.QtCore import QThread, pyqtSignal
import tensorflow as tf
import os


class WorkerTrainModel(QThread):
    def __init__(self, X, Y, n_units, n_epochs, lr, metrics, parent=None):
        """Construct a worker to train a Logistic Regression model.

        Args:
            X (ndarray): Numpy array of inputs.
            Y (ndarray): Numpy array of outputs.
            n_units (int): Input shape.
            n_epochs (int): Total epochs.
            lr (float): Learning rate.
            metrics (list): Custom metrics.
            parent (optional): Defaults to None.
        """
        QThread.__init__(self, parent)
        self.X = (X,)
        self.Y = (Y,)
        self.n_units = n_units
        self.n_epochs = n_epochs
        self.lr = lr
        self.metrics = metrics

    worker_complete = pyqtSignal(dict)

    def run(self):
        """Trains a model"""

        sgd_optimizer = tf.keras.optimizers.SGD(
            learning_rate=self.lr, momentum=0.0, nesterov=False, name="SGD"
        )
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.InputLayer(input_shape=self.n_units))
        model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

        model.compile(optimizer=sgd_optimizer, loss="binary_crossentropy")

        history = model.fit(self.X, self.Y, epochs=self.n_epochs, verbose=0)

        self.worker_complete.emit({"model": model})


class WorkerTrainModelTrainingLoop(QThread):
    def __init__(self, X, Y, n_units, n_epochs, lr, metrics, parent=None):
        """Construct a worker to train a Logistic Regression model.

        Args:
            X (ndarray): Numpy array of inputs.
            Y (ndarray): Numpy array of outputs.
            n_units (int): Input shape.
            n_epochs (int): Total epochs.
            lr (float): Learning rate.
            metrics (list): Custom metrics.
            parent (optional): Defaults to None.
        """
        QThread.__init__(self, parent)
        self.X = (X,)
        self.Y = (Y,)
        self.n_units = n_units
        self.n_epochs = n_epochs
        self.lr = lr
        self.metrics = metrics

    worker_complete = pyqtSignal(dict)

    def run(self):
        """Trains a model"""

        sgd_optimizer = tf.keras.optimizers.SGD(
            learning_rate=self.lr, momentum=0.0, nesterov=False, name="SGD"
        )

        inputs = tf.keras.Input(shape=(self.n_units,))
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(inputs)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)

        model = tf.keras.Sequential()
        model.add(tf.keras.Input(shape=self.n_units))
        model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

        loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)

        batch_size = 64
        train_dataset = tf.data.Dataset.from_tensor_slices((self.X, self.Y))
        train_dataset = train_dataset.shuffle(buffer_size=1024).batch(batch_size)

        for i in range(self.n_epochs):

            # Iterate over the batches of the dataset.
            for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):

                # Open a GradientTape to record the operations run
                # during the forward pass, which enables auto-differentiation.
                with tf.GradientTape() as tape:

                    # Run the forward pass of the layer.
                    # The operations that the layer applies
                    # to its inputs are going to be recorded
                    # on the GradientTape.
                    # Logits for this minibatch
                    logits = model(x_batch_train, training=True)

                    # Compute the loss value for this minibatch.
                    loss_value = loss_fn(y_batch_train, logits)

                # Use the gradient tape to automatically retrieve
                # the gradients of the trainable variables with respect to the loss.
                grads = tape.gradient(loss_value, model.trainable_weights)

                # Run one step of gradient descent by updating
                # the value of the variables to minimize the loss.
                sgd_optimizer.apply_gradients(zip(grads, model.trainable_weights))

        self.worker_complete.emit({"model": model})
