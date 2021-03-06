from chainer.functions.connection import embed_id
from chainer.initializers import normal
from chainer import link
from chainer import variable


class EmbedID(link.Link):

    """Efficient linear layer for one-hot input.

    This is a link that wraps the :func:`~chainer.functions.embed_id` function.
    This link holds the ID (word) embedding matrix ``W`` as a parameter.

    Args:
        in_size (int): Number of different identifiers (a.k.a. vocabulary
            size).
        out_size (int): Size of embedding vector.
        initialW (2-D array): Initial weight value. If ``None``, then the
            matrix is initialized from the standard normal distribution.
            May also be a callable that takes ``numpy.ndarray`` or
            ``cupy.ndarray`` and edits its value.
        ignore_label (int or None): If ``ignore_label`` is an int value,
            ``i``-th column of return value is filled with ``0``.

    .. seealso:: :func:`~chainer.functions.embed_id`

    Attributes:
        W (~chainer.Variable): Embedding parameter matrix.

    .. admonition:: Example

        >>> W = np.array([[0, 0, 0],
        ...               [1, 1, 1],
        ...               [2, 2, 2]]).astype('f')
        >>> W
        array([[ 0.,  0.,  0.],
               [ 1.,  1.,  1.],
               [ 2.,  2.,  2.]], dtype=float32)
        >>> l = L.EmbedID(W.shape[0], W.shape[1], initialW=W)
        >>> x = np.array([2, 1]).astype('i')
        >>> x
        array([2, 1], dtype=int32)
        >>> y = l(x)
        >>> y.data
        array([[ 2.,  2.,  2.],
               [ 1.,  1.,  1.]], dtype=float32)

    """

    ignore_label = None

    def __init__(self, in_size, out_size, initialW=None, ignore_label=None):
        super(EmbedID, self).__init__()
        self.ignore_label = ignore_label

        with self.init_scope():
            if initialW is None:
                initialW = normal.Normal(1.0)
            self.W = variable.Parameter(initialW, (in_size, out_size))

    def __call__(self, x):
        """Extracts the word embedding of given IDs.

        Args:
            x (~chainer.Variable): Batch vectors of IDs.

        Returns:
            ~chainer.Variable: Batch of corresponding embeddings.

        """
        return embed_id.embed_id(x, self.W, ignore_label=self.ignore_label)
