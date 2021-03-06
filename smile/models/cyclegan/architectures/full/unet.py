import tensorflow as tf


# TODO: Implement this properly.
def unet_generator(X, is_training):
    weight_initializer = tf.truncated_normal_initializer(stddev=0.02)

    def conv7_stride1_k(inputs, k):
        """7x7, 1 strided convolution with k filters."""
        padded = tf.pad(inputs, [[0, 0], [3, 3], [3, 3], [0, 0]], "reflect")
        return tf.layers.conv2d(
            padded,
            kernel_size=(7, 7),
            strides=(1, 1),
            filters=k,
            activation=None,
            kernel_initializer=weight_initializer,
            use_bias=False,
            padding="valid")

    def conv3_stride2_k(inputs, k):
        """3x3, 2 strided convolution with k filters."""
        return tf.layers.conv2d(
            inputs,
            kernel_size=(3, 3),
            strides=(2, 2),
            filters=k,
            activation=None,
            kernel_initializer=weight_initializer,
            use_bias=False,
            padding="same")

    def deconv3_stride2_k(inputs, shortcuts, k):
        """3x3. 2 strided deconvolution (transposed convolution) with k filters."""
        upsampled = tf.layers.conv2d_transpose(
            inputs,
            kernel_size=(3, 3),
            strides=(2, 2),
            filters=k,
            activation=None,
            kernel_initializer=weight_initializer,
            use_bias=False,
            padding="same")

        return tf.concat((upsampled, shortcuts), axis=-1)

    lrelu = tf.nn.leaky_relu
    norm = tf.contrib.layers.instance_norm

    # Net definition.  # TODO: See paper code.
    c1 = lrelu(norm(conv7_stride1_k(X, 32)))
    c2 = lrelu(norm(conv3_stride2_k(c1, 64)))
    c3 = lrelu(norm(conv3_stride2_k(c2, 128)))
    c4 = lrelu(norm(conv3_stride2_k(c3, 256)))
    d1 = lrelu(norm(deconv3_stride2_k(c4, c3, 128)))
    d2 = lrelu(norm(deconv3_stride2_k(d1, c2, 64)))
    d3 = lrelu(norm(deconv3_stride2_k(d2, c1, 32)))
    net = lrelu(norm(tf.layers.conv2d_transpose(d3, kernel_size=(3, 3), strides=(2, 2), filters=16, padding="same")))
    net = tf.nn.tanh(norm(tf.layers.conv2d(net, kernel_size=(3, 3), strides=(2, 2), filters=3, padding="same")))
    return net