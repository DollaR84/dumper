"""
Main module for running dumper.

Created on 16.03.2018

@author: Ruslan Dolovanyuk

"""

from drawer import Drawer

from dumper import Dumper


if __name__ == '__main__':
    dumper = Dumper()
    drawer = Drawer(dumper)
    drawer.mainloop()
