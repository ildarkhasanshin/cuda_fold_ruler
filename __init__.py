import os
from cudatext import *

FN_CONFIG = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
SECTION = 'fold_ruler'

class Command:
    def __init__(self):
        self.before = None
        self.lexers = ini_read(FN_CONFIG, SECTION, 'lexers', 'Python')

    def ruler_set(self, show_now, text = ''):

        if self.before is None:
            self.before = ed.get_prop(PROP_RULER)

        if show_now and self.before and not text:
            text = '-'

        ed.set_prop(PROP_RULER, show_now or self.before)
        ed.set_prop(PROP_RULER_TEXT, text)

    def ruler_restore(self):
        self.ruler_set(self.before or False)

    def get_fold_block(self, y):
        for fold in reversed(ed.folding(FOLDING_GET_LIST)):
            f0 = fold[0]
            f1 = fold[1]
            if f0 < y <= f1 and ((f1 - f0) > 1):
                return f0

    def work(self):
        res = self.get_fold_block(ed.get_carets()[0][1])
        if res is not None:
            self.ruler_set(True, ed.get_text_line(res).strip())
        else:
            self.ruler_restore()

    def on_caret_slow(self, ed_self):
        
        lexer = ed_self.get_prop(PROP_LEXER_FILE)
        if ','+lexer+',' in ','+self.lexers+',':
            self.work()

    def on_exit(self, ed_self):

        self.ruler_restore()

    def config(self):

        ini_write(FN_CONFIG, SECTION, 'lexers', self.lexers)
        file_open(FN_CONFIG)
        with open(FN_CONFIG, mode='r', encoding='utf-8') as f:
            lines = f.read().splitlines()

        try:
            index = lines.index('['+SECTION+']')
            ed.set_caret(0, index)
        except:
            pass
