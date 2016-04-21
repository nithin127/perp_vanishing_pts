% This is the code for the computer vision project [CS763, IIT-B,2016]
% Developers: Nithin Vasisth, Pulkit Katdare
% This code mainly follows the paper written by Varsha Hedao: Recovering
% the spacial layout of Cluttered Rooms 
% "http://vision.cs.uiuc.edu/~vhedau2/Research/research_spatialLayout.html"

clear;
close all
%image = imread('image.jpg');
%image = imread('groundtruth/Images/2884291786_69bec3d738_m.jpg');
image = imread('groundtruth/Images/bedroom4.jpg');
grayIm = rgb2gray(image);
size_im = size(grayIm);
minLen = 0.025*sqrt(size(image,1)*size(image,2));

lines = APPgetLargeConnectedEdges(grayIm, minLen);
% Adding a column to indicate the validity of the detected lines
% 1 == valid, 0 == invalid
lines = [lines , ones(size(lines,1),1)];

%{.
% displaying image
figure(1), hold off, imshow(grayIm)
figure(1), hold on, plot(lines(:, [1 2])', lines(:, [3 4])')
%pause
%}

% Detecting the vanishing points
intn_pts = find_intersection(lines);

%{
%plot intersection points
ind = find((intn_pts(:,2) ~= inf)&(intn_pts(:,5)==1));
figure, imshow(grayIm), hold on
plot(intn_pts(ind,1),intn_pts(ind,2),'o')
%}

% Voting for each of the interesection points
[vote,vote_matrix] = vote_points(intn_pts,lines);
[~,num_1] = sort(vote);

% remove points whose vote is zero
intn_pts(vote==0,5)=0;

 %{
    % displaying most voted points and their lines
    for i = 1:30
    figure(2), hold off, imshow(1/5*grayIm)
    figure(2), hold on, plot(lines(intn_pts(num_1(end-i),3:4),[1 2])',...
        lines(intn_pts(num_1(end-i),3:4),[3 4])')
    pause
    end
 %}
clc;

%% Staring the iterative loop to create bins
% Here we iteratively remove the most voted points, and the lines voting
% for it, so that in the end we have a set of most voted points and their
% membership points

vp_candidates = zeros(size(intn_pts,1),1);
count_vp = 0;

while((sum(intn_pts(:,5)==1)>10)&&(numel((unique(vote)))~=1))
    
    [~,num] = sort(vote);

    % Since we want to ignore the vanishing point, we'll change it's validity
    % index from 1 to 0; Also we'll invalidate the lines voting for it
    count_vp = count_vp +1;
    vp_candidates(count_vp) = num(end);
    intn_pts(num(end),5) = 0;
    vp_lines = vote_matrix{num(end)}{2};
    lines(vp_lines,7) = 0;    
    
    % Let's also remove the validity of all the points who have been formed by
    % the intersection of the vp_1_lines
    intn_pts((ismember(intn_pts(:,3),vp_lines)|...
        ismember(intn_pts(:,4),vp_lines)),5) = 0;
    
    %recomputing the votes of each point
    [vote,vote_matrix] = vote_points(intn_pts,lines);
    
    %{
    % display the lines voting for the selected point in each iteration
    vp_1 = num(end);
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(vp_lines,[1 2])',...
        lines(vp_lines,[3 4])','r')
    pause
    %}    
end

vp_candidates = vp_candidates(1:count_vp);

%[suitable_set,o,f] = find_vpoints(lines,vp_candidates,intn_pts,vote_matrix,size_im,grayIm);

%{

value_set = vote(suitable_set(:,1))+vote(suitable_set(:,2));
[~,ind_s] = sort(value_set);
for i = 0:30
    vp_2 = suitable_set(ind_s(end-i),1);
    vp_3 = suitable_set(ind_s(end-i),2);

    x = [intn_pts([vp_1,vp_2,vp_3],1),intn_pts([vp_1,vp_2,vp_3],2)];
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(intn_pts(vp_1,3:4),[1 2])',...
        lines(intn_pts(vp_1,3:4),[3 4])','r')
    figure(3), hold on, plot(lines(intn_pts(vp_2,3:4),[1 2])',...
        lines(intn_pts(vp_2,3:4),[3 4])','b')
    figure(3), hold on, plot(lines(intn_pts(vp_3,3:4),[1 2])',...
        lines(intn_pts(vp_3,3:4),[3 4])','g')
    hold on, plot(intn_pts(vp_1,1),intn_pts(vp_1,2),'ro')
    hold on, plot(intn_pts(vp_2,1),intn_pts(vp_2,2),'bo')
    hold on, plot(intn_pts(vp_3,1),intn_pts(vp_3,2),'go')
    axis([min(0,min(x(:,1))) max(size_im(1),max(x(:,1))) ...
        min(0,min(x(:,2))) max(size_im(2),max(x(:,2)))])
    pause
end
%}

%{
% This would select only the top 3 points as the vanishing points
vp_1 = vp_candidates(1);
vp_2 = vp_candidates(2);
vp_3 = vp_candidates(3);

x = [intn_pts([vp_1,vp_2,vp_3],1),intn_pts([vp_1,vp_2,vp_3],2)];
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(intn_pts(vp_1,3:4),[1 2])',...
        lines(intn_pts(vp_1,3:4),[3 4])','r')
    figure(3), hold on, plot(lines(intn_pts(vp_2,3:4),[1 2])',...
        lines(intn_pts(vp_2,3:4),[3 4])','b')
    figure(3), hold on, plot(lines(intn_pts(vp_3,3:4),[1 2])',...
        lines(intn_pts(vp_3,3:4),[3 4])','g')
    hold on, plot(intn_pts(vp_1,1),intn_pts(vp_1,2),'ro')
    hold on, plot(intn_pts(vp_2,1),intn_pts(vp_2,2),'bo')
    hold on, plot(intn_pts(vp_3,1),intn_pts(vp_3,2),'go')
    %axis([min(0,min(x(:,1))) max(size_im(1),max(x(:,1))) ...
    %    min(0,min(x(:,2))) max(size_im(2),max(x(:,2)))])
%}
