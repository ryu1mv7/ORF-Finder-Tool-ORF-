

class Node:
    
    def __init__(self, datstart_index=None,level = None, size = 5) -> None:
        """
    Function description:
        This is the constructor of Node for suffix trie
    Approach description: 
        One node has the list(self.link) that contain the another node(child node). 
        index of the list is the role of ABCD.
        In other words, one cell in the list points to its child node.
        self.start_index and self.end_index will have the possible index of substring of genome.
        These will be used to find all combinations of [start: end] for the substring
        These indices are meant to be used in slice in find()
        
    Input:
        string(genome): non-empty string consisting only of uppercase ABCD
    Return:
        None
    Time complexity: O(1)
        Time complexity analysis: size is fixed (=5) because ABCD are the only characters we consider, so take as constant operation
    Space complexity: O(N) where N is the length of genome 
        Input space analysis: O(1) bcs size is constant 
        Aux space analysis: even in the worst case, start and end index is within the length of the character, so O(N)
        """
        self.link = [None] * size # non-none represents existence of the character($ or  ABCD)
        # data (pay-load)
        self.start_index = [] 
        self.end_index = []
        

class OrfFinder:
    def __init__(self, string) -> None:
        """
    Function description:
        This is the constructor of OrfFinder
    Approach description: 
        get a input string and instance of the root node for suffix trie.And from the input string, I make a suffix trie.
        I will explain about make_suffix_trie() in the docstring of the function.
    Input:
        string(genome): non-empty string consisting only of uppercase ABCD
    Return:
        None
    Time complexity: O(N^2) where N is the length of genome
        Time complexity analysis: making suffix trie takes O(N^2) but I will write the detal in that function. Others takes O(1)
    Space complexity: O(N) where N is the length of genome
        Input space analysis: O(N) for all 3 attributes and input string
        Aux space analysis: O(N) where N is the length of genome for all 3 attributes
        """
        self.string = string
        self.root = Node(level = 0) # node obj of the root
        self.make_suffix_trie(string)
        
    def insert(self, key,insert_start_index):
        """
    Function description:
        This function itself is to make prefix trie of input string(key)
    Approach description:
        When I insert each key in prefix trie, I store the start index and end index in the pay load.
        
        Then when I search the key, I get all possible start and end position(index) of the substring.
        In all insert operations for making suffix trie, The more I go through the same path, the more indices the node have.
        Fore example, When I insert "AAABBBCCC" as key,  
        ()... node, (a,b)... a is the list of start index, bi is the one of end index
        (root)--A--([0],[0])--A--([0],[1])--A--([0],[2])--B--([0],[3])--B--([0],[4])--B--([0],[5])--C--([0],[6])--C--([0],[7])--C--([0],[8])--$--()
        difference_btw_start_end is used to calculate the end index based on start index
        These indices are meant to be used in slice in find()
    Time complexity: O(N) where N is the length of genome
        Time complexity analysis: loop iterate the length of key times, which takes O(N)
    Space complexity: O(N) where N is the length of genome
        Input space analysis: key is the string, so O(N)
        Aux space analysis: in the worst case, instanciate Node takes O(N) space
        """
        current = self.root
        output = ""
        difference_btw_start_end = 0
        for i in range(insert_start_index, len(key)): #
            char = key[i]
            output += str(char)
            #calculate index for self.link from the char 
            index = ord(char) - 64 #ABCD
            # if there is a path I still can go through (can traverse the path alr exist)
            if current.link[index] is not None:
                current = current.link[index] # just go to the next node
                current.start_index.append(insert_start_index)
                current.end_index.append(insert_start_index + difference_btw_start_end)
                difference_btw_start_end += 1
            else:
                new_node = Node() #create new child node put it
                current.link[index] = new_node
                current = current.link[index]
                current.start_index.append(insert_start_index)
                current.end_index.append(insert_start_index + difference_btw_start_end)
                difference_btw_start_end += 1
                
        # reach here after traversing all char of the string
        if current.link[0] is not None:
                current = current.link[0] # just go to the next node
        else:
                new_node = Node() #create new node and 
                current.link[0] = new_node
                current = current.link[0]
        current.start_index.append(insert_start_index)
        current.end_index.append(insert_start_index + difference_btw_start_end)
        difference_btw_start_end += 1
                
    def make_suffix_trie(self,string):
        """
        Function description:
            This is the function is used to insert characters to make suffix trie of the genome
        Approach description:
            Fore example, When I finish insert "AAABBBCCC" as string, one payload of suffix trie will be like below
            ()... node, (a,b)... a is the list of start index, bi is the one of end index
            (root)--A--([0,1,2],[0,1,2])--A--([0,1],[1,2])--A--([0],[2])--B--([0],[3])--B--([0],[4])--B--([0],[5])--C--([0],[6])--C--([0],[7])--C--([0],[8])--$--()
            The nodes in lower level have more indices because I go through more times during all insertions.
        Time complexity: O(N^2) where N is the length of genome
        Time complexity analysis: insert() takes O(N) but iterate it O(N/2) times so O(N)
        Space complexity: O(N) where N is the length of genome
        Input space analysis: input strings take O(N)
        Aux space analysis: insert()takes O(N)
        """
        for insert_start_index in range(len(string)): # inserting all char, 1st-last char, 2nd-last char... achieve to make suffix trie
            self.insert(string,insert_start_index)

    def search(self, key):
        """ 
        Function description:
            This function search the string(key) and return the start indices and end indices for that paticular key
        Approach description:
             Fore example, When I finish insert "AAABBBCCC" as string, one payload of suffix trie will be like below
            ()... node, (a,b)... a is the list of start index, bi is the one of end index
            (root)--A--([0,1,2],[0,1,2])--A--([0,1],[1,2])--A--([0],[2])--B--([0],[3])--B--([0],[4])--B--([0],[5])--C--([0],[6])--C--([0],[7])--C--([0],[8])--$--()
            If I search the key of "AA", this function returns ([0,1],[1,2])
                substring of start is AA, it possibly start at either 0 or 1
                substring of end is AA, it possibly end at either 1 or 2
            These indices are meant to be used in slice in find()
        Time complexity: O(N) where N is the length of genome
        Time complexity analysis: loop iterate the length of key times, which takes O(N)
        Space complexity: O(N) where N is the length of genome
        Input space analysis: key is the string, so O(N)
        Aux space analysis: in the worst case, instanciate Node takes O(N) space
        """
        current = self.root
        for char in key:
            #calculate index for self.link from the char 
            index = ord(char) - 64
            # if there is a path I still can go through (can traverse the path alr exist)
            if current.link[index] is not None:
                current = current.link[index] # just go to the next node
            # if there is no path (= no string I am looking for)
            else:
                return None, None #When try to get the substring that prefix or suffix(start or end) does not exist
        return current.start_index, current.end_index # return the data when I reach the $ (key exist in the trie)

    def find(self, start, end):
        """
    Function description:
        This is the function returns a list of strings that contains all substring of genome which start as a prefix and end as a suffix.
     Approach description: 
        After I get a genome in constractor, I firstly find the start indices and end indices from the each given input, start, end.
        Then I find the all possible combination of those start indices and end indices for slice to find all combination of substrings
        that starts given input start and end. By putting combination to prevent overlapping, I added the condition in the code also.
        These indices are meant to be used in slice in find()
        
    Input:
        start: consisting only of uppercase ABCD, string type 
        end: consisting only of uppercase ABCD,string type
    Return:
        substrings: the list contains all substrings that starts with start(input), end with end(input)
    Time complexity: O(T+U+V) where T is the length of the string, start, U is the length of the string, end, V is the number of characters in the output list
        Time complexity analysis: two search takes O(T+U) in total, combination of start and end index make the substrings that total number of characters are V.
    Space complexity: O(T+U+V) where V is the number of characters in the output list
        Input space analysis: O(T+U) for the input key
        Aux space analysis: O(V) for substrings, 
        """
        substrings = []
        string = self.string
        #search --> data  O(T)
        start_index = self.search(start)[0] # get possible indices(for start and end) of the key
        #search --> data  O(U)
        end_index = self.search(end)[1] # get possible indices(for start and end) of the key
         # When try to get the substring that prefix or suffix(start or end) does not exist, return empty list
        if start_index is None or end_index is None:
            return substrings
        #O(V)
        length_start = len(start)
        length_end = len(end)
        for i in start_index:
            for j in end_index:
                if i + length_start - 1 < j - length_end + 1: #prevent overlap
                    substrings.append(string[i:j+1])
        return substrings