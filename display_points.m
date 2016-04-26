function x = display_points(vp_candidates,intn_pts,lines,grayIm,vp_membership)
% This also includes all the codes to display images, intersections etc.

%{.

    vp_1 = vp_candidates(1);
    vp_2 = vp_candidates(2);
    vp_3 = vp_candidates(3);
    size_im = size(grayIm);

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

%%

    %{
    % displaying image
    figure(1), hold off, imshow(grayIm)
    figure(1), hold on, plot(lines(:, [1 2])', lines(:, [3 4])')
    %pause
    %}
%%

    %{
    %plot intersection points
    ind = find((intn_pts(:,2) ~= inf)&(intn_pts(:,5)==1));
    x = intn_pts(ind,1:2);
    figure, imshow(1/5*grayIm), hold on
    plot(intn_pts(ind,1),intn_pts(ind,2),'o')
    axis([min(0,min(x(:,1))) max(size_im(1),max(x(:,1))) ...
        min(0,min(x(:,2))) max(size_im(2),max(x(:,2)))])
    %}

%%

 %{
    % displaying most voted points and their lines
    for i = 1:30
    figure(2), hold off, imshow(1/5*grayIm)
    figure(2), hold on, plot(lines(intn_pts(num_1(end-i),3:4),[1 2])',...
        lines(intn_pts(num_1(end-i),3:4),[3 4])')
    pause
    end
 %}
%%

  %{
    % display the lines voting for the selected point in each iteration
    %vp_1 = num(end);
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(vp_lines,[1 2])',...
        lines(vp_lines,[3 4])','r')
    pause
    %}  

%%

%{
    %{
    count = 0;
    suitable_set = zeros((numel(vp_candidates)-1)^2,2);
    for i = 2:numel(vp_candidates)-1
        for j = i+1:numel(vp_candidates)-1
            count = count+1;
            suitable_set(count,:) = [vp_candidates(i), vp_candidates(j)];
        end
    end
    suitable_set = suitable_set(1:count,:);
    %}

    suitable_set = [vp_candidates(2),vp_candidates(9);...
        vp_candidates(2),vp_candidates(11);...
        vp_candidates(2),vp_candidates(13)];

    value_set = vote_init(suitable_set(:,1))+vote_init(suitable_set(:,2));
    [~,ind_s] = sort(value_set,'descend');
    for i = 1:size(suitable_set,1)
        vp_2 = suitable_set(ind_s(i),1);
        vp_3 = suitable_set(ind_s(i),2);
        disp([vp_1,vp_2,vp_3]);
        x = intn_pts([vp_1,vp_2,vp_3],1:2);
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

%%

%{
    % Debugging vanishing lines criteria
      

    for set = [1,2; 1,4;2,4]'        
        set_1_com = vp_membership{set(1)};
        set_2_com = vp_membership{set(2)};
        vp_lines = intersect(set_1_com,set_2_com);
        figure(3), hold off, imshow(1/5*grayIm)
        figure(3), hold on, plot(lines(set_1_com,[1 2])',...
            lines(set_1_com,[3 4])','r')
        pause
        figure(3), hold off, imshow(1/5*grayIm)
        figure(3), hold on, plot(lines(set_2_com,[1 2])',...
            lines(set_2_com,[3 4])','r')
        pause
        figure(3), hold off, imshow(1/5*grayIm)
        figure(3), hold on, plot(lines(vp_lines,[1 2])',...
            lines(vp_lines,[3 4])','r')
        v_line_pt = [intn_pts(set(1),1:2);intn_pts(set(2),1:2)];
        figure(3), hold on, plot(v_line_pt(:,1),v_line_pt(:,2),'b')
        pause
    end
    %}  

end

