# -*- coding: utf-8 -*-
#図を描く

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

#draw rect
def draw_rect():
    left, bottom, width,height = 0.25, 0.25, 0.5, 0.5
    right = left + width 
    top = bottom + height

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    p = patches.Rectangle((left, bottom), 
                        width, height, 
                        fill=False, 
                        transform=ax.transAxes, 
                        clip_on=False)
    ax.add_patch(p)
    ax.text(left, bottom,'1: left top',
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes)

    ax.text(left, bottom,'2: left bottom',
            horizontalalignment='left',
            verticalalignment='bottom',
            transform=ax.transAxes)

    ax.text(right, top, '3: right bottom',
            horizontalalignment='right',
            verticalalignment='bottom',
            transform=ax.transAxes)
    ax.text(right, top, '4: right top',
            horizontalalignment='right',
            verticalalignment='top',
            transform=ax.transAxes)

    ax.text(right, bottom, '5: center top',
            horizontalalignment='center',
            verticalalignment='top',
            transform=ax.transAxes)

    ax.text(left, 0.5*(bottom+top), '6: right center',
            horizontalalignment='right',
            verticalalignment='center',
            rotation='vertical',
            transform=ax.transAxes)

    ax.text(left, 0.5*(bottom+top), '7: left center',
            horizontalalignment='left',
            verticalalignment='center',
            rotation='vertical',
            transform=ax.transAxes)

    ax.text(0.5*(left+right), 0.5*(bottom+top), '8: middle',
            horizontalalignment='center',
            verticalalignment='center',        
            fontsize=20, color='red',
            transform=ax.transAxes)

    ax.text(right, 0.5*(bottom+top), '9: centered',
            horizontalalignment='center',
            verticalalignment='center',
            rotation='vertical',
            transform=ax.transAxes)
    ax.text(left, top, '10: rotated\nwith newlines',
            horizontalalignment='center',
            verticalalignment='center',
            rotation=45,
            transform=ax.transAxes)

    title = r'$\alpha > \beta$'
    ax.text(0.5*(left+right), top*2, title,
            horizontalalignment='center',
            verticalalignment='center',        
            transform=ax.transAxes)

    ax.set_axis_off()
    plt.show()
    pass

#draw math
def draw_math():
    t = np.arange(0.0, 2.0, 0.01)
    s = np.sin(2*np.pi*t)
    plt.plot(t,s)
    plt.title(r'$\alpha_i > \beta_i$', fontsize=20)
    plt.text(1, -0.6, r'$\sum_{i=0}^\infty x_i$', fontsize=20)
    plt.text(0.6, 0.6, r'$\mathcal{A}\mathrm{sin}(2 \omega t)$', fontsize=20)
    plt.xlabel('time (s)')
    plt.ylabel('volts (mV)')
    plt.show()
    pass
        
if __name__ == "__main__":
    #draw_rect()
    draw_math()