class HuffmanNode:
    def __init__(self, char_ascii, freq):
        self.char_ascii = char_ascii  # stored as an integer - the ASCII character code value
        self.freq = freq  # the frequency count associated with the node
        self.left = None  # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __lt__(self, other):
        return comes_before(self, other)  # Allows use of Python List sorting

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __repr__(self):
        return "HuffmanNode({!r}, {!r}, {!r}, {!r})".format(self.char_ascii, self.freq, self.left, self.right)


def comes_before(a, b):
    """Returns True if node a comes before node b, False otherwise"""
    if a.freq == b.freq:
        return a.char_ascii < b.char_ascii
    return a.freq < b.freq


def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    freq = a.freq + b.freq
    if a.freq == b.freq:
        if a.char_ascii < b.char_ascii:
            newhuff = HuffmanNode(a.char_ascii, freq)
            newhuff.set_left(a)
            newhuff.set_right(b)
            return newhuff
        elif b.char_ascii < a.char_ascii:
            newhuff = HuffmanNode(b.char_ascii, freq)
            newhuff.set_left(b)
            newhuff.set_right(a)
            return newhuff
    elif a.freq < b.freq:
        if a.char_ascii < b.char_ascii:
            newhuff = HuffmanNode(a.char_ascii, freq)
        elif b.char_ascii < a.char_ascii:
            newhuff = HuffmanNode(b.char_ascii, freq)
        newhuff.set_left(a)
        newhuff.set_right(b)
        return newhuff
    elif b.freq < a.freq:
        if a.char_ascii < b.char_ascii:
            newhuff = HuffmanNode(a.char_ascii, freq)
        elif b.char_ascii < a.char_ascii:
            newhuff = HuffmanNode(b.char_ascii, freq)
        newhuff.set_left(b)
        newhuff.set_right(a)
        return newhuff


def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the
    frequency of occurrences of all the characters within that file
    Returns a Python List with 256 entries - counts are initialized to zero.
    The ASCII value of the characters are used to index into this list for the frequency counts"""
    file = open(filename, 'r')
    char_counts = [0] * 256
    while True:
        char = file.read(1)
        if not char:
            break
        else:
            char_counts[ord(char)] += 1
    file.close()
    return char_counts


def create_huff_tree(freq_list):
    """Input is the list of frequencies (provided by cnt_freq()).
    Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree. Returns None if all counts are zero."""
    sorted_list = []
    for i in range(len(freq_list)):
        if freq_list[i] > 0:
            node = HuffmanNode(i, freq_list[i])
            sorted_list.append(node)
    if not sorted_list:
        return None
    if len(sorted_list) == 1:
        return sorted_list[0]
    while len(sorted_list) > 1:
        # sorted_list.sort(key = sort_by_freq)
        sorted_list = sorted(sorted_list, key=lambda x: (x.freq, x.char_ascii))
        first = sorted_list.pop(0)
        second = sorted_list.pop(0)
        newhuff = combine(first, second)
        sorted_list.append(newhuff)
    return sorted_list[0]

                                                                        # why does this order work?
def code_helper(root, pylist, val):
    if root is not None:
        pylist[root.char_ascii] = val
        code_helper(root.left, pylist, val + '0')
        code_helper(root.right, pylist, val + '1')
    return pylist


def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    as the index into the arrary, with the resulting Huffman code for that character stored at that location.
    Characters that are unused should have an empty string at that location"""
    pylist = [''] * 256
    return code_helper(node, pylist, '')


def create_header(freq_list):
    """Input is the list of frequencies (provided by cnt_freq()).
    Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” """
    header = []
    for i in range(len(freq_list)):
        if freq_list[i] != 0:
            header.append(str(i))
            header.append(str(freq_list[i]))
    return ' '.join(header)


def order(in_file):
    file = open(in_file, 'r')
    char_order = []
    while True:
        char = file.read(1)
        if not char:
            break
        else:
            char_order.append(ord(char))
    file.close()
    return char_order


def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take not of special cases - empty file and file with only one unique character"""
    pylist = cnt_freq(in_file)
    header = create_header(pylist)
    node = create_huff_tree(pylist)
    code_list = create_code(node)
    ordered = order(in_file)
    for i in range(len(code_list)):
        for j in range(len(ordered)):
            if ordered[j] == i:
                ordered[j] = code_list[i]
    full_code = ''.join(ordered)
    output = open(out_file, "w", newline='')
    output.write(header)
    if len(header) > 0 and len(full_code) > 0:
        output.write('\n')
    output.write(full_code)
    output.close()


def parse_header(header_string):
    """takes properly formatted header from solution file and makes a
    frequency list of ascii characters"""
    freq_list = [0] * 256
    header_list = header_string.split()
    while len(header_list) > 0:
        index = int(header_list.pop(0))
        freq_list[index] = int(header_list.pop(0))
    return freq_list


def get_code(encoded_file):
    """gets the encoded text from an encoded file"""
    file = open(encoded_file, "r")
    header = file.readline()
    code = file.readline()
    file.close()
    return code


def get_header(encoded_file):
    """gets the header from an encoded file"""
    file = open(encoded_file, "r")
    header = file.readline()
    file.close()
    return header


def decode_tree_traversal(node: HuffmanNode, code):
    """traverses through a huffman tree and turns encoded text back to
    the original decoded text"""
    root = node
    decoded = ""
    i = 0
    while i < len(code):
        if node.left is not None:
            if code[i] == "0":
                node = node.left
            if code[i] == "1":
                node = node.right
            i += 1
        else:
            decoded += chr(node.char_ascii)
            node = root
    decoded += chr(node.char_ascii)
    return decoded


def huffman_decode(encoded_file, decode_file):
    """takes a file with properly formatted header and encoded code and
    writes the decoded code to a new file"""
    header = get_header(encoded_file)
    code = get_code(encoded_file)
    if not header:
        decoded = ''
    else:
        parsed_header = parse_header(header)
        tree = create_huff_tree(parsed_header)
        decoded = decode_tree_traversal(tree, code)
    file = open(decode_file, "w", newline='')
    if header and not code:
        decoded = decoded * tree.freq
    file.write(decoded)
    file.close()
