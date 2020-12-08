def chunker(seq, size):
    """
    Chunk the seq (sequence) in the specified size(chunk) of items/objects

    :param seq: Sequence/List/Collection of objects
    :param size: The size of the chunk
    :return:
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
