clc;
close; 
clear all;

addpath(genpath('H:\Tools\matconvnet-1.0-beta25'));
vl_setupnn();
%remember to clearvars, clearvars -global
global net;
net = load('imagenet-vgg-f.mat') ;
net = vl_simplenn_tidy(net) ;