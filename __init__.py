import os
from cudatext import *


class Command:
    def __init__(self):
        self.ruler_init = ed.get_prop(PROP_RULER)

    def ruler_set(self, bool_show, text = ''):
        ed.set_prop(PROP_RULER, bool_show)
        ed.set_prop(PROP_RULER_TEXT, text)

    def check_ruler_init(self):
        if self.ruler_init:
            self.ruler_set(True)
        else:
            self.ruler_set(False)

    def get_fold_block(self, y):
        for fold in reversed(ed.folding(FOLDING_GET_LIST)):
            fold_0 = fold[0]
            fold_1 = fold[1]
            if y >= fold_0 and y <= fold_1 and y != fold_0 and ((fold_1 - fold_0) > 1):
                return fold_0
        return

    def fr(self):
        res = self.get_fold_block(ed.get_carets()[0][1])
        if res is not None:
            self.ruler_set(True, ed.get_text_line(res).strip())
        else:
            self.check_ruler_init()

    def on_caret_slow(self, ed_self):
        self.fr()

    def on_exit(self, ed_self):
        self.check_ruler_init()
