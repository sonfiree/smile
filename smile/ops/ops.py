import tensorflow as tf


# TODO: Easily composable ops for all models.
# TODO: Add spectral normed layers here.
# TODO: Add spectral norm as an option on the conv layer.
# TODO: Maybe split up files by functionality a bit.


def reflect_pad(x, p):
    return tf.pad(x, [[0, 0], [p, p], [p, p], [0, 0]], "reflect")


def self_attention(x):
    f = None
    g = None
    # Support adding attention over any layer?


def get_normalization_fn(type, is_training, **hparams):
    if type == "batchnorm":
        pass
    elif type == "instancenorm":
        pass
    else:
        raise ValueError("Invalid normalization fn type.")
