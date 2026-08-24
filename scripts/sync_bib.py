#!/usr/bin/env python3
"""Regenerate the publications/talks lists in _pages/publications.md from the
Overleaf CV bib.

Source of truth is overleaf_cv/cvRef.bib (a private, gitignored clone --
never committed, never referenced by URL). Edit the .bib, not the page;
re-running this script overwrites only the content between the generated
markers in _pages/publications.md and leaves the rest of the page alone.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

REPO_ROOT = Path(__file__).resolve().parent.parent
OVERLEAF_DIR = Path(os.environ.get("OVERLEAF_DIR", str(REPO_ROOT / "overleaf_cv")))
BIB_FILE = OVERLEAF_DIR / "cvRef.bib"

PUBLICATIONS_PAGE = REPO_ROOT / "_pages" / "publications.md"

PUB_MARKER_BEGIN = "<!-- BEGIN GENERATED PUBLICATIONS: edit overleaf_cv/cvRef.bib and run scripts/sync_bib.py, do not hand-edit -->"
PUB_MARKER_END = "<!-- END GENERATED PUBLICATIONS -->"
TALK_MARKER_BEGIN = "<!-- BEGIN GENERATED TALKS: edit overleaf_cv/cvRef.bib and run scripts/sync_bib.py, do not hand-edit -->"
TALK_MARKER_END = "<!-- END GENERATED TALKS -->"

MONTHS = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}

def refresh_overleaf_clone():
    if not (OVERLEAF_DIR / ".git").exists():
        print(f"warning: {OVERLEAF_DIR} is not a git clone; skipping refresh", file=sys.stderr)
        return
    try:
        subprocess.run(
            ["git", "-C", str(OVERLEAF_DIR), "pull", "--ff-only"],
            check=True, capture_output=True, text=True, timeout=20,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        detail = exc.stderr if isinstance(exc, subprocess.CalledProcessError) else exc
        print(f"warning: could not refresh Overleaf clone ({detail}); using existing checkout",
              file=sys.stderr)

SELF_MARKER_RE = re.compile(r"\\textbf\{([^{}]*)\}")

def strip_latex(text):
    if not text:
        return text
    text = re.sub(r"\\textit\{([^{}]*)\}", r"<i>\1</i>", text)
    text = re.sub(r"\\textbf\{([^{}]*)\}", r"<b>\1</b>", text)
    text = text.replace(r"\&", "&")
    text = text.replace("{", "").replace("}", "")
    return text.strip()

def parse_name(raw):
    """Return (display_name, is_self) for one 'and'-separated author segment."""
    is_self = bool(SELF_MARKER_RE.search(raw))
    cleaned = SELF_MARKER_RE.sub(r"\1", raw).strip()
    cleaned = cleaned.replace("{", "").replace("}", "")
    if "," in cleaned:
        family, given = cleaned.split(",", 1)
        full = f"{given.strip()} {family.strip()}".strip()
    else:
        full = cleaned
    return full, is_self

def format_authors(raw):
    segments = re.split(r"\s+and\s+", raw.strip())
    et_al = False
    if segments and segments[-1].strip().lower() == "others":
        et_al = True
        segments = segments[:-1]
    names = []
    for seg in segments:
        full, is_self = parse_name(seg)
        names.append(f"<b>{full}</b>" if is_self else full)
    if et_al:
        joined = ", ".join(names) + ", et al"
    elif len(names) == 1:
        joined = names[0]
    elif len(names) == 2:
        joined = f"{names[0]} and {names[1]}"
    else:
        joined = ", ".join(names[:-1]) + ", and " + names[-1]
    # Every citation template appends its own sentence period after the
    # author block; strip a stray one from a malformed bib name (e.g. a
    # trailing "R." with no comma) so it doesn't double up.
    return joined.rstrip(".")

def format_date_paren(entry):
    year = entry.get("year", "").strip()
    month = entry.get("month", "").strip()
    if month and month in MONTHS:
        return f"{MONTHS[month]} {year}"
    return year

def iso_date(entry):
    year = (entry.get("year", "") or "0000").strip() or "0000"
    month = (entry.get("month", "") or "01").strip() or "01"
    day = (entry.get("day", "") or "01").strip() or "01"
    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"

def format_pages(pages):
    pages = pages.strip()
    sep = "--" if "--" in pages else ("-" if "-" in pages else None)
    if sep:
        lo, hi = pages.split(sep, 1)
        return f"pp. {lo.strip()}\u2013{hi.strip()}"
    return f"p. {pages}"

def doi_link(doi):
    doi = doi.strip()
    return f'<a href="https://doi.org/{doi}">{doi}</a>'

def build_citation(entry):
    kind = entry["ENTRYTYPE"].lower()
    authors = format_authors(entry.get("author", ""))
    title = strip_latex(entry.get("title", ""))

    if kind == "article":
        journal = strip_latex(entry.get("journal", ""))
        date = format_date_paren(entry)
        citation = f'{authors}. "{title}". In: <i>{journal}</i> ({date})'
        if entry.get("pages"):
            citation += f", {format_pages(entry['pages'])}"
        citation += "."
        if entry.get("issn"):
            citation += f" ISSN: {entry['issn'].strip()}."
        if entry.get("doi"):
            citation += f" DOI: {doi_link(entry['doi'])}."
        return citation

    if kind == "inproceedings":
        booktitle = strip_latex(entry.get("booktitle", ""))
        citation = f'{authors}. "{title}". In: <i>{booktitle}</i>.'
        if entry.get("volume"):
            citation += f" Vol. {entry['volume'].strip()}."
        org = entry.get("organization") or entry.get("publisher")
        if org:
            citation += f" {strip_latex(org)}."
        year = entry.get("year", "").strip()
        if entry.get("pages"):
            citation += f" {year}, {format_pages(entry['pages'])}."
        else:
            citation += f" {year}."
        return citation

    if kind == "techreport":
        institution = strip_latex(entry.get("institution", ""))
        number = entry.get("number", "").strip()
        year = entry.get("year", "").strip()
        citation = f"{authors}. <i>{title}</i>. Tech. rep."
        if number:
            citation += f" {number}."
        citation += f" {institution}, {year}."
        return citation

    if kind != "misc":
        print(f"warning: unrecognised entry type '{kind}' for {entry.get('ID')}; "
              "falling back to @misc-style citation", file=sys.stderr)
    howpublished = strip_latex(entry.get("howpublished", ""))
    date = format_date_paren(entry)
    citation = f'{authors}. "{title}".'
    if howpublished:
        citation += f" {howpublished}."
    if date:
        citation += f" {date}."
    return citation

def keywords_of(entry):
    return [k.strip() for k in entry.get("keywords", "").split(",") if k.strip()]

def sorted_newest_first(entries):
    # Mirrors Jekyll's previous `site.collection reversed` behaviour: ascending
    # sort by (date, bibkey), then reverse the whole list.
    ordered = sorted(entries, key=lambda e: (iso_date(e), e["ID"]))
    ordered.reverse()
    return ordered

def render_list(entries):
    lines = ['<ul class="bib-list">']
    for entry in entries:
        lines.append(f"  <li>{build_citation(entry)}</li>")
    lines.append("</ul>")
    return "\n".join(lines)

def inject(text, begin_marker, end_marker, content):
    pattern = re.compile(
        re.escape(begin_marker) + r".*?" + re.escape(end_marker), re.DOTALL
    )
    replacement = f"{begin_marker}\n{content}\n{end_marker}"
    new_text, count = pattern.subn(replacement, text)
    if count != 1:
        print(f"error: expected exactly one '{begin_marker}' block in {PUBLICATIONS_PAGE}, "
              f"found {count}", file=sys.stderr)
        sys.exit(1)
    return new_text

def main():
    if not BIB_FILE.exists():
        print(f"error: bib file not found at {BIB_FILE}", file=sys.stderr)
        print("Set OVERLEAF_DIR to point at the Overleaf CV clone.", file=sys.stderr)
        sys.exit(1)

    refresh_overleaf_clone()

    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with BIB_FILE.open(encoding="utf-8") as f:
        bib_database = bibtexparser.load(f, parser=parser)

    publications, talks = [], []
    for entry in bib_database.entries:
        keywords = set(keywords_of(entry))
        if "publications" in keywords:
            publications.append(entry)
        elif "conference" in keywords:
            talks.append(entry)
        else:
            print(f"warning: entry '{entry.get('ID')}' has no publications/conference "
                  "keyword; skipped", file=sys.stderr)

    publications = sorted_newest_first(publications)
    talks = sorted_newest_first(talks)

    text = PUBLICATIONS_PAGE.read_text(encoding="utf-8")
    text = inject(text, PUB_MARKER_BEGIN, PUB_MARKER_END, render_list(publications))
    text = inject(text, TALK_MARKER_BEGIN, TALK_MARKER_END, render_list(talks))
    PUBLICATIONS_PAGE.write_text(text, encoding="utf-8")

    print(f"sync_bib: wrote {len(publications)} publications, {len(talks)} talks "
          f"into {PUBLICATIONS_PAGE.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
