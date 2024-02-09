from tensorflow import keras

class ResidualUnit(keras.layers.Layer):
    def __init__(self, filter_map_size: int, strides: int=1, **kwargs):
        super().__init__(**kwargs)
        self.conv_layers = [
            keras.layers.Conv2D(filter_map_size, 3, strides=strides, padding="same", use_bias=False),
            keras.layers.BatchNormalization(),
            keras.layers.Activation("relu"),
            keras.layers.Conv2D(filter_map_size, 3, strides=1, padding="same", use_bias=False),
            keras.layers.BatchNormalization(),
        ]
        
        if strides > 1:
            self.skip_layers = [
                keras.layers.Conv2D(filter_map_size, 1, strides=strides, padding="same", use_bias=False),
                keras.layers.BatchNormalization(),
            ]
        else:
            self.skip_layers = []
    
    def call(self, inputs):
        inputs_ = inputs
        for layer in self.conv_layers:
            inputs_ = layer(inputs_)
        for layer in self.skip_layers:
            inputs = layer(inputs)
        return keras.activations.relu(inputs + inputs_)