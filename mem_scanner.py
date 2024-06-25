class mem_scanner:
    mem_object = []
    lower_bound = 0x0000
    upper_bound = 0xFFFF
    mode = "match"
    val = 0

    matches = []
    matches_index = []

    def __init__ (self, mem_object, lower_bound = 0xC000, upper_bound = 0xDFFF, mode = "match", val = 0):
        self.mem_object = mem_object
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.mode = mode
        self.val = val
        
    def update_mem (self, mem_object):
        self.mem_object = mem_object
        for i in range (0, len(self.matches)):
            self.matches[i] = self.mem_object[self.matches_index[i]]

    def set_mode (self, mode):
        self.mode = mode

    def set_bounds(self, lower_bound = 0xC000, upper_bound=0xDFFF):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def set_val(self, val):
        self.val = val

    def init_scan (self):
        for i in range (self.lower_bound, self.upper_bound):
            self.matches.append(self.mem_object[i])
            self.matches_index.append(i)

    def scan (self):

        if (self.mode == "match"):
            self.matches, self.matches_index = filter_lists_match(self.matches, self.matches_index, self.val)



def filter_lists_match(first, second, target):
    first_filtered = []
    second_filtered = []

    for i, element in enumerate(first):
        if element == target:
            first_filtered.append(element)
            second_filtered.append(second[i])
    
    return first_filtered, second_filtered