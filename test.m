
count = 0;

suitable_set = zeros(numel(vp_candidates)^2,3);
for i = 3:numel(vp_candidates)
    count = count+1;
    suitable_set(count,:) = [1,2,i];    
end

suitable_set = suitable_set(1:count,:);

%{
for t = suitable_set'
    k = vp_candidates(t(1));
    i = vp_candidates(t(2));
    j = vp_candidates(t(3));

    vp_1 = k;
    vp_2 = i;
    vp_3 = j;

    x = intn_pts([vp_1,vp_2,vp_3],1:2);
    figure(3), hold off, imshow(1/5*grayIm)
    figure(3), hold on, plot(lines(vp_membership{t(1)},[1 2])',...
    lines(vp_membership{t(1)},[3 4])','r')
    figure(3), hold on, plot(lines(vp_membership{t(2)},[1 2])',...
    lines(vp_membership{t(2)},[3 4])','b')
    figure(3), hold on, plot(lines(vp_membership{t(3)},[1 2])',...
    lines(vp_membership{t(3)},[3 4])','g')
    hold on, plot(intn_pts(vp_1,1),intn_pts(vp_1,2),'ro')
    hold on, plot(intn_pts(vp_2,1),intn_pts(vp_2,2),'bo')
    hold on, plot(intn_pts(vp_3,1),intn_pts(vp_3,2),'go')
    k = waitforbuttonpress;
    if k == 0
        disp(t)
    end
    %axis([min(0,min(x(:,1))) max(size_im(1),max(x(:,1))) ...
        %min(0,min(x(:,2))) max(size_im(2),max(x(:,2)))])
    %[res,o,f] = orthogonality_criteria(i,j,k,intn_pts,size_im,lines);
end
%}
