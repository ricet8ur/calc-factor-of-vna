from typing import List, Tuple
import numpy as np
from matplotlib.patches import Circle, Polygon
from matplotlib.axes import Axes

from .circle_math import point_of_intersection_with_unit

# UTILS

def draw_smith_circle(ax: Axes, x: float, y: float, r: float, color=(0, 0, 0)):
    ax.add_artist(
        Circle((x, y),
               r,
               clip_on=True,
               zorder=2,
               linewidth=2,
               edgecolor=color,
               facecolor=(0, 0, 0, .0)))


def draw_grid_circle(ax: Axes,
                     x: float,
                     y: float,
                     r: float,
                     color=(.2, .2, .2, .5),
                     clip=None):
    a = ax.add_artist(
        Circle((x, y),
               r,
               clip_on=True,
               linewidth=1.5,
               edgecolor=color,
               facecolor=(0, 0, 0, 0)))
    if clip:
        a.set_clip_path(clip)


def draw_polygon(axis: Axes, a: List, color=(0, 0, 0), clip=None):
    artist = axis.add_artist(
        Polygon(np.array(a),
                clip_on=True,
                linewidth=1.5,
                edgecolor=color,
                facecolor=(0, 0, 0, 0)))
    if clip:
        artist.set_clip_path(clip)


# !UTILS


# |S|
def plot_abs_s_gridlines(ax: Axes):
    abs_s_ticks = [0.1, 0.3, 0.5, 0.75, 1]
    for r in abs_s_ticks:
        draw_grid_circle(ax, 0, 0, r)
        ax.text(r / (2**0.5) + 0.05,
                r / (2**0.5) + 0.05,
                f'{r:0.2f}'.rstrip('.0'),
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=12)


# Re(Z)
def plot_re_z_gridlines(ax: Axes):
    z_ticks = [0, 0.2, 0.5, 1, 2, 5]
    for r in z_ticks:
        draw_grid_circle(ax, r / (1 + r), 0, 1 / (1 + r))
        if r != 0:
            ax.text(r / (1 + r) * 2 - 1.055,
                    0.045,
                    f'{r}',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=12)


# Im(Z)
def plot_im_z_gridlines(ax: Axes):
    patch = Circle(
        (0, 0),
        radius=1,
        transform=ax.transData,
    )

    z_ticks = [0.2, 0.5, 1, 2, 5]
    for r in z_ticks:
        for direction in (-1, 1):
            x, y, r = 1, direction * 1 / r, 1 / r
            draw_grid_circle(ax, x, y, r, clip=patch)
            tx, ty = point_of_intersection_with_unit(x, y, r)
            ax.text(
                tx * 1.10,
                ty * 1.07,
                f'{direction/r}'.rstrip('.0') + 'j',
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=12,
            )

    # 'x' line
    draw_polygon(ax, [[-1, 0], [1, 0]], clip=patch)
    ax.text(-1.13,
            0.01,
            '0 + 0j',
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=12)
    ax.set_clip_box([[-1, 1], [-1, 1]])
    ax.set_clip_on(True)

    ax.text(1.07,
            0.01,
            r"$\infty$",
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=24)
