"""
节目：《 过 年 》
作者：B站 小倪同学

建议先看原视频：BV1xL4y1E7nT

开工于 2023/1/10
完工于 2023/1/15
"""

import time as btin_time
from collections.abc import Iterable
from itertools import repeat
from sys import exit
from typing import Callable, Literal, Optional, Tuple, Union

import pygame as pg

pg.init()

FPS = 0  # > 0 为帧数限制，为 0 时不限制帧数（能跑到几帧算几帧，往往都是好几百）
SIZE = (1280, 720)
TITLE = '《 过 年 》 | 作者：B站 小倪同学 | %d fps'

screen = pg.display.set_mode(SIZE, pg.RESIZABLE, vsync=True)  # , pg.NOFRAME)
screen_sur = pg.Surface(SIZE)
full_screen = False
max_size = pg.display.list_modes()[0]
temp_size = fact_size = SIZE

# 标题
pg.display.set_caption(TITLE % 0)

# 音乐
pg.mixer.music.load('./assets/audio.mp3')
# 图片
images = {
    'fireworks_fire': pg.transform.scale(pg.image.load('./assets/fireworks_fire.png'), (152, 76)),
    'fireworks_works': pg.transform.scale(pg.image.load('assets/fireworks_works.png'), (196, 482)),
    'lantern': pg.transform.scale(pg.image.load('./assets/lantern.png'), (510, 837)),
}
# 时钟
framerate = pg.time.Clock()


class Animation:
    """一个动画"""

    def __init__(self, func: Callable[..., Optional[pg.Surface]],
                 func_type: Literal[0, 1],
                 args: tuple = (), *,
                 # 变化值：
                 time: Optional[float], pos: Tuple[int, int], move: Tuple[int, int] = None, rotate: int = None,
                 scale: float = None, alpha: Tuple[float, float] = None, crop: Tuple[int, int] = None,
                 # 时间函数：
                 move_func: Optional[Tuple[Callable[[float], float], Callable[[float], float]]] = None,
                 rotate_func: Optional[Callable[[float], float]] = None,
                 scale_func: Optional[Callable[[float], float]] = None,
                 crop_func: Optional[Callable[[float], float]] = None,
                 name: Optional[str] = None):
        """
        :param func:        回调函数，用于绘制图形
        :param func_type:   函数类型。需要传 sur 的是 0，不需要是 1
        :param args:        绘制图形的参数
        :param name:        这个动画的名字

        :param time:        滞留时间
        :param pos:         初始位置
        :param move:        平移，元组
        :param rotate:      旋转
        :param scale:       伸缩，倍数
        :param alpha:       透明度
        :param crop:        裁剪，元组，（方位: int (上0下1), 数值: [0, 1]）
        :param move_func:   时间函数（平移）
        :param rotate_func: 时间函数（旋转）
        :param scale_func:  时间函数（缩放）
        :param crop_func:   时间函数（裁剪）
        """
        self.name = name
        # 创建Surface对象
        self.sur = pg.Surface((1280, 850))
        self.sur.fill('gray')
        self.sur.set_colorkey('gray')
        if func_type == 0:
            func(self.sur, *args)
        elif func_type == 1:
            self.sur.blit(func(*args), (0, 0))
        # print('%s %s' % (self, self.sur.get_bounding_rect()))
        self.sur = self.sur.subsurface(self.sur.get_bounding_rect())
        #
        self.used = False
        self.t0 = None
        self.active = True
        #
        self.action = {
            'time': time,
            'pos': pos,
            'move': move,
            'rotate': rotate,
            'scale': scale,
            'alpha': alpha,
            'crop': crop
        }
        self.action_func = {
            'move': move_func,
            'rotate': rotate_func,
            'scale': scale_func,
            'crop': crop_func
        }
        self.name = name

    def show(self):
        """显示这个动画的这一帧"""
        if not self.used:
            self.used = True
            self.t0 = btin_time.time()
            self.create()
        t_rate = (btin_time.time() - self.t0) / self.action['time']
        # 显示
        if t_rate < 1:
            o = self.sur
            # 处理缩放
            if self.action['scale'] is not None:
                if self.action_func['scale'] is None:
                    size = array_op(lambda x, y: x * y, o.get_size(), t_rate * self.action['scale'] + 1 - t_rate)
                else:
                    f = self.action_func['scale']
                    size = array_op(lambda x, y: x * y, o.get_size(), f(t_rate) * self.action['scale'] + 1 - f(t_rate))
                o = pg.transform.scale(o, size)
            # 处理旋转
            if self.action['rotate'] is not None:
                if self.action_func['rotate'] is None:
                    angle = t_rate * self.action['rotate']
                else:
                    f = self.action_func['rotate']
                    angle = f(t_rate) * self.action['rotate']
                o = pg.transform.rotate(o, angle)
            # 处理位置
            r = o.get_rect()
            if self.action['move'] is not None:
                if self.action_func['move'] is None:
                    pos = array_op(lambda x, y, z: x + y * z,
                                   self.action['pos'], self.action['move'], t_rate)
                else:
                    f_x, f_y = self.action_func['move']
                    pos = array_op(lambda x, y, z: x + y * z,
                                   self.action['pos'], self.action['move'], (f_x(t_rate), f_y(t_rate)))
            else:
                pos = self.action['pos']
            r.center = pos
            # 处理剪切
            if self.action['crop'] is not None:
                dire, rate = self.action['crop']
                w, h = o.get_size()
                if dire == 0:
                    o = pg.transform.chop(o, (0, 0, 0, h * t_rate))
                elif dire == 1:
                    o = pg.transform.chop(o, (0, h * (1 - t_rate), 0, h))
            # 处理透明度
            # if self.action['alpha'] is not None:
            #     o.set_alpha(self.action['alpha'])

            # 拼上去
            screen_sur.blit(o, r)
        # 到时了，删
        else:
            self.active = False

    def create(self):
        """
        创建对象时的输出
        可输出绿色，只有在 pycharm 里能用
        """
        print('>>> \033[1;32mCreate\033[0m %s' % self)

    def delete(self):
        """
        创建对象时的输出
        可输出红色，只有在 pycharm 里能用
        """
        print('>>> \033[1;31mDelete\033[0m %s' % self)

    def __str__(self):
        return self.name or '<%s object Unnamed at 0x%X>' % (self.__class__.__name__, id(self))

    __repr__ = __str__


