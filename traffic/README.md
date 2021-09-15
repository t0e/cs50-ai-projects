# Implementing an AI to identify which traffic sign appears in a photograph

First of all, I have tried to use the sample model for the Handwriting project from the lecture with the input shape (30, 30, 3).

```python
  model = tf.keras.models.Sequential([

        tf.keras.layers.Conv2D(
            32, (3, 3), activation="relu", input_shape=(30, 30, 3)
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
```

I got the result ```loss: 3.5000 - accuracy: 0.0567``` which is a pretty low accuracy.

So, I've watched the lecture video again to find out the problem and I figured out that the images should be reshaped by dividing them by 255.

```python
  resized_img = resized_img / 255.0
```

Then the result was significantly improve to ```loss: 0.1541 - accuracy: 0.9692```.

I also changed the dropout value to ```0.3``` and got the result ```loss: 0.1137 - accuracy: 0.9735```.

I was not satisfied with the result and added one more convolution and pooling layers as follow.

```python
  tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
  tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
```

The result was improved a bit like this ```loss: 0.0714 - accuracy: 0.9809```.

Finally, I change the size of filters to ```64```.

```python
  tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
```

Here is the final result ```loss: 0.0616 - accuracy: 0.9867```.
