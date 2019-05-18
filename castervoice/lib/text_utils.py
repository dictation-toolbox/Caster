import time


from castervoice.lib.actions import Key, Text
from castervoice.lib import settings, context

def master_text_nav(mtn_mode, mtn_dir, nnavi500, extreme):
    '''
    (<mtn_dir> | <mtn_mode> [<mtn_dir>]) [(<nnavi500> | <extreme>)]
    mtn_mode: "shin" s, "queue" cs, "fly" c, (default None)
    mtn_dir: 0-up, 1-down, 2-left, 3-right, (default right)
    nnavi500: number of keypresses (default 1)
    extreme: home/end (default None)
    '''

    k = None
    if mtn_mode is None:
        if extreme is not None:
            if mtn_dir == "left":
                k = "home"
            elif mtn_dir == "right":
                k = "end"
            elif mtn_dir == "up":
                k = "c-home"
            elif mtn_dir == "down":
                k = "c-end"
        else:
            k = str(mtn_dir) + "/5:" + str(nnavi500)
    elif extreme is None:
        k = str(mtn_mode) + "-" + str(mtn_dir) + "/5:" + str(nnavi500)
    else:
        mtn_dir = str(mtn_dir)
        way = "end" if mtn_dir in ["right", "down"] else "home"
        k = str(mtn_mode) + "-" + str(way)
    Key(k).execute()
    time.sleep(settings.SETTINGS["miscellaneous"]["keypress_wait"]/1000.)


def enclose_selected(enclosure):
    ''' 
    Encloses selected text in the appropriate enclosures
    By using the system Clipboard as a buffer ( doesn't delete previous contents)
    '''

    (err, selected_text) = context.read_selected_without_altering_clipboard(True)
    if err == 0:
        opener = enclosure.split('~')[0]
        closer = enclosure.split('~')[1]
        enclosed_text = opener + selected_text + closer
        # Attempt to paste enclosed text without altering clipboard
        if not context.paste_string_without_altering_clipboard(enclosed_text):
            print("failed to paste {}".format(enclosed_text))