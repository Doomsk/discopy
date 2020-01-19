import os
from matplotlib import pyplot as plt
from matplotlib.testing.compare import compare_images
from discopy import *


FOLDER, TOL = 'docs/imgs/', 0


def draw_and_compare(file, folder=FOLDER, tol=TOL,
                     draw=Diagram.draw, **params):
    def result(test):
        draw(test(), path=os.path.join(folder, '.' + file), **params)
        assert compare_images(os.path.join(folder, file),
                              os.path.join(folder, '.' + file), tol) is None
        os.remove(os.path.join(folder, '.' + file))
    return result


@draw_and_compare('crack-eggs.png', figsize=(5, 6), fontsize=18)
def test_draw_eggs():
    def merge(x):
        return Box('merge', x @ x, x)
    egg, white, yolk = Ty('egg'), Ty('white'), Ty('yolk')
    crack = Box('crack', egg, white @ yolk)
    crack_two_eggs = crack @ crack\
        >> Id(white) @ Box('swap', yolk @ white, white @ yolk) @ Id(yolk)\
        >> merge(white) @ merge(yolk)
    return crack_two_eggs


@draw_and_compare('snake-equation.png',
                  aspect='auto', figsize=(5, 2), draw_as_nodes=True,
                  color='#ffffff', draw_types=False)
def test_draw_snake():
    x, eq = Ty('x'), Box('=', Ty(), Ty())
    diagram = Id(x.r).transpose_l() @ eq @ Id(x) @ eq @ Id(x.l).transpose_r()
    diagram = diagram.interchange(1, 4).interchange(3, 1, left=True)
    return diagram


@draw_and_compare('typed-snake-equation.png',
                  figsize=(5, 3), aspect='auto',
                  draw_as_nodes=True, color='#ffffff')
def test_draw_typed_snake():
    x, eq = Ty('x'), Box('=', Ty(), Ty())
    diagram = Id(x.r).transpose_l() @ eq @ Id(x) @ eq @ Id(x.l).transpose_r()
    diagram = diagram.interchange(1, 4).interchange(3, 1, left=True)
    return diagram


@draw_and_compare('who-ansatz.png')
def test_draw_who():
    n, s = Ty('n'), Ty('s')
    copy, update = Box('copy', n, n @ n), Box('update', n @ s, s)
    return Cap(n.r, n)\
        >> Id(n.r) @ copy\
        >> Id(n.r @ n) @ Cap(s, s.l) @ Id(n)\
        >> Id(n.r) @ update @ Id(s.l @ n)


@draw_and_compare('alice-loves-bob.png', draw=pregroup.draw,
                  fontsize=18, fontsize_types=12,
                  figsize=(5, 2), margins=(0, 0))
def test_pregroup_draw():
    s, n = Ty('s'), Ty('n')
    Alice, Bob = Word('Alice', n), Word('Bob', n)
    loves = Word('loves', n.r @ s @ n.l)
    return Alice @ loves @ Bob >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)


def test_autonomisation_to_gif(folder=FOLDER, file='autonomisation.gif'):
    s, n = Ty('s'), Ty('n')
    Alice, Bob = Box("Alice", Ty(), n), Box("Bob", Ty(), n)
    loves = Box('loves', Ty(), n.r @ s @ n.l)
    love_box = Box('loves', n @ n, s)
    love_ansatz = Cap(n.r, n) @ Cap(n, n.l) >> Id(n.r) @ love_box @ Id(n.l)
    ob, ar = {s: s, n: n}, {Alice: Alice, Bob: Bob, loves: love_ansatz}
    A = RigidFunctor(ob, ar)
    sentence = Alice @ loves @ Bob >> Cup(n, n.r) @ Id(s) @ Cup(n.l, n)
    Diagram.to_gif(A(sentence), diagrams=A(sentence).normalize(),
                   path=os.path.join(folder, file), aspect='auto',
                   figsize=(5, 4))


def test_spiral_to_gif(n_cups=2, folder=FOLDER, file='spiral.gif'):
    diagram = moncat.spiral(n_cups)
    diagram.to_gif(os.path.join(folder, file),
                   timestep=500, loop=True, draw_types=False)


def test_Eckmann_Hilton_to_gif(folder=FOLDER, file='EckmannHilton.gif'):
    diagram = Box('s0', Ty(), Ty()) @ Box('s1', Ty(), Ty())
    diagram.to_gif(os.path.join(folder, file),
                   timestep=500, margins=(0.1, 0.1))