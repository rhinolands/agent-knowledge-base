"""The lint gate, the chunker and the two outputs."""

import json
import sys

import pytest

import index


def write(kb, rel, name="doc", type_="concept", desc="One line.", body="Body."):
    path = kb / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ntype: {type_}\ndescription: {desc}\n---\n{body}\n",
        encoding="utf-8",
    )


def run(monkeypatch, tmp_path, *args):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["index.py", *args])
    return index.main()


def test_shipped_kb_passes_lint():
    records, errors = index.build(index.Path("kb"), 800, 100)
    assert errors == []
    assert {r["type"] for r in records} == {"concept", "reference", "log"}


def test_missing_field_fails(tmp_path):
    (tmp_path / "a.md").write_text("---\nname: a\ntype: concept\n---\nx\n")
    _, errors = index.build(tmp_path, 800, 100)
    assert "missing frontmatter ['description']" in errors[0]


def test_no_frontmatter_fails(tmp_path):
    (tmp_path / "a.md").write_text("just text\n")
    _, errors = index.build(tmp_path, 800, 100)
    assert len(errors) == 1


def test_unknown_type_fails(tmp_path):
    write(tmp_path, "a.md", type_="howto")
    _, errors = index.build(tmp_path, 800, 100)
    assert "unknown type 'howto'" in errors[0]


def test_duplicate_name_fails(tmp_path):
    write(tmp_path, "concepts/a.md", name="same")
    write(tmp_path, "log/b.md", name="same", type_="log")
    _, errors = index.build(tmp_path, 800, 100)
    assert "duplicate name 'same'" in errors[0]


def test_lint_failure_exits_non_zero_and_writes_nothing(monkeypatch, tmp_path):
    write(tmp_path / "kb", "a.md", type_="howto")
    assert run(monkeypatch, tmp_path) == 1
    assert not (tmp_path / "index.json").exists()


def test_missing_kb_dir_exits_2(monkeypatch, tmp_path):
    assert run(monkeypatch, tmp_path, "--kb", "nope") == 2


def test_chunks_overlap_and_cover_the_body():
    words = [f"w{i}" for i in range(500)]
    chunks = index.chunk(" ".join(words), size=200, overlap=50)
    assert len(chunks) > 1
    first, second = chunks[0].split(), chunks[1].split()
    assert set(first) & set(second)  # overlap
    assert chunks[-1].split()[-1] == "w499"  # nothing dropped at the end


def test_outputs_are_written(monkeypatch, tmp_path):
    write(tmp_path / "kb", "concepts/a.md", name="a", body="alpha " * 400)
    write(tmp_path / "kb", "reference/b.md", name="b", type_="reference")
    assert run(monkeypatch, tmp_path, "--chunk-size", "400", "--overlap", "50") == 0
    records = json.loads((tmp_path / "index.json").read_text())
    assert len({r["id"] for r in records}) == len(records)
    cmap = (tmp_path / "capability-map.md").read_text()
    assert "## concept (1)" in cmap and "## reference (1)" in cmap


@pytest.mark.parametrize("size,overlap", [(10, 10), (5, 100)])
def test_overlap_at_or_above_size_still_terminates(size, overlap):
    assert index.chunk("a b c d e f g h", size, overlap)
