ObjC.import('Cocoa');
ObjC.import('Quartz');
function run(argv) {
    var pdfPath = argv[0], outDir = argv[1], scale = parseFloat(argv[2] || "1.5");
    var url = $.NSURL.fileURLWithPath(pdfPath);
    var doc = $.PDFDocument.alloc.initWithURL(url);
    var n = doc.pageCount;
    $.NSFileManager.defaultManager.createDirectoryAtPathWithIntermediateDirectoriesAttributesError(outDir, true, $(), null);
    for (var i = 0; i < n; i++) {
        var page = doc.pageAtIndex(i);
        var bounds = page.boundsForBox($.kPDFDisplayBoxMediaBox);
        var w = Math.round(bounds.size.width * scale), h = Math.round(bounds.size.height * scale);
        var img = $.NSImage.alloc.initWithSize($.NSMakeSize(w, h));
        img.lockFocus;
        $.NSColor.whiteColor.set;
        $.NSRectFill($.NSMakeRect(0, 0, w, h));
        var ctx = $.NSGraphicsContext.currentContext;
        ctx.saveGraphicsState;
        var t = $.NSAffineTransform.transform;
        t.scaleXByYBy(scale, scale);
        t.concat;
        page.drawWithBoxToContext($.kPDFDisplayBoxMediaBox, ctx.CGContext);
        ctx.restoreGraphicsState;
        img.unlockFocus;
        var tiff = img.TIFFRepresentation;
        var rep = $.NSBitmapImageRep.imageRepWithData(tiff);
        var png = rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $());
        var num = ("00" + (i + 1)).slice(-3);
        png.writeToFileAtomically(outDir + "/page-" + num + ".png", true);
    }
    return "done " + n;
}
