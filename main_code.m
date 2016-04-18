% This is the main code for the computer project [CS-763], IIT Bombay.
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
minLen = 0.025*sqrt(size(image,1)*size(image,2));

lines = APPgetLargeConnectedEdges(grayIm, minLen);
%{
% displaying image
figure(1), hold off, imshow(grayIm)
figure(1), hold on, plot(lines(:, [1 2])', lines(:, [3 4])')
%}

% let's try to detect the vanishing points using this information

cross = find_intersection(lines);

%{
%plot intersection points
ind = find((cross(:,2) ~= inf)&(cross(:,5)==1));
hold on
plot(cross(ind,1),cross(ind,2),'o')
%}

% now we vote for each of the interesection points

vote = vote_points(cross,lines);
[val,num] = max(vote);

%{
% displaying most voted vanishing point and their lines
figure(2), hold off, imshow(1/5*grayIm)
figure(2), hold on, plot(lines(cross(num,3:4),[1 2])', lines(cross(num,3:4),[3 4])')
%}
