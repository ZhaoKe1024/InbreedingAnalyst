#!/user/zhao/miniconda3/envs/torch-0
# -*- coding: utf_8 -*-
# @Time : 2024/4/10 20:38
# @Author: ZhaoKe
# @File : comm.py
# @Software: PyCharm
import argparse
import distutils
import functools
from audio import AudioSegment

def print_arguments(args=None, configs=None):
    if args:
        print("----------- 额外配置参数 -----------")
        for arg, value in sorted(vars(args).items()):
            print("%s: %s" % (arg, value))
        print("------------------------------------------------")
    if configs:
        print("----------- 配置文件参数 -----------")
        for arg, value in sorted(configs.items()):
            if isinstance(value, dict):
                print(f"{arg}:")
                for a, v in sorted(value.items()):
                    if isinstance(v, dict):
                        print(f"\t{a}:")
                        for a1, v1 in sorted(v.items()):
                            print("\t\t%s: %s" % (a1, v1))
                    else:
                        print("\t%s: %s" % (a, v))
            else:
                print("%s: %s" % (arg, value))
        print("------------------------------------------------")


def add_arguments(argname, type, default, help, argparser, **kwargs):
    type = distutils.util.strtobool if type == bool else type
    argparser.add_argument("--" + argname,
                           default=default,
                           type=type,
                           help=help + ' 默认: %(default)s.',
                           **kwargs)


parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg(argname='info', type=str, default=None, help='计算音频信息')
args = parser.parse_args()
print_arguments(args=args)


if args.info:
    seg = AudioSegment.from_file(args.info)
    print("{}: duration {}".format(args.info, seg.duration))
