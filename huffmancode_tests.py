import unittest
from huffman import *

class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)
        freqlist1 = cnt_freq("multiline.txt")
        anslist2 = [5, 2, 0, 2, 7, 0, 0, 5, 2, 4, 1, 3]
        self.assertListEqual(freqlist1[101:113], anslist2)
        empty = cnt_freq("empty_file.txt")
        anslist3 = [0] * 256
        self.assertListEqual(empty, anslist3)
        onechar = cnt_freq("single_char.txt")
        anslist4 = [0, 5, 0]
        self.assertListEqual(onechar[96:99], anslist4)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char_ascii, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char_ascii, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char_ascii, 100)
        # empty file
        empty = cnt_freq("empty_file.txt")
        huff1 = create_huff_tree(empty)
        self.assertEqual(huff1, None)
        # one char
        onechar = cnt_freq("single_char.txt")
        huff2 = create_huff_tree(onechar)
        self.assertEqual(huff2.freq, 5)
        self.assertEqual(huff2.right, None)
        self.assertEqual(huff2.left, None)
        self.assertEqual(huff2.char_ascii, 97)

    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")
        empty = cnt_freq("empty_file.txt")
        self.assertEqual(create_header(empty), "")
        onechar = cnt_freq("single_char.txt")
        self.assertEqual(create_header(onechar), "97 5")


    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        empty = cnt_freq("empty_file.txt")
        emptyhuff = create_huff_tree(empty)
        emptycodes = create_code(emptyhuff)
        emptylist = [''] * 256
        self.assertListEqual(emptycodes, emptylist)
        onechar = cnt_freq("single_char.txt")
        onehuff = create_huff_tree(onechar)
        onecodes = create_code(onehuff)
        self.assertEqual(onecodes[97], '')

    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1_out.txt", "file1_soln.txt"))
        huffman_encode("file2.txt", "file2_out.txt")
        self.assertTrue(compare_files("file2_out.txt", "file2_soln.txt"))
        huffman_encode("multiline.txt", "multiline_out.txt")
        self.assertTrue(compare_files("multiline_out.txt", "multiline_soln.txt"))
        huffman_encode("declaration.txt", "declaration_out.txt")
        self.assertTrue(compare_files("declaration_out.txt", "declaration_soln.txt"))
        huffman_encode("single_char.txt", "single_char_out.txt")
        self.assertTrue(compare_files("single_char_out.txt", "single_char_soln.txt"))
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        self.assertTrue(compare_files("empty_file_out.txt", "empty_file.txt"))
        with self.assertRaises(FileNotFoundError):
            huffman_encode("doesnotexist.txt", "no_output.txt")

    def test_parse_header(self):
        header = "97 2 98 4 99 8 100 16 102 2"
        freqlist = parse_header(header)
        anslist = [0]*256
        anslist[97:104] = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist[97:104])
        empty = ""
        emptylist = parse_header(empty)
        emptyanslist = [0] * 256
        self.assertListEqual(emptylist, emptyanslist)

    def test_decode_01(self):
        huffman_decode("file1_soln.txt", "file1_decode.txt")
        # detect errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("file1.txt", "file1_decode.txt"))

    def test_decode_02(self):
        huffman_decode("declaration_soln.txt", "declaration_decode.txt")
        # detect errors by comparing your encoded file with a *known* solution file
        self.assertTrue(compare_files("declaration.txt", "declaration_decode.txt"))

        huffman_decode("file2_soln.txt", "file2_decode.txt")
        self.assertTrue(compare_files("file2.txt", "file2_decode.txt"))

        huffman_decode("multiline_soln.txt", "multiline_decode.txt")
        self.assertTrue(compare_files("multiline.txt", "multiline_decode.txt"))

        huffman_decode("single_char_soln.txt", "single_char_decode.txt")
        self.assertTrue(compare_files("single_char.txt", "single_char_decode.txt"))

        huffman_decode("empty_file.txt", "empty_file_decode.txt")
        self.assertTrue(compare_files("empty_file.txt", "empty_file_decode.txt"))



# Compare files - takes care of CR/LF, LF issues
def compare_files(file1,file2):
    match = True
    done = False
    with open(file1, "r") as f1:
        with open(file2, "r") as f2:
            while not done:
                line1 = f1.readline().strip()
                line2 = f2.readline().strip()
                if line1 == '' and line2 == '':
                    done = True
                if line1 != line2:
                    done = True
                    match = False
    return match

if __name__ == '__main__':
   unittest.main()
