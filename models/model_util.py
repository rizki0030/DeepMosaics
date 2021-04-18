import torch
import torch.nn as nn
from torch.nn import init
import functools


def save(net,path,gpu_id):
    if isinstance(net, nn.DataParallel):
        torch.save(net.module.cpu().state_dict(),path)
    else:
        torch.save(net.cpu().state_dict(),path) 
    if gpu_id != '-1':
        net.cuda()

def get_norm_layer(norm_type='instance',mod = '2d'):
    if norm_type == 'batch':
        if mod == '2d':
            norm_layer = functools.partial(nn.BatchNorm2d, affine=True)
        elif mod == '3d':
            norm_layer = functools.partial(nn.BatchNorm3d, affine=True)
    elif norm_type == 'instance':
        if mod == '2d':
            norm_layer = functools.partial(nn.InstanceNorm2d, affine=False, track_running_stats=True)
        elif mod =='3d':
            norm_layer = functools.partial(nn.InstanceNorm3d, affine=False, track_running_stats=True)
    elif norm_type == 'none':
        norm_layer = None
    else:
        raise NotImplementedError('normalization layer [%s] is not found' % norm_type)

    return norm_layer

def init_weights(net, init_type='normal', gain=0.02):
    def init_func(m):
        classname = m.__class__.__name__
        if hasattr(m, 'weight') and (classname.find('Conv') != -1 or classname.find('Linear') != -1):
            if init_type == 'normal':
                init.normal_(m.weight.data, 0.0, gain)
            elif init_type == 'xavier':
                init.xavier_normal_(m.weight.data, gain=gain)
            elif init_type == 'kaiming':
                init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
            elif init_type == 'orthogonal':
                init.orthogonal_(m.weight.data, gain=gain)
            else:
                raise NotImplementedError('initialization method [%s] is not implemented' % init_type)
            if hasattr(m, 'bias') and m.bias is not None:
                init.constant_(m.bias.data, 0.0)
        elif classname.find('BatchNorm2d') != -1:
            init.normal_(m.weight.data, 1.0, gain)
            init.constant_(m.bias.data, 0.0)

    print('initialize network with %s' % init_type)
    net.apply(init_func)