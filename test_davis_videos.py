from __future__ import division
import time
import torch
import numpy as np
from torch.autograd import Variable
import models.networks
from options.train_options import TrainOptions
import sys
from loaders import data_loader
from models import models
import random
import math

BATCH_SIZE = 1

opt = TrainOptions().parse()  # set CUDA_VISIBLE_DEVICES before import torch

video_list = 'test_data/test_davis_video_list.txt'

isTrain = False
eval_num_threads = 2
video_data_loader = data_loader.CreateDAVISDataLoader(video_list, BATCH_SIZE)
video_dataset = video_data_loader.load_data()
video_data_size = len(video_data_loader)
print('========================= Video dataset #images = %d =========' %
      video_data_size)

model = models.create_model(opt, isTrain)

def test_video(model, dataset, dataset_size):

  model.switch_to_eval()
  save_path = 'test_data/viz_predictions/'
  print('save_path %s' % save_path)

  for i, data in enumerate(dataset):
    print(i)
    stacked_img = data[0]
    targets = data[1]

    model.run_and_save_DAVIS(stacked_img, targets, save_path)


torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True
best_epoch = 0
global_step = 0

print(
    '=================================  BEGIN VALIDATION ====================================='
)

print('TESTING ON VIDEO')
test_video(model, video_dataset, video_data_size)
