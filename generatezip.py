#!/usr/bin/env python
import sys
import os
from shutil import copyfile
from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw.objects import PdfDict, PdfArray, PdfName


def addmark(i,n):
    wmark_trailer = PdfReader("dot.pdf")
    wmark = PageMerge().add(wmark_trailer.pages[0])[0]
    wmark.scale(0.2)
# left : 94  right: 217
# top: 567 bottom: 410
    wmark.x = 94. + (217.-94.)/8.*i
    wmark.y = 566. - (566.-410.)/9.*n
    PageMerge(trailer.pages[0]).add(wmark).render()

j = 0
def render(self):
    def do_xobjs(xobj_list):
        global j
        content = []
        for obj in xobj_list:
            index = PdfName('pdfrw_%d' % (j))
            j=j+1
            if xobjs.setdefault(index, obj) is not obj:
                raise KeyError("XObj key %s already iiiin use" % index)
            content.append('%s Do' % index)
        return PdfDict(indirect=True, stream='\n'.join(content))

    mbox = self.mbox
    cbox = self.cbox
    page = self.page
    old_contents = self.contents
    resources = self.resources or PdfDict()

    key_offset = 0
    xobjs = resources.XObject
    if xobjs is None:
        xobjs = resources.XObject = PdfDict()
    else:
        allkeys = xobjs.keys()
        if allkeys:
            keys = (x for x in allkeys if x.startswith('/pdfrw_'))
            keys = (x for x in keys if x[6:].isdigit())
            keys = sorted(keys, key=lambda x: int(x[6:]))
            key_offset = (int(keys[-1][6:]) + 1) if keys else 0
            key_offset -= len(allkeys)

    if old_contents is None:
        new_contents = do_xobjs(self)
    else:
        isdict = isinstance(old_contents, PdfDict)
        old_contents = [old_contents] if isdict else old_contents
        new_contents = PdfArray()
        index = self.index(None)
        if index:
            new_contents.append(do_xobjs(self[:index]))
        new_contents.extend(old_contents)
        index += 1
        if index < len(self):
            new_contents.append(do_xobjs(self[index:]))

    if mbox is None:
        cbox = None
        mbox = self.xobj_box
        mbox[0] = min(0, mbox[0])
        mbox[1] = min(0, mbox[1])

    page = PdfDict(indirect=True) if page is None else page
    page.Type = PdfName.Page
    page.Resources = resources
    page.MediaBox = mbox
    page.CropBox = cbox
    page.Rotate = self.rotate
    page.Contents = new_contents
    return page

#Monkey patch
PageMerge.render = render

def getzipwithstudentid(outfile, sid):
    global trailer
    trailer = PdfReader("zip100.pdf")
    for i,n in enumerate(list(map(int,str(sid)))):
        addmark(i,n)
    PdfWriter().write(outfile, trailer)

