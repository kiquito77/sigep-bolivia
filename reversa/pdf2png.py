import sys, pymupdf
src, dst = sys.argv[1], sys.argv[2]
doc = pymupdf.open(src)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=130)
    out = dst if len(doc) == 1 else dst.replace(".png", f"_{i+1}.png")
    pix.save(out)
    print("PNG:", out, pix.width, "x", pix.height)
