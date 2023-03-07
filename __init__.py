import os
from cudatext import *


class Command:
    def get_fold_block(self, y):
        for fold in reversed(ed.folding(FOLDING_GET_LIST)):
            fold_0 = fold[0]
            fold_1 = fold[1]
            if y >= fold_0 and y <= fold_1 and y != fold_0 and ((fold_1 - fold_0) > 1):
                return fold_0
        return

    def sfl(self):
        res = self.get_fold_block(ed.get_carets()[0][1])
        if res is not None:
            ed.set_prop(PROP_RULER, True)
            ed.set_prop(PROP_RULER_TEXT, ed.get_text_line(res).strip())
        else:
            ed.set_prop(PROP_RULER, False)
            ed.set_prop(PROP_RULER_TEXT, '')

    def on_caret_slow(self, ed_self):
        self.sfl()
