import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation
import time

# set axis off for all plots
rc = {"axes.spines.left" : False,
      "axes.spines.right" : False,
      "axes.spines.bottom" : False,
      "axes.spines.top" : False,
      "xtick.bottom" : False,
      "xtick.labelbottom" : False,
      "ytick.labelleft" : False,
      "ytick.left" : False}
plt.rcParams.update(rc)

fig = plt.figure()
fig.canvas.manager.set_window_title('✧ﾟ❀ wordle ❀ﾟ✧')
fig.set_figheight(8)
fig.set_figwidth(6)
ax = fig.add_subplot(111)

# small delay to allow wordle.py to generate a new empty attempt.png figure
#(so as not to display the results of the previous game)
time.sleep(0.5)

img = mpimg.imread('attempt.png')
implot = ax.imshow(img)

def update(frame):
    # sometimes image plotting occurs while image file is being updated
    # in that case we would get a syntax error message. try/except here because
    # I want to ignore this error message and continue with the next plot anyway
    try:
        new_im = mpimg.imread('attempt.png')
        implot.set_data(new_im)
    except SyntaxError:
        pass

anim = FuncAnimation(fig, update, frames=None, interval=1000, cache_frame_data=False)
plt.show()
