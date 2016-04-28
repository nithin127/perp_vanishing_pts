check_set = zeros(3,numel(vp_candidates)^3); %pre-allocation for speed
count = 0;
for i = 1:numel(vp_candidates)
    for j = i+1:numel(vp_candidates)
        for k = j+1:numel(vp_candidates)
            count = count+1;
            check_set(:,count) = [i;j;k];
        end
    end
end
check_set = check_set(:,1:count);


count = 0;

for set = check_set;
    count = count+1;
    i = vp_candidates(set(1));
    j = vp_candidates(set(2));
    k = vp_candidates(set(3));

    %{.
    list = [[i,j,k]',zeros(3,1)];
    n = 0;
    for t = 1:3
        if(intn_pts(list(t,1),2)==inf)
            n = n+1;
            list(t,2) = 1;
        end
    end    
    %}

    m1 = (intn_pts(i,2)-intn_pts(j,2))/(intn_pts(i,1)-intn_pts(j,1)); %slope between i&j
    m2 = -1/m1; %slope of perpendicular from k


    x = (intn_pts(k,2)-intn_pts(j,2)+m1*intn_pts(j,1)-m2*intn_pts(k,1))/(m1-m2);
    y = m1*(x-intn_pts(j,1))+intn_pts(j,2);
    p = [x,y];


    %{.
    x_range = zeros(5,2);
    figure(1), hold off, imshow(grayIm)
    figure(1), hold on, plot([intn_pts(i,1),intn_pts(j,1),intn_pts(k,1),x],...
        [intn_pts(i,2),intn_pts(j,2),intn_pts(k,2),y],'o')
    figure(1), hold on, plot([intn_pts(i,1);intn_pts(j,1)],[intn_pts(i,2);...
        m1*(intn_pts(j,1)-intn_pts(i,1))+intn_pts(i,2)],'r')
    x_range(1:3,1:2) = [intn_pts([i,j,k],1),intn_pts([i,j,k],2)];
    axis([min(0,min(x_range(:,1))) max(size_im(1),max(x_range(:,1))) ...
        min(0,min(x_range(:,2))) max(size_im(2),max(x_range(:,2)))])
    figure(1), hold on, plot([intn_pts(k,1);...
        10*intn_pts(j,1)],[intn_pts(k,2);...
        -1/m1*(10*intn_pts(j,1)-intn_pts(k,1))+intn_pts(k,2)],'b')
    %pause
    %}

    m1 = (intn_pts(i,2)-intn_pts(k,2))/(intn_pts(i,1)-intn_pts(k,1));%slope between i&k
    m_2 = -1/m1; % slope of perpendicular from j

    x_r = (intn_pts(k,2)-intn_pts(j,2)+m_2*intn_pts(j,1)-m2*intn_pts(k,1))/(m_2-m2);
    y_r = m_2*(x-intn_pts(j,1))+intn_pts(j,2);
    o = [x_r,y_r]; % o is the orthocenter of triangle ijk

    figure(1), hold on, plot([intn_pts(i,1);intn_pts(k,1)],[intn_pts(i,2);...
        m1*(intn_pts(k,1)-intn_pts(i,1))+intn_pts(i,2)],'r')
    figure(1), hold on, plot([intn_pts(j,1);55],[intn_pts(j,2);...
        -1/m1*(55-intn_pts(j,1))+intn_pts(j,2)],'b')
    figure(1), hold on, plot(x_r,y_r,'bo')
    x_range(4:5,1:2) = [x,y;x_r,y_r];
    axis([min(0,min(x_range(:,1))) max(size_im(1),max(x_range(:,1))) ...
        min(0,min(x_range(:,2))) max(size_im(2),max(x_range(:,2)))])
    x_range = [];
    th = 0:pi/50:2*pi;
    xunit = 10000 * cos(th) + x_r;
    yunit = 10000 * sin(th) + y_r;
    figure(1), hold on, plot(xunit, yunit);

    vx = [intn_pts(i,1);intn_pts(j,1);intn_pts(k,1)];
    vy = [intn_pts(i,2);intn_pts(j,2);intn_pts(k,2)];
    res = inpolygon(o(1),o(2),vx,vy);
    disp(res)
    pause

    k = waitforbuttonpress;
        if k==0
            disp('check the index:')
            disp(count)
            % i = 5 and 11 are the good ones, may change with code
        end

end
