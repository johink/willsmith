"""
Collection of functions for adjusting hex coordinates.

All directions are in reference to flat-topped hexes.  The dir_changes 
dictionary is used to dynamically generate all of the move operations on 
module import.  

Dynamic function names are all in the form cubic_dir or axial_dir.
"""


from sys import modules


_current_module = modules[__name__]


_dir_changes = {"north" : (0, 1, -1), "south" : (0, -1, 1), 
                "n_east" : (1, 0, -1), "s_east" : (1, -1, 0),
                "n_west" : (-1, 1, 0), "s_west" : (-1, 0, 1),
                "east" : (2, -1, -1), "west" : (-2, 1, 1)}

def axial_to_cubic(col, slant):
    """
    Convert axial coordinate to its cubic equivalent.
    """
    x = col
    z = slant
    y = -x - z
    return x, y, z

def cubic_to_axial(x, y, z):
    """
    Convert cubic coordinate to its axial equivalent.
    """
    return x, z

def cubic_n_moves(f, n, x, y, z):
    """
    Return coordinate moved n hexes by the action defined in f.
    """
    for _ in range(n):
        x, y, z = f(x, y, z)
    return x, y, z

def axial_n_moves(f, n, col, slant):
    """
    Return coordinate moved n hexes by the action defined in f.
    """
    for _ in range(n):
        col, slant = f(col, slant)
    return col, slant

def _cubic_move_gen(delta):
    def f(x, y, z):
        return tuple([a + b for a, b in zip((x, y, z), delta)])
    return f

def _axial_move_gen(delta):
    def f(col, slant):
        cubic = axial_to_cubic(col, slant)
        return cubic_to_axial(*tuple([a + b for a, b in zip(cubic, delta)]))
    return f

for name, tup in _dir_changes.items():
    f = _cubic_move_gen(tup)
    setattr(_current_module, "cubic_" + name, f)

    g = _axial_move_gen(tup)
    setattr(_current_module, "axial_" + name, g)

# clean up module namespace after the function generation
delattr(_current_module, "f")
delattr(_current_module, "g")
delattr(_current_module, "name")
delattr(_current_module, "tup")
