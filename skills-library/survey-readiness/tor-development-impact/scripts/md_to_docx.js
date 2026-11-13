#!/usr/bin/env node
// Convert a TOR written in the template's Markdown subset into a Word file.
// Usage: node md_to_docx.js tor.md out.docx
// Handles: # title, ## and ### headings, paragraphs, - bullets (two levels), pipe tables, > notes,
// **bold**, [text](url), and [[placeholders]] (shown highlighted yellow so unfilled ones stand out).
// Needs the "docx" npm package. If it is missing, use: pandoc tor.md -o out.docx
const D = require('docx');
const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, AlignmentType,
  HeadingLevel, LevelFormat, Footer, PageNumber, ExternalHyperlink } = D;

function runs(str, base = {}) {
  const out = [];
  str.split(/(\[\[.*?\]\]|\*\*.*?\*\*|\[[^\]]+\]\([^)]+\))/g).forEach(part => {
    if (!part) return;
    if (part.startsWith('[[')) out.push(new TextRun({ ...base, text: '[' + part.slice(2, -2) + ']', highlight: 'yellow' }));
    else if (part.startsWith('**')) out.push(...runs(part.slice(2, -2), { ...base, bold: true }));
    else if (/^\[[^\]]+\]\([^)]+\)$/.test(part)) {
      const m = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      out.push(new ExternalHyperlink({ link: m[2], children: [new TextRun({ ...base, text: m[1], color: '0563C1', underline: {} })] }));
    } else out.push(new TextRun({ ...base, text: part }));
  });
  return out;
}
const thin = { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6' };
const borders = { top: thin, bottom: thin, left: thin, right: thin };

function table(lines) {
  const rows = lines.filter((l, i) => i !== 1).map(l => l.trim().replace(/^\||\|$/g, '').split(' | ').map(c => c.trim()));
  const n = rows[0].length, total = 9360;
  const len = Array.from({ length: n }, (_, i) => Math.min(60, Math.max(8, ...rows.map(r => (r[i] || '').length))));
  const sum = len.reduce((a, b) => a + b, 0);
  let widths = len.map(x => Math.floor(total * x / sum));
  widths[n - 1] += total - widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: ri === 0, children: widths.map((w, ci) => new TableCell({
      width: { size: w, type: WidthType.DXA }, borders, margins: { top: 60, bottom: 60, left: 100, right: 100 },
      shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'E7E6E6', color: 'auto' } : undefined,
      children: [new Paragraph({ children: runs(ri === 0 && !(r[ci] || '').startsWith('**') ? '**' + (r[ci] || '') + '**' : (r[ci] || ''), { size: 20 }) })]
    })) }))
  });
}

const src = fs.readFileSync(process.argv[2], 'utf8').replace(/<!--[\s\S]*?-->/g, '').split('\n');
const kids = [];
for (let i = 0; i < src.length; i++) {
  const l = src[i];
  if (!l.trim()) continue;
  if (l.startsWith('|')) {
    const blk = [];
    while (i < src.length && src[i].startsWith('|')) blk.push(src[i++]);
    i--;
    kids.push(table(blk), new Paragraph({ children: [], spacing: { after: 120 } }));
  } else if (l.startsWith('# ')) kids.push(new Paragraph({ heading: HeadingLevel.TITLE, alignment: AlignmentType.CENTER, children: runs(l.slice(2)) }));
  else if (l.startsWith('## ')) kids.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(l.slice(3)) }));
  else if (l.startsWith('### ')) kids.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: runs(l.slice(4)) }));
  else if (/^\s*- /.test(l)) kids.push(new Paragraph({ children: runs(l.replace(/^\s*- /, '')), numbering: { reference: 'bul', level: /^\s{2,}- /.test(l) ? 1 : 0 }, spacing: { after: 80 } }));
  else if (l.startsWith('> ')) kids.push(new Paragraph({ children: runs(l.slice(2), { italics: true, color: '595959', size: 19 }), shading: { type: ShadingType.CLEAR, fill: 'F2F2F2', color: 'auto' }, spacing: { after: 120 } }));
  else kids.push(new Paragraph({ children: runs(l), spacing: { after: 120 }, keepNext: /^\*\*.*\*\*$/.test(l.trim()) }));
}
const doc = new Document({
  styles: {
    default: { document: { run: { font: 'Arial', size: 21 } } },
    paragraphStyles: [
      { id: 'Title', name: 'Title', basedOn: 'Normal', run: { font: 'Arial', size: 32, bold: true }, paragraph: { spacing: { before: 0, after: 200 }, keepNext: true } },
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Arial', size: 26, bold: true }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: 'Arial', size: 23, bold: true }, paragraph: { spacing: { before: 200, after: 100 }, keepNext: true, outlineLevel: 1 } }
    ]
  },
  numbering: { config: [{ reference: 'bul', levels: [
    { level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
    { level: 1, format: LevelFormat.BULLET, text: '\u2013', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1260, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
    children: kids
  }]
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[3], b); console.log('written ' + process.argv[3]); });
