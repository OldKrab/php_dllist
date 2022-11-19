import gdb


def color_address(address):
    blue = "\x1b[34m"
    normal = "\x1b[0m"
    return blue + "%#x" % (address) + normal


class DllistPrettyPrinter(object):
    def __init__(self, val):
        self.val = val

    def _elements_to_str(self):
        llist = self.val["llist"]
        if llist == 0:
            return "llist in NULL"

        head = llist["head"]
        if head == 0:
            return "llist is empty"

        result = color_address(head)
        head = head["next"]
        while head != 0:
            result += " —▸ " + color_address(head)
            head = head["next"]
        return result

    def to_string(self):
        return "\ntraverse_position = %d\n" % (self.val["traverse_position"]) \
            + "traverse_pointer = %s\n" % (color_address(self.val["traverse_pointer"])) \
            + "List elements:\n" + self._elements_to_str()

def dllist_lookup_function(val):
    typename = gdb.types.get_basic_type(val.type).name
    if typename == "_spl_dllist_object":
        return DllistPrettyPrinter(val)


gdb.pretty_printers.append(dllist_lookup_function)
