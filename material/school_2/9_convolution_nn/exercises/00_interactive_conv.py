import matplotlib.pyplot as plt
import os
import torch
from matplotlib.backend_bases import MouseButton
from typing import Callable
from torchvision.transforms.functional import resize
import argparse
curren_dir = os.path.dirname(os.path.abspath(__file__))

def pink(shape: tuple, c: float, a: float, actfun: Callable = None):
    if len(shape) == 2:
        pink = torch.zeros((1, *shape))
    elif len(shape) == 3:
        pink = torch.zeros(shape)
    else:
        return
    if actfun is None:
        actfun = lambda y: y
    if actfun == "scale":
        actfun = lambda y: (y - y.min())/(y.max() - y.min())
    channels, height, width = pink.shape
    f_height = torch.linspace(1/height, 1.0, height)
    f_width = torch.linspace(1/width, 1.0, width)
    freq = torch.stack(torch.meshgrid((f_height, f_width), indexing="ij")).sum(dim=0) / 2
    for i in range(channels):
        phases = 2 * torch.pi * (torch.rand((height, width)) - 0.5)
        combi = a * (phases * (1 + 1j)) / freq.pow(c)
        pink[i] = torch.fft.ifft2(combi).real
    pink = pink.squeeze()
    return actfun(pink)

class ConvDraw:
    def __init__(self, img: torch.Tensor):
        self.img = (img.permute(2, 0, 1).float())[0:1]
        self.s_sqr = 12  # square size
        self.kernel_dim = 5  # kernel size
        self.a_sqr = (self.kernel_dim + 1) + self.kernel_dim * self.s_sqr  # area size
        self.h, self.w = 3*self.a_sqr, 3*self.a_sqr
        self.x = self.gen_image()
        self.kernel_im = 0.5 * torch.ones(self.a_sqr, self.a_sqr)
        self.kernel = torch.zeros(1, 1, self.kernel_dim, self.kernel_dim)
        self.mid = self.kernel_dim//2
        self.kernel[:, :, self.mid, self.mid] = 1.0
        # self.kernel -= (self.kernel.sum() / (self.kernel_dim**2))
        self.kernel_im[self.mid*(self.s_sqr+1):(self.mid+1)*(self.s_sqr+1), self.mid*(self.s_sqr+1):(self.mid+1)*(self.s_sqr+1)] = 1.0
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.borders()
        self.draw()

    def gen_image(self):
        vertc = torch.tensor([[0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0]])
        horiz = torch.tensor([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0]])
        check = torch.tensor([[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0]])
        cross = torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 1.0]])
        x = torch.zeros(1, self.h, self.w)
        x[0, :self.a_sqr, self.a_sqr:2*self.a_sqr] = torch.rand(self.a_sqr, self.a_sqr)
        x[0, :self.a_sqr, 2*self.a_sqr:] = check.repeat(1 + self.a_sqr//3, 1 + self.a_sqr//3)[:self.a_sqr, :self.a_sqr].unsqueeze(0)
        x[0, self.a_sqr:2*self.a_sqr, :self.a_sqr] = pink((self.a_sqr, self.a_sqr), 2.5, 0.5, actfun=torch.cos)
        x[0, 2*self.a_sqr:, :self.a_sqr] = cross.repeat(1 + self.a_sqr//3, 1 + self.a_sqr//3)[:self.a_sqr, :self.a_sqr].unsqueeze(0)
        x[:, self.a_sqr:, self.a_sqr:] = resize(self.img, (2*self.a_sqr, 2*self.a_sqr), antialias=False)

        return x

    def draw(self):
        draw_img = self.x.clone()
        draw_img = torch.nn.functional.conv2d(draw_img, self.kernel, stride=1, padding="same")[0]
        draw_img = (draw_img - draw_img.min()) / (draw_img.max() - draw_img.min())
        draw_img[:self.a_sqr, :self.a_sqr] = self.kernel_im
        self.ax.clear()
        self.ax.imshow(torch.relu(draw_img))
        self.ax.axis('off')
        plt.gcf().canvas.draw_idle()

    def borders(self):
        for i in range(self.kernel_dim + 1):
            self.kernel_im[i*(self.s_sqr + 1), :] = 1.0
            self.kernel_im[:, i*(self.s_sqr + 1)] = 1.0

    def update(self, x, y, v):
        i = y // (self.s_sqr + 1)
        j = x // (self.s_sqr + 1)
        self.kernel[:, :, i, j] = v
        # self.kernel[self.kernel > 0.0] = 1.0
        # self.kernel[self.kernel < 0.0] = -1.0
        # self.kernel -= (self.kernel.sum() / (self.kernel_dim**2))
        # print(self.kernel[0, 0])
        # self.kernel /= self.kernel[0, 0].norm() if self.kernel[0, 0].norm() > 0 else 1.0
        self.kernel_im[i*(self.s_sqr+1):(i+1)*(self.s_sqr+1), j*(self.s_sqr+1):(j+1)*(self.s_sqr+1)] = (v + 1.0) / 2.0
        self.borders()
        self.draw()

    def on_click(self, event):
        x, y = int(event.xdata), int(event.ydata)
        if x < self.a_sqr and y < self.a_sqr:
            if event.dblclick:
                self.update(x, y, 0.0)
            elif event.button is MouseButton.LEFT:
                self.update(x, y, 1.0)
            elif event.button is MouseButton.RIGHT:
                self.update(x, y, -1.0)
        # plt.disconnect(binding_id)

parser = argparse.ArgumentParser()
parser.add_argument('-dir', type=str, nargs='?')
dir = parser.parse_args().dir
if dir is not None and os.path.exists(dir):
    img = torch.tensor(plt.imread(dir))
elif os.path.exists(os.path.join(curren_dir, r"figures/cat.png")):
    img = torch.tensor(plt.imread("cat.png"))
else:
    raise FileNotFoundError("No image found!")
cnvdrw = ConvDraw(img)
on_click = cnvdrw.on_click
plt.connect('button_press_event', on_click)
plt.show()
 