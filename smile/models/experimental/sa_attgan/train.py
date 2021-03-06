from pathlib import Path
from typing import List

import tensorflow as tf

from smile.data.celeb import img_and_attribute_dataset
from smile.models.experimental import SelfAttentionAttGAN
from smile import experiments


def run_training(model_dir: Path,
                 train_tfrecord_paths: List[str],
                 test_tfrecord_paths: List[str],
                 considered_attributes: List[str],
                 **hparams):

    model_dir.mkdir(parents=True, exist_ok=True)

    train_dataset = img_and_attribute_dataset(
        train_tfrecord_paths,
        considered_attributes,
        batch_size=hparams["batch_size"],
        crop_and_rescale=True)
    test_dataset = img_and_attribute_dataset(
        test_tfrecord_paths,
        considered_attributes,
        batch_size=3,
        crop_and_rescale=True)

    train_iterator = train_dataset.make_initializable_iterator()
    test_iterator = test_dataset.make_initializable_iterator()

    img_train, attributes_train = train_iterator.get_next()
    img_test, attributes_test = test_iterator.get_next()

    iterator_initializer = tf.group(train_iterator.initializer, test_iterator.initializer)

    model = SelfAttentionAttGAN(
        considered_attributes,
        img_train, attributes_train,
        img_test, attributes_test,
        **hparams)

    summary_writer = tf.summary.FileWriter(str(model_dir))

    scaffold = tf.train.Scaffold(local_init_op=tf.group(
        tf.local_variables_initializer(),
        tf.tables_initializer(),
        iterator_initializer))

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    max_training_steps = 150000

    with tf.train.MonitoredTrainingSession(
            scaffold=scaffold,
            config=config,
            checkpoint_dir=str(model_dir),
            save_summaries_secs=30) as sess:
        while not sess.should_stop():
            i = model.train_step(sess, summary_writer, **hparams)
            if i > max_training_steps:
                break


if __name__ == "__main__":
    arg_parser = experiments.ArgumentParser()
    arg_parser.add_argument("--model-dir", required=False, help="Directory for checkpoints etc.")
    arg_parser.add_argument("--train_tfrecords", nargs="+", required=True, help="train tfrecords files.")
    arg_parser.add_argument("--test_tfrecords", nargs="+", required=True, help="test tfrecords files.")

    arg_parser.add_hparam("--batch_size", default=32, type=int, help="Batch size")

    args, hparams = arg_parser.parse_args()

    ROOT_RUNS_DIR = Path("runs")
    if args.model_dir is None:
        model_dir = ROOT_RUNS_DIR / Path(experiments.experiment_name("experimental", hparams))
    else:
        model_dir = Path(args.model_dir)

    # TODO: Param for this. Handle mutual exclusiveness?
    considered_attributes = ["Smiling", "Male", "Mustache", "5_o_Clock_Shadow", "Blond_Hair"]

    run_training(
        model_dir,
        args.train_tfrecords,
        args.test_tfrecords,
        considered_attributes,
        **hparams)
