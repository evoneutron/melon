
Melon
=====

Melon is a lightweight package meant to simplify data processing for Deep Learning.

| It removes the need for boilerplate code to pre-process the data prior to (model) training or inference.
| It aims at standardizing data serialization and manipulation approaches, and simplifies model training.
|
| The default formats align with the requirements by frameworks such as **Tensorflow** / **PyTorch**. The package also provides various level of customizations depending on the use-case.


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

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        reader = ImageReader(source_dir)
        X, Y = reader.read()
        ...
        with tf.Session() as s:
            s.run(..., feed_dict = {X_placeholder: X, Y_placeholder: Y})

| ``source_dir`` directory should contain images to process (``svg`` format is currently not suppored).
| See ``tests/resources/images`` for sample directory. In that directory there is an optional ``labels.txt`` file that is described in Labeling_.
|
| *With custom* options_:

.. code-block:: python

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        options = { "data_format": "channels_last",
                    "normalize": False }
        reader = ImageReader(source_dir, options)
        ...

| This changes output of data to `channels-last` format (each sample will be ``Height x Width x Channel``) and doesn't normalize the data. See options_ for available options.
|
| In case number of images is too large to fit into memory we can use batch-processing.

.. code-block:: python

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        options = { "batch_size": 64 }
        reader = ImageReader(source_dir, options)
        while reader.has_next():
            X, Y = reader.read()
            ...

| This reads images in batches of 64 images per batch until all images are read.
| If ``batch_size`` is not specified then ``reader.read()`` will read all images in ``source_dir``.




Options
------------------
.. _options:

**Images**

- width - width dimension of the output (pixels)
    default: ``255``
- height - height dimension of the output (pixels)
    default: ``255``
- data_format - format of the output
    options:
        - ``channels_first`` - `Channel x Height x Width`
        - ``channels_last`` - `Height x Width x Channel`

- normalize - normalize data
    default: ``True``
- num_threads - number of threads for parallel data processing
    default: ``Number of cores of the machine``

Labeling
-----------------
.. _Labeling:

| Labeling section.
