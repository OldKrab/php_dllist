import gdb


def color_address(address):
    blue = "\x1b[34m"
    normal = "\x1b[0m"
    return blue + "%#x" % (address) + normal


def traverse_list(head, next_field_name, len=-1) -> list[int]:
    if head == 0 or len == 0:
        return []
    result = [head]
    head = head[next_field_name]
    while head != 0 and len != 1:
        result.append(head)
        head = head[next_field_name]
        len -= 1
    return result


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

        elems = traverse_list(head, "next")
        return " —▸ ".join(map(color_address, elems))

    def to_string(self):
        return "\ntraverse_position = %d\n" % (self.val["traverse_position"]) \
            + "traverse_pointer = %s\n" % (color_address(self.val["traverse_pointer"])) \
            + "List elements:\n" + self._elements_to_str()


def dllist_lookup_function(val):
    typename = gdb.types.get_basic_type(val.type).name
    if typename == "_spl_dllist_object":
        return DllistPrettyPrinter(val)


class SmallBinsCmd(gdb.Command):
    """Prints the ListNode from our example in a nice format!"""

    def __init__(self):
        super(SmallBinsCmd, self).__init__(
            "small_bins", gdb.COMMAND_DATA
        )

    def invoke(self, args, from_tty):
        alloc_globals = gdb.selected_frame().read_var('alloc_globals')
        heap = alloc_globals['mm_heap'].dereference()
        slots_count = heap["free_slot"].type.sizeof // heap["free_slot"].dereference().type.sizeof
        max_list_len = 5

        for i in range(slots_count):
            elems = traverse_list(
                heap["free_slot"][i], "next_free_slot", max_list_len + 1)

            elems_str = " —▸ ".join(map(color_address, elems[0: max_list_len]))
            rest = " ..." if len(elems) > max_list_len else " ◂— 0x0" if len(
                elems) > 0 else "0x0"

            print("[%d]: %s%s" % (i, elems_str, rest))


gdb.pretty_printers.append(dllist_lookup_function)
SmallBinsCmd()
