# -*- coding: utf-8 -*-

from __future__ import division, absolute_import, print_function
import os
from musicscout.util import confit

class IncludeLazyConfig(confit.LazyConfig):
    """A version of Confit's LazyConfig that also merges in data from
    YAML files specified in an `include` setting.
    """
    def read(self, user=True, defaults=True):
        super(IncludeLazyConfig, self).read(user, defaults)

        try:
            for view in self['include']:
                filename = view.as_filename()
                if os.path.isfile(filename):
                    self.set_file(filename)
        except confit.NotFoundError:
            pass

config = IncludeLazyConfig('musicscout', __name__)
