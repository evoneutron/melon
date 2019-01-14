|build-status| |coverage-status|

Melon
=====

| Melon is a lightweight package meant to simplify data processing for Deep Learning.

| It removes the need for boilerplate code to pre-process the data prior to (model) training, testing and inference.
| It aims at standardizing data serialization and manipulation approaches.
|
| The default formats align with the requirements by frameworks such as **Tensorflow** / **PyTorch**.
| The tool also provides various level of customizations depending on the use-case.

Installation
------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install melon

Supported in Python >= 3.4.0

.. _pip: https://pip.pypa.io/en/stable/quickstart/

Examples
----------------

**Images**

With default options_:

.. code-block:: python

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        reader = ImageReader(source_dir)
        X, Y = reader.read()
        ...
        with tf.Session() as s:
            s.run(..., feed_dict = {X_placeholder: X, Y_placeholder: Y})

| ``source_dir`` directory should contain images that need to be read. See `sample directory`_ for reference.
| In the sample directory there is an optional ``labels.txt`` file that is described in Labeling_.

-------

Since number of images may be too large to fit into memory the tool supports batch-processing.

.. code-block:: python

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        options = { "batch_size": 32 }
        reader = ImageReader(source_dir, options)
        while reader.has_next():
            X, Y = reader.read()
            ...

| This reads images in the batches of 32 until all images are read. If ``batch_size`` is not specified then ``reader.read()`` will read all images.

---------------

.. _Custom options:

With custom options_:

.. code-block:: python

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        options = { "data_format": "channels_last", "normalize": False }
        reader = ImageReader(source_dir, options)
        ...

| This changes format of data to ``channels-last`` (each sample will be ``Height x Width x Channel``) and doesn't normalize the data. See options_ for available options.

.. _options:

Options
------------------

**Images**

    width
        Width of the output (pixels). default: ``255``

    height
        Height of the output (pixels). default: ``255``

    batch_size
        Batch size of each read. default: All images in a directory

    data_format
        Format of the images data

            | ``channels_first`` - `Channel x Height x Width` (default)
            | ``channels_last`` - `Height x Width x Channel`

    label_format
        Format of the labels data

            | ``one_hot`` - as a matrix, with one-hot vector per image (default)
            | ``label`` -  as a vector, with a single label per image


    normalize
        Normalize data. default: ``True``

    num_threads - number of threads for parallel processing
        default: Number of cores of the machine

.. _Labeling:

Labeling
-----------------

| In supervised learning each image needs to be mapped to a label.
| While the tool supports reading images without labels (e.g. for inference) it also provides a way to label them.

-----

**Generating labels file**

| To generate ``labels`` file use the following command:

.. code-block:: text

    $ melon generate
    > Source dir:

| After providing source directory the tool will generate ``labels`` file in that directory with blank labels.
| Final step is to add a label to each row in the generated file.
|
| For reference see `sample labels`_:

.. code-block:: text

    #legend
    pedestrian:0
    cat:1
    parrot:2
    car:3
    apple tree:4

    #map
    img275.jpg:1
    img324.jpg:2
    img551.jpg:3
    img928.jpg:1
    img999.png:0
    img736.png:4

| ``#legend`` section is optional but ``#map`` section is required to map a label to an image.

-----

**Format of the labels**

Label's output format can be specified in `Custom options`_. It defaults to ``one-hot`` format.

Roadmap
-------

- Support for textual data (Q1 2019)

- Support for video data (Q1 2019)

- Support for reading from AWS S3 (Q2 2019)



.. |build-status| image:: https://travis-ci.com/evoneutron/melon.svg?branch=master
    :target: https://travis-ci.com/evoneutron/melon

.. |coverage-status| image:: https://codecov.io/gh/evoneutron/melon/branch/master/graphs/badge.svg
   :target: https://codecov.io/gh/evoneutron/melon/branch/master

.. _`sample directory`: https://github.com/evoneutron/melon/tree/master/tests/resources/images/sample

.. _`sample labels`: https://github.com/evoneutron/melon/tree/master/tests/resources/images/sample/labels.txt
