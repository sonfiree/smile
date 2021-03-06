from multiprocessing import cpu_count
from typing import List

import tensorflow as tf


_CELEB_A_SHAPE = (218, 178, 3)


def _parse_serialized_img(bytes, crop_and_rescale):
    """Parse img from tfrecords to [0, 1]."""
    img = tf.decode_raw(bytes, tf.uint8)
    img = tf.reshape(img, _CELEB_A_SHAPE)
    if crop_and_rescale:
        img = tf.image.crop_to_bounding_box(img, 26, 3, 170, 170)
        img = tf.image.resize_images(img, (128, 128))
    img = tf.cast(img, tf.float32)
    img = img / 255.0
    return img


def dataset(tfrecord_paths: List[str], crop_and_rescale: bool=False) -> tf.data.Dataset:
    """
    Create dataset from tfrecords containing raw encoded celeb-a images.
    :param tfrecord_paths: paths to tfrecord files.
    :param crop_and_rescale: whether images should be cropped and rescaled to 128x128.
    :return: the dataset.
    """

    def parse_serialized(serialized_example):
        features = tf.parse_single_example(
            serialized_example,
            features={"img": tf.FixedLenFeature([], tf.string)})
        img = _parse_serialized_img(features["img"], crop_and_rescale)
        return img

    ds = tf.data.TFRecordDataset(tfrecord_paths)
    ds = ds.map(parse_serialized, num_parallel_calls=cpu_count())

    return ds


def dataset_with_attributes(tfrecord_paths: List[str],
                            considered_attributes: List[str],
                            crop_and_rescale: bool=False,
                            filter_examples_without_attributes: bool=True) -> tf.data.Dataset:
    """
    Create dataset from tfrecords containing raw encoded celeb-a images and
    their attributes as tf.VarLenFeature strings.
    :param tfrecord_paths: paths to tfrecord files.
    :param considered_attributes: The attributes to include in attribute set per image.
    :param crop_and_rescale: whether images should be cropped and rescaled to 128x128.
    :param filter_examples_without_attributes: whether examples without any of the considered attributes
                                               should be filtered.
    :return: the dataset
    """

    # TODO: Add check for valid attribute names.

    # Note: One oov bucket for all non considered attributes.
    attribute_index = tf.contrib.lookup.index_table_from_tensor(considered_attributes, num_oov_buckets=1)

    def parse_serialized(serialized_example):
        features = tf.parse_single_example(
            serialized_example,
            features={"img": tf.FixedLenFeature([], tf.string),
                      "attributes": tf.VarLenFeature(tf.string)})

        img = _parse_serialized_img(features["img"], crop_and_rescale)

        # Considered attributes as indicator vector.
        attributes = attribute_index.lookup(features["attributes"])
        attributes = tf.sparse_to_indicator(attributes, len(considered_attributes) + 1)  # +1 for the oov bucket.
        attributes = attributes[:-1]  # Skip the oov bucket since those attributes should not be considered.
        attributes = tf.cast(attributes, tf.float32)

        return img, attributes

    def at_least_one_considered_attribute(_unused_img, attributes):
        return tf.logical_not(tf.reduce_all(tf.equal(attributes, 0.0)))

    ds = tf.data.TFRecordDataset(tfrecord_paths)
    ds = ds.map(parse_serialized, num_parallel_calls=cpu_count())
    if filter_examples_without_attributes:
        ds = ds.filter(at_least_one_considered_attribute)

    return ds
