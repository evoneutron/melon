
Melon
=====

Melon is a lightweight package meant to simplify data processing for Deep Learning.

| It removes the need for boilerplate code to pre-process the data prior to (model) training or inference.
| It aims at standardizing data serialization and manipulation approaches, and simplifies model training.
|
| The default formats align with the requirements by frameworks such as **Tensorflow** / **PyTorch**.
| The tool also provides various level of customizations depending on the use-case.


Installation
------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install melon

Supported in Python >=3.4, 2.7

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Examples
----------------

**Images**

| *With default* options_:

.. code-block:: python

    from melon import ImageReader

    def train():
        source_dir = "resources/images"
        reader = ImageReader(source_dir)
        X, Y = reader.read()
        ...
        with tf.Session() as s:
            s.run(..., feed_dict = {X_placeholder: X, Y_placeholder: Y})

| ``source_dir`` directory should contain images to read. See ``tests/resources/images`` for a sample directory.
| In that directory there is an optional ``labels.txt`` file that is described in Labeling_.

-------

| Number of images may be too large to fit into memory which creates the need for batch-processing.
|

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


Options
------------------

.. _options:

**Images**

    width
        Width of the output (pixels). default: ``255``

    height
        Height of the output (pixels). default: ``255``

    batch_size
        Batch size of each read. default: all images

    data_format
        | ``channels_first`` - `Channel x Height x Width` (default)
        | ``channels_last`` - `Height x Width x Channel`

    normalize
        Normalize data. default: ``True``

    num_threads - number of threads for parallel processing
        default: ``Number of cores of the machine``

Labeling
-----------------
.. _Labeling:

| In supervised learning each image needs to be mapped to a label.
| While the tool supports reading images without labels (e.g. for inference) it also provides a way to label them.
|
| To read images and labels ``source_dir`` needs to have ``labels`` (extension optional) file.
| Sample file is provided in ``tests/reosurces/images/labels.txt``

.. code-block:: text

    #legend
    1 : human
    2 : pedestrian
    3 : cat
    4 : parrot
    5 : car

    #map
    img275:3
    img324:4
    img551:5
    img872:1
    img928:3
    img999:2

| ``#legend`` section is optional but ``#map`` section is needed for mapping labels to an image.

-----

**Generating labels file**

| To generate ``labels.txt`` we can use CLI with the following command:

.. code-block:: text

    $ melon generate
    > Source dir:

| After providing source directory path the tool will generate labels file in that directory that looks similar to the sample above.
| Final step is to add label to each row in the generated file.


Roadmap
-------

- Support for video data

- Support for textual data