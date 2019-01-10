
Melon
=====

Melon is a lightweight package meant to simplify data processing for Deep Learning.

It removes the need for boring boilerplate code that is meant for pre-processing the data prior to (model) training or inference.
It aims at standardizing data serialization and manipulation approaches, and simplifies model training.

The format conventions align with Deep Learning frameworks such as **Tensorflow** / **PyTorch**, but the package also provides various level of customizations depending on the use-case.


Installation
------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install melon

Supported in Python 3.5 and newer, Python 2.7.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Examples
----------------

**Tensorflow**

**Images**

*With default* options_:

.. code-block:: python

    from melon import ImageLoader

    def train():
        loader = ImageLoader()
        source_dir = "resources/images"
        X, Y = loader.read(source_dir)
        ...
        with tf.Session() as s:
            s.run(..., feed_dict={X_placeholder: X, Y_placeholder: Y})

| ``resources/images`` directory should contain images to process (``svg`` format is currently not suppored).
| See ``tests/resources/images`` for sample directory. In that directory there is an optional ``labels.txt`` file that is described in Labeling_.


*With custom* options_:

.. code-block:: python

    from melon import ImageLoader

    def train():
        options = { "data_format": "channels_last",
                    "normalize": False }
        loader = ImageLoader(options)
        source_dir = "resources/images"
        X, Y = loader.read(source_dir)
        ...
        with tf.Session() as s:
            s.run(..., feed_dict={X_placeholder: X, Y_placeholder: Y})

| This changes output of data to `channels-last` format (each sample will be ``Height x Width x Channel``) and doesn't normalize the data. See options_ for available options.

Options
------------------
.. _options:

**Images**

- width - width dimension of the output (pixels)
    default: 255
- height - height dimension of the output (pixels)
    default: 255
- channels - channels dimension of the output
    default: 3
- data_format - format of the output
    options:
        - channels_first - ``Channel x Height x Width``
        - channels_last - ``Height x Width x Channel``

- normalize - normalize data
    default: True
- num_threads - number of threads for parallel data processing
    default: Number of cores of the server

Labeling
-----------------
.. _Labeling:

| Labeling section.
