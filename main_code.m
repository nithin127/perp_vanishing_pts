% This is the code for the computer vision project [CS763, IIT-B,2016]
% Developers: Nithin Vasisth, Pulkit Katdare
% This code mainly follows the paper written by Varsha Hedao: Recovering
% the spacial layout of Cluttered Rooms 
% "http://vision.cs.uiuc.edu/~vhedau2/Research/research_spatialLayout.html"

clear;
close all
%image = imread('image.jpg');
%image = imread('groundtruth/Images/2884291786_69bec3d738_m.jpg');
%image = imread('groundtruth/Images/bedroom4.jpg');
image = imread('groundtruth/Images/0000000041.jpg');
grayIm = rgb2gray(image);
size_im = size(grayIm);
minLen = 0.025*sqrt(size(image,1)*size(image,2));

lines = APPgetLargeConnectedEdges(grayIm, minLen);
% Adding a column to indicate the validity of the detected lines
% 1 == valid, 0 == invalid
lines = [lines , ones(size(lines,1),1)];

% Detecting the vanishing points
intn_pts = find_intersection(lines);

% Voting for each of the interesection points
threshold = 1;
[vote_init,vote_matrix_init] = vote_points(intn_pts,lines,threshold);
[~,num_1] = sort(vote_init);

% remove points whose vote is zero
%intn_pts(vote==0,5)=0;

clc;

%% Staring the iterative loop to create bins

% Here we iteratively remove the most voted points, and the lines voting
% for it, so that in the end we have a set of most voted points and their
% membership points

vp_candidates = zeros(size(intn_pts,1),1); % pre-allocating for speed
count_vp = 0;
vote = vote_init;
vote_matrix = vote_matrix_init;
vp_membership = cell(1);

while((sum(intn_pts(:,5)==1)>10)&&(numel((unique(vote)))~=1))
    
    [~,num] = sort(vote);

    % Since we want to ignore the vanishing point, we'll change it's validity
    % index from 1 to 0; Also we'll invalidate the lines voting for it
    
    count_vp = count_vp +1;
    vp_candidates(count_vp) = num(end);
    intn_pts(num(end),5) = 0;
    vp_lines = determine_membership(num(end),lines,vote_matrix);
    lines(vp_lines,7) = 0;    
    vp_membership{count_vp} = vp_lines;
    
    % Let's also remove the validity of all the points who have been formed by
    % the intersection of the vp_1_lines
    intn_pts((ismember(intn_pts(:,3),vp_lines)|...
        ismember(intn_pts(:,4),vp_lines)),5) = 0;
    
    %recomputing the votes of each point
    % We change the threshold at each iteration
    % threshold = 1/(count_vp^2); % We're not using thresholds here
    [vote,vote_matrix] = vote_points(intn_pts,lines,threshold);
    
    %{
    % display the lines voting for the selected point in each iteration
    vp_1 = num(end);
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(vp_lines,[1 2])',...
        lines(vp_lines,[3 4])','r')
    disp(vp_lines)
    pause
    %}    
end

vp_candidates = vp_candidates(1:count_vp);

[suitable_set,o,f] = find_vpoints(lines,vp_candidates,intn_pts,size_im,grayIm,vp_membership);


% We now display the image with all the vanishing points and corresponding lines
%{
for i = 1:size(suitable_set,1)
    display_points([vp_candidates(1),suitable_set(i,:)],intn_pts,lines,grayIm);
    k = waitforbuttonpress;
    if k==0
        disp(i)
        % i = 5 and 11 are the good ones, may change with code
    end
end
%}