class Stage:
    """舞台，容纳动画"""

    # 单例
    __instance = None

    def __new__(cls):
        # 单例
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.on_stage = []

    def add(self, o: 'Animation'):
        self.on_stage.append(o)

    def show(self):
        screen_sur.fill('white')  # TODO 去掉这个 -> 地狱绘图
        for each in self.on_stage:
            if each.active:
                each.show()
            else:
                each.delete()
                self.on_stage.remove(each)
        size = pg.display.get_window_size()
        size = (size[0], size[0] * 9 / 16) if size[0] * 9 / 16 < size[1] else (size[1] * 16 / 9, size[1])
        screen.blit(pg.transform.scale(screen_sur, size), (0, 0))


stage = Stage()


def q():
    """退出程序"""
    print('程序退出')
    pg.quit()
    exit()


def get_ev():
    """
    处理事件
    ESC退出，F11全屏，窗口大小调整
    """
    global screen, full_screen, max_size, fact_size, temp_size
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            q()
        elif ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE:
                q()
            # TODO 删
            elif ev.key == pg.K_SPACE:
                print('停止...')
                pg.mixer.music.fadeout(500)
                # 永久暂停
                while True:
                    pg.display.flip()
                    for e in pg.event.get():
                        if e.type == pg.QUIT:
                            q()
                        elif e.type == pg.KEYDOWN:
                            if e.key == pg.K_ESCAPE:
                                q()
            #
            elif ev.key == pg.K_F11:
                full_screen = not full_screen
                if full_screen:
                    temp_size = fact_size
                    fact_size = max_size
                    screen = pg.display.set_mode(fact_size, pg.FULLSCREEN | pg.HWSURFACE, vsync=True)
                else:
                    fact_size = temp_size
                    screen = pg.display.set_mode(fact_size, pg.RESIZABLE, vsync=True)
        elif ev.type == pg.VIDEORESIZE and not full_screen:
            fact_size = ev.size
            screen = pg.display.set_mode(fact_size, pg.RESIZABLE, vsync=True)


