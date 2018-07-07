import tensorflow as tf


def spectral_norm_constraint(W, n_power_iterations):
    # TODO: Implement spectral norm to be usable with variable constraint with tf.get_variable
    # Then this would be run after each sgd update step. See e.g. tf.clip_by_norm
    # Issue with first pass? doesn't matter probably
    # TODO: Remove the transposes by reformulating equations a bit.

    original_kernel_shape = W.shape
    d_out = original_kernel_shape[-1]

    W_sn = W
    W_sn = tf.reshape(W_sn, (-1, d_out))
    W_sn = tf.transpose(W_sn)

    u = tf.get_variable(
        "u",
        shape=(d_out, 1),
        initializer=tf.truncated_normal_initializer(mean=0.0, stddev=1.0),
        trainable=False)

    def power_iteration_step(i, u_i, _v_i):
        v_i = tf.nn.l2_normalize(tf.transpose(W_sn) @ u_i)
        u_i = tf.nn.l2_normalize(W_sn @ v_i)
        return i + 1, u_i, v_i

    # TODO: Any benefit to using a tf.while_loop? Could just unroll it.
    _, u_pi, v_pi = tf.while_loop(
        cond=lambda i, _u, _v: i < n_power_iterations,
        body=power_iteration_step,
        loop_vars=(
            tf.constant(0, tf.int32),
            u,
            tf.zeros((W.shape[1], 1))))

    W_sn = W_sn / (tf.transpose(u_pi) @ W_sn @ v_pi)
    W_sn = tf.transpose(W_sn)
    W_sn = tf.reshape(W_sn, original_kernel_shape)

    return W_sn


def sn_conv(x, d, k, s, padding="SAME", use_bias=True, n_power_iterations=1, **kwargs):
    # TODO: Add assertion about data format. NHWC is expected atm.
    # TODO: Remove the transposes by reformulating equations a bit.

    d_in = x.shape[-1]
    d_out = d

    kernel_shape = (k, k, d_in, d_out)
    W = tf.get_variable("kernel", shape=kernel_shape, initializer=tf.initializers.variance_scaling())
    W = tf.reshape(W, (-1, d_out))
    W = tf.transpose(W)  # Paper says R^(d_out, d_in, h, w) -> R^(d_out, (d_in*h*w)).

    u = tf.get_variable(
        "u",
        shape=(d_out, 1),
        initializer=tf.truncated_normal_initializer(mean=0.0, stddev=1.0),
        trainable=False)

    def power_iteration_step(i, u_i, _v_i):
        v_i = tf.nn.l2_normalize(tf.transpose(W) @ u_i)
        u_i = tf.nn.l2_normalize(W @ v_i)
        return i + 1, u_i, v_i

    _, u_pi, v_pi = tf.while_loop(
        cond=lambda i, _u, _v: i < n_power_iterations,
        body=power_iteration_step,
        loop_vars=(
            tf.constant(0, tf.int32),
            u,
            tf.zeros((W.shape[1], 1))))

    sigma_W = tf.transpose(u_pi) @ W @ v_pi
    W = W / sigma_W
    W = tf.transpose(W)
    W = tf.reshape(W, kernel_shape)

    # TODO: Should the normalization of W happen everytime? Probably not during evaluation for example?

    tf.add_to_collection(tf.GraphKeys.UPDATE_OPS, u.assign(u_pi))

    x = tf.nn.conv2d(x, W, strides=(1, s, s, 1), padding=padding)
    if use_bias:
        b = tf.get_variable("b", shape=(d_out,), initializer=tf.initializers.constant(0.0))
        x = tf.nn.bias_add(x, b)
    return x, u, u_pi


def dconv():
    # TODO: Handle spectral normalization
    pass
