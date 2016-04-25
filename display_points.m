function x = display_points(vp,intn_pts,lines,grayIm)
% This also includes all the codes to display images, intersections etc.

vp_1 = vp(1);
vp_2 = vp(2);
vp_3 = vp(3);
size_im = size(grayIm);

%{.
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
%}


%{
% displaying image
figure(1), hold off, imshow(grayIm)
figure(1), hold on, plot(lines(:, [1 2])', lines(:, [3 4])')
%pause
%}

%{
%plot intersection points
ind = find((intn_pts(:,2) ~= inf)&(intn_pts(:,5)==1));
figure, imshow(grayIm), hold on
plot(intn_pts(ind,1),intn_pts(ind,2),'o')
%}


 %{
    % displaying most voted points and their lines
    for i = 1:30
    figure(2), hold off, imshow(1/5*grayIm)
    figure(2), hold on, plot(lines(intn_pts(num_1(end-i),3:4),[1 2])',...
        lines(intn_pts(num_1(end-i),3:4),[3 4])')
    pause
    end
 %}

  %{
    % display the lines voting for the selected point in each iteration
    vp_1 = num(end);
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(vp_lines,[1 2])',...
        lines(vp_lines,[3 4])','r')
    pause
    %}  


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

end