def array_op(op: Callable, *a) -> tuple:
    """两个数组运算"""
    a = list(a)
    for ind, it in enumerate(a):
        if not isinstance(it, Iterable):
            a[ind] = repeat(it)
    return tuple(map(op, *a))


def text_func(name: str, size: int, text: str, antialias: bool = False, color: Union[tuple, str] = 'black'):
    return pg.font.SysFont(name, size).render(text, antialias, color)


# 渲染一个 `福` 字，会反复用
fu = pg.Surface(SIZE)
fu.fill('gray')
fu.set_colorkey('gray')
pg.draw.polygon(fu, 'red', ((180, 0), (0, 180), (180, 360), (360, 180)))
pg.draw.polygon(fu, 'white', ((180, 0), (0, 180), (180, 360), (360, 180)), 2)
fu.blit(text_func('simhei', 150, '福', True, 'black'), (104, 104))
fu = pg.transform.chop(fu, (360, 360, 920, 360))


def fu_func(scale: Union[int, float] = 1, rotate: Union[int, float] = 0) -> pg.Surface:
    """
    生成 `福` 字的函数。
    正方形的对角线长为 360px
    """
    # 处理伸缩
    o = fu if scale == 1 else pg.transform.scale(fu, (360 * scale,) * 2)
    # 处理旋转
    o = o if rotate == 0 else pg.transform.rotate(o, rotate)
    return o


def fireworks_func(type_: Literal[0, 1]) -> pg.Surface:
    """生成鞭炮的函数"""
    if type_ == 0:
        return images['fireworks_fire']
    elif type_ == 1:
        return images['fireworks_works']


def lantern_func() -> pg.Surface:
    return images['lantern']


