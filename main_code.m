% This is the main code for the computer vision project [CS763, IIT-B,2016]
% Developers: Nithin Vasisth, Pulkit Katdare
% This code mainly follows the paper written by Varsha Hedao: Recovering
% the spacial layout of Cluttered Rooms 
%"http://vision.cs.uiuc.edu/~vhedau2/Research/research_spatialLayout.html"

clear;
close all
%image = imread('image.jpg');
image = imread('groundtruth/Images/2884291786_69bec3d738_m.jpg');
%image = imread('groundtruth/Images/0000000041.jpg');
grayIm = rgb2gray(image);
size_im = size(grayIm);
minLen = 0.025*sqrt(size(image,1)*size(image,2));

lines = APPgetLargeConnectedEdges(grayIm, minLen);
%{
% displaying image
figure(1), hold off, imshow(grayIm)
figure(1), hold on, plot(lines(:, [1 2])', lines(:, [3 4])')
%}

% let's try to detect the vanishing points using this information

intn_pts = find_intersection(lines);

%{
%plot intersection points
ind = find((intn_pts(:,2) ~= inf)&(intn_pts(:,5)==1));
hold on
plot(intn_pts(ind,1),intn_pts(ind,2),'o')
%}

% now we vote for each of the interesection points

[vote,vote_matrix] = vote_points(intn_pts,lines);
[val,num] = sort(vote);

%{
% displaying most voted vanishing point and their lines
for i = 1:30
figure(2), hold off, imshow(1/5*grayIm)
figure(2), hold on, plot(lines(intn_pts(num(end-i),3:4),[1 2])',...
    lines(intn_pts(num(end-i),3:4),[3 4])')
pause
end
%}

% since we want to ignore the vaninishing point, we'll change it's validity
% index from 1 to 0;
vp_1 = num(end);
intn_pts(num(end),5) = 0;

%[vp_2,vp_3] = find_vpoints(lines,intn_pts,vp_1,vote_matrix,size_im );