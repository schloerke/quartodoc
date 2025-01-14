import pytest
import griffe.docstrings.dataclasses as ds

from quartodoc.renderers import MdRenderer
from quartodoc import get_object


@pytest.fixture
def renderer():
    return MdRenderer()


def test_render_param_kwargs(renderer):
    f = get_object("quartodoc.tests.example_signature.no_annotations")
    res = renderer.render(f.parameters)

    assert res == "a, b=1, *args, c, d=2, **kwargs"


def test_render_param_kwargs_annotated():
    renderer = MdRenderer(show_signature_annotations=True)
    f = get_object("quartodoc.tests.example_signature.yes_annotations")

    res = renderer.render(f.parameters)

    assert (
        res
        == "a: int, b: int = 1, *args: list\\[str\\], c: int, d: int, **kwargs: dict\\[str, str\\]"
    )


@pytest.mark.parametrize(
    "src, dst",
    [
        ("example_signature.pos_only", "x, /, a, b=2"),
        ("example_signature.kw_only", "x, *, a, b=2"),
        ("example_signature.early_args", "x, *args, a, b=2, **kwargs"),
        ("example_signature.late_args", "x, a, b=2, *args, **kwargs"),
    ],
)
def test_render_param_kwonly(src, dst, renderer):
    f = get_object("quartodoc.tests", src)

    res = renderer.render(f.parameters)
    assert res == dst


@pytest.mark.parametrize(
    "pair",
    [
        [ds.DocstringSectionParameters, ds.DocstringParameter],
        [ds.DocstringSectionAttributes, ds.DocstringAttribute],
        [ds.DocstringSectionReturns, ds.DocstringReturn],
    ],
)
def test_render_table_description_interlink(renderer, pair):
    interlink = "[](`abc`)"
    cls_section, cls_par = pair
    pars = cls_section([cls_par(name="x", description=interlink)])

    res = renderer.render(pars)
    assert interlink in res