# 超大的动画集
data = (
    # ----------------------------------------第 1 篇 √ ----------------------------------------
    # ------------------------------开头的福字------------------------------
    # 三个福字(470px, 313px)
    [0.4, Animation(fu_func, 1, (0.87,), name='福-1', time=2, pos=(640, 360)), True],
    [1.3, Animation(fu_func, 1, (0.87,), name='福-2', time=1.1, pos=(640 + 344, 360)), True],
    [2, Animation(fu_func, 1, (0.87,), name='福-3', time=0.4, pos=(640 - 344, 360)), True],
    # 一个
    [2.4, Animation(fu_func, 1, (0.87,), name='福-4', time=0.5, pos=(640 + 37, 360 + 37)), True],
    # 大
    [2.9, Animation(fu_func, 1, (1.9,), name='福-5', time=0.4, pos=(640, 360)), True],
    # *2
    [3.3, Animation(fu_func, 1, (1.9,), name='福-6', time=0.5, pos=(362, 360)), True],
    [3.3, Animation(fu_func, 1, (1.9,), name='福-7', time=0.5, pos=(986, 360)), True],
    # *1
    [3.8, Animation(fu_func, 1, (1.9,), name='福-8', time=0.4, pos=(635, 343)), True],
    # 倒
    [4.2, Animation(fu_func, 1, (1.9, 180), name='福-9', time=0.2, pos=(635, 368)), True],
    # 转
    [4.4, Animation(fu_func, 1, (1.9, 180), name='福-10', time=2.2, pos=(640, 360), rotate=-8 * 360), True],
    # *2
    [6.6, Animation(fu_func, 1, (1.9, 180), name='福-11', time=2.6, pos=(365, 360), rotate=-11 * 360), True],
    [6.6, Animation(fu_func, 1, (1.9, 180), name='福-12', time=2.6, pos=(985, 360), rotate=-11 * 360), True],  # ind=11
    # ------------------------------烟花------------------------------
    # 1
    [9, Animation(fireworks_func, 1, (1,), name='烟花-1-1', time=1.1, pos=(383, 434), crop=(1, 1)), True],
    [9, Animation(fireworks_func, 1, (0,), name='烟花-1-2', time=1.1, pos=(383 - 22, 434 + 119)), True],
    # 2
    [9.7, Animation(fireworks_func, 1, (1,), name='烟花-2-1', time=1.1, pos=(927, 330), crop=(1, 1)), True],
    [9.7, Animation(fireworks_func, 1, (0,), name='烟花-2-2', time=1.1, pos=(927 - 22, 330 + 119)), True],
    # 3
    [10.5, Animation(fireworks_func, 1, (1,), name='烟花-3-1', time=1.1, pos=(670, 400), crop=(1, 1)), True],
    [10.5, Animation(fireworks_func, 1, (0,), name='烟花-3-2', time=1.1, pos=(670 - 22, 400 + 119)), True],
    # ----------------------------------------第 2 篇----------------------------------------
    # ------------------------------灯笼------------------------------
    # 1
    [10.9, Animation(lantern_func, 1, name='灯笼-1-1', time=2, pos=(200, 337), move=(857, 0)), True],
    [12.9, Animation(lantern_func, 1, name='灯笼-1-2', time=1, pos=(857, 337), move=(-957, -152), rotate=11 * 360), True],
    # 2
    [14.4, Animation(lantern_func, 1, name='灯笼-2-1', time=1.9, pos=(1520, 338), move=(434 - 1520, 0)), True],
    [16.3, Animation(lantern_func, 1, name='灯笼-2-2', time=1.2, pos=(434, 338), move=(1520 - 400, 265 - 338),
                     rotate=-9 * 360), True],
    # 3
    [17.5, Animation(lantern_func, 1, name='灯笼-3-1', time=0.8, pos=(1520, 340), move=(632 - 1520, -20)), True],
    [18.4, Animation(lantern_func, 1, name='灯笼-3-2', time=0.4, pos=(623, 320), scale=2), True],
    [18.8, Animation(lantern_func, 1, name='灯笼-3-2', time=0.6, pos=(623, 320), scale=2), True],  # 944px
    # 4
    [19.5, Animation(lantern_func, 1, name='灯笼-4-1', time=0.6, pos=(640, 400), move=(-100, 0)), True],
    [20.1, Animation(lantern_func, 1, name='灯笼-4-2', time=1.1, pos=(540, 400), scale=2), True],
    # 5
    [21.4, Animation(lantern_func, 1, name='灯笼-5-1', time=1.4, pos=(-100, 0), move=(1580, 1020)), True],
    # ----------------------------------------第 3 篇 √ ----------------------------------------
    # ------------------------------烟花------------------------------
    # 1
    [23, Animation(fireworks_func, 1, (1,), name='烟花-1-1', time=1.1, pos=(130, 450), crop=(1, 1)), True],
    [23, Animation(fireworks_func, 1, (0,), name='烟花-1-2', time=1.1, pos=(383 - 22, 434 + 119)), True],
    # 2
    [23.2, Animation(fireworks_func, 1, (1,), name='烟花-2-1', time=1.1, pos=(372, 440), crop=(1, 1)), True],
    [23.2, Animation(fireworks_func, 1, (0,), name='烟花-2-2', time=1.1, pos=(372 - 22, 440 + 119)), True],
    # 3
    [23.4, Animation(fireworks_func, 1, (1,), name='烟花-3-1', time=1.1, pos=(535, 485), crop=(1, 1)), True],
    [23.4, Animation(fireworks_func, 1, (0,), name='烟花-3-2', time=1.1, pos=(535 - 22, 485 + 119)), True],
    # 4
    [23.7, Animation(fireworks_func, 1, (1,), name='烟花-4-1', time=1.1, pos=(383, 210), crop=(1, 1)), True],
    [23.7, Animation(fireworks_func, 1, (0,), name='烟花-4-2', time=1.1, pos=(383 - 22, 210 + 119)), True],
    # 5
    [23.8, Animation(fireworks_func, 1, (1,), name='烟花-5-1', time=1.1, pos=(773, 446), crop=(1, 1)), True],
    [23.8, Animation(fireworks_func, 1, (0,), name='烟花-5-2', time=1.1, pos=(773 - 22, 446 + 119)), True],
    # 6
    [23.9, Animation(fireworks_func, 1, (1,), name='烟花-6-1', time=1.1, pos=(453, 378), crop=(1, 1)), True],
    [23.9, Animation(fireworks_func, 1, (0,), name='烟花-6-2', time=1.1, pos=(453 - 22, 378 + 119)), True],
    # 7
    [24.1, Animation(fireworks_func, 1, (1,), name='烟花-7-1', time=1.1, pos=(615, 417), crop=(1, 1)), True],
    [24.1, Animation(fireworks_func, 1, (0,), name='烟花-7-2', time=1.1, pos=(615 - 22, 417 + 119)), True],
    # 8
    [24.5, Animation(fireworks_func, 1, (1,), name='烟花-8-1', time=1.1, pos=(852, 380), crop=(1, 1)), True],
    [24.5, Animation(fireworks_func, 1, (0,), name='烟花-8-2', time=1.1, pos=(852 - 22, 380 + 119)), True],
    # 9
    [24.6, Animation(fireworks_func, 1, (1,), name='烟花-9-1', time=1.1, pos=(565, 246), crop=(1, 1)), True],
    [24.6, Animation(fireworks_func, 1, (0,), name='烟花-9-2', time=1.1, pos=(565 - 22, 246 + 119)), True],
    # 10
    [24.9, Animation(fireworks_func, 1, (1,), name='烟花-10-1', time=1.1, pos=(808, 246), crop=(1, 1)), True],
    [24.9, Animation(fireworks_func, 1, (0,), name='烟花-10-2', time=1.1, pos=(808 - 22, 246 + 119)), True],
    # 11
    [25.0, Animation(fireworks_func, 1, (1,), name='烟花-11-1', time=1.1, pos=(969, 288), crop=(1, 1)), True],
    [25.0, Animation(fireworks_func, 1, (0,), name='烟花-11-2', time=1.1, pos=(969 - 22, 288 + 119)), True],
    # 12
    [25.2, Animation(fireworks_func, 1, (1,), name='烟花-12-1', time=1.1, pos=(583, 644), crop=(1, 1)), True],
    [25.2, Animation(fireworks_func, 1, (0,), name='烟花-12-2', time=1.1, pos=(583 - 22, 644 + 119)), True],
    # 13
    [25.4, Animation(fireworks_func, 1, (1,), name='烟花-13-1', time=1.1, pos=(1207, 250), crop=(1, 1)), True],
    [25.4, Animation(fireworks_func, 1, (0,), name='烟花-13-2', time=1.1, pos=(1207 - 22, 250 + 119)), True],
    # 14
    [25.5, Animation(fireworks_func, 1, (1,), name='烟花-14-1', time=1.1, pos=(825, 630), crop=(1, 1)), True],
    [25.5, Animation(fireworks_func, 1, (0,), name='烟花-14-2', time=1.1, pos=(825 - 22, 630 + 119)), True],
    # 15
    [25.6, Animation(fireworks_func, 1, (1,), name='烟花-15-1', time=1.1, pos=(989, 672), crop=(1, 1)), True],
    [25.6, Animation(fireworks_func, 1, (0,), name='烟花-15-2', time=1.1, pos=(989 - 22, 672 + 119)), True],
    # 16
    [26, Animation(fireworks_func, 1, (1,), name='烟花-16-1', time=1.1, pos=(1226, 636), crop=(1, 1)), True],
    [26, Animation(fireworks_func, 1, (0,), name='烟花-16-2', time=1.1, pos=(1226 - 22, 636 + 119)), True],
    # 17
    [26.2, Animation(fireworks_func, 1, (1,), name='烟花-17-1', time=1.1, pos=(163, 376), crop=(1, 1)), True],
    [26.2, Animation(fireworks_func, 1, (0,), name='烟花-17-2', time=1.1, pos=(163 - 22, 376 + 119)), True],
    # 18
    [26.4, Animation(fireworks_func, 1, (1,), name='烟花-18-1', time=1.1, pos=(405, 365), crop=(1, 1)), True],
    [26.4, Animation(fireworks_func, 1, (0,), name='烟花-18-2', time=1.1, pos=(405 - 22, 365 + 119)), True],
    # 19
    [26.6, Animation(fireworks_func, 1, (1,), name='烟花-19-1', time=1.1, pos=(566, 409), crop=(1, 1)), True],
    [26.6, Animation(fireworks_func, 1, (0,), name='烟花-19-2', time=1.1, pos=(566 - 22, 409 + 119)), True],
    # 20
    [27, Animation(fireworks_func, 1, (1,), name='烟花-20-1', time=1.1, pos=(804, 376), crop=(1, 1)), True],
    [27, Animation(fireworks_func, 1, (0,), name='烟花-20-2', time=1.1, pos=(804 - 22, 376 + 119)), True],
    # 21
    [27.2, Animation(fireworks_func, 1, (1,), name='烟花-21-1', time=1.1, pos=(677, 573), crop=(1, 1)), True],
    [27.2, Animation(fireworks_func, 1, (0,), name='烟花-21-2', time=1.1, pos=(677 - 22, 573 + 119)), True],
    # 22
    [27.4, Animation(fireworks_func, 1, (1,), name='烟花-22-1', time=1.1, pos=(919, 562), crop=(1, 1)), True],
    [27.4, Animation(fireworks_func, 1, (0,), name='烟花-22-2', time=1.1, pos=(919 - 22, 562 + 119)), True],
    # 23
    [27.6, Animation(fireworks_func, 1, (1,), name='烟花-23-1', time=1.1, pos=(1082, 608), crop=(1, 1)), True],
    [27.6, Animation(fireworks_func, 1, (0,), name='烟花-23-2', time=1.1, pos=(1082 - 22, 608 + 119)), True],
    # 24
    [28, Animation(fireworks_func, 1, (1,), name='烟花-24-1', time=1.1, pos=(1310, 566), crop=(1, 1)), True],
    [28, Animation(fireworks_func, 1, (0,), name='烟花-24-2', time=1.1, pos=(1310 - 22, 566 + 119)), True],
    # ----------------------------------------第 4 篇----------------------------------------
    # ------------------------------4 个福字乱舞------------------------------
    # 原 360px
    # 小(290px)
    # [29.4, Animation(fu_func, 1, (0.54,), time=14.2, pos=(-90, 150), move=(1460, 0)), True],
    # 中间 从右往左(470px)
    # [29.4, Animation(fu_func, 1, (0.78,), time=14.2, pos=(1600, 350), move=(-1780, 0), rotate=-10 * 360), True],
    # 中间 转圈
    [29.4, Animation(fu_func, 1, (0.78,), time=14.3, pos=(363, 320), move=(360, -260), rotate=-113 * 360), True],  # 先上去
    # 下
    # [29.4, Animation(fu_func, 1, (0.78,), time=4.8, pos=(1400, 620), move=(-1450, 0), rotate=-30 * 360), True],
    # 字
    [34.2, Animation(text_func, 1, ('simhei', 50, '过年啦', False, 'red'), time=14.8, pos=(1350, 100), move=(-1450, 0)),
     True],
    [34.2, Animation(text_func, 1, ('simhei', 50, '过年啦', False, 'red'), time=14.8, pos=(1350, 50), move=(-1450, 0)),
     True],
    # 下 停滞
    [34.2, Animation(fu_func, 1, (0.78,), time=9.4, pos=(-50, 620)), True],
    # ----------------------------------------第 5 篇----------------------------------------
    # ------------------------------8 个大字------------------------------
    [45.8, Animation(text_func, 1, ('kaiti', 150, '欢', False, 'yellow'), time=0.8, pos=(383, 243)), True],
    [46.6, Animation(text_func, 1, ('kaiti', 150, '欢', False, 'yellow'), time=0.8, pos=(383, 243)), True],
)
n_data = len(data)
print('动画集数量：%d' % n_data)


# FPS = 30
def main(start: float = 0):
    """
    主函数
    :param start: 动画从第几秒开始，默认从头开始
    """
    index = 0  # 播放到哪一个了
    while data[index][0] < start:
        index += 1
    print('从第 %.1f 秒开始播放，从 index=%d 动画开始播放' % (start, index))
    # 播放音乐
    pg.mixer.music.play(start=start)
    pg.mixer.music.set_volume(0.3)  # TODO 删
    t0 = btin_time.time() - start
    second = 0
    print('=' * 60)
    while True:
        index = min(index, n_data - 1)
        if data[index][2] and btin_time.time() - t0 > data[index][0]:
            # 添加到舞台
            stage.add(data[index][1])
            data[index][2] = False
            index += 1
        # 事件
        get_ev()
        # 填充 白色
        screen.fill('black')
        # 刷新舞台
        stage.show()
        # 刷新窗口
        pg.display.flip()
        framerate.tick(FPS)
        if pg.time.get_ticks() / 1000 > second:
            second += 0.75
            pg.display.set_caption(TITLE % min(framerate.get_fps(), 1e4))  # 帧数不能是 inf, 最大 10000


if __name__ == '__main__':
    main()
