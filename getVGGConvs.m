function [conv1, conv2, conv3, conv4, conv5] = getVGGConvs(imgpath)
    im = imread(imgpath) ;
    im_ = single(im) ; % note: 255 range
    
    global net;
    im_ = imresize(im_, net.meta.normalization.imageSize(1:2)) ;
    im_ = im_ - net.meta.normalization.averageImage ;
    res = vl_simplenn(net, im_) ;

    conv1 = reshape(res(2).x, [], 1).';
    conv2 = reshape(res(6).x, [], 1).';
    conv3 = reshape(res(10).x, [], 1).';
    conv4 = reshape(res(12).x, [], 1).';
    conv5 = reshape(res(14).x, [], 1).';

end