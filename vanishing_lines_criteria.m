function res = vanishing_lines_criteria(i,j,vp_1,lines,intn_pts,vote_matrix,~)
% This function returns true, if the points satisfy the vanishing lines
% criteria, (See Rother['02] for details). It also returns true if the
% vanishing line doesn't exist, i.e both the vanishing points are at Inf

% We define the thresholds here
a_thres = 5*pi/180;
d_thres = 30;

res1 = check_theshold_vlines(i,j,lines,intn_pts,vote_matrix,a_thres,d_thres);

res2 = check_theshold_vlines(i,vp_1,lines,intn_pts,vote_matrix,a_thres,d_thres);

res3 = check_theshold_vlines(j,vp_1,lines,intn_pts,vote_matrix,a_thres,d_thres);

res = res1&&res2&&res3;

%figure(2), hold off, imshow(1/5*grayIm)
%{
if (res == true)    
    figure(2), hold on, plot(lines(intn_pts(i,3:4),[1 2])',...
    lines(intn_pts(i,3:4),[3 4])','r')
    figure(2), hold on, plot(lines(intn_pts(j,3:4),[1 2])',...
    lines(intn_pts(j,3:4),[3 4])','b')
    figure(2), hold on, plot(lines(intn_pts(vp_1,3:4),[1 2])',...
    lines(intn_pts(vp_1,3:4),[3 4])','g')
    disp([i,j,vp_1])% checking purpose
    pause
end
%}
end

function res = check_theshold_vlines(i,j,lines,intn_pts,vote_matrix,a_thres,d_thres)
% If either of the points are at Inf, then the criteria is satisied, if 
% both are at Inf, then the criteria doesn't apply thus we'll return the 
%min_angle possible.

if (intn_pts(i,2)==inf && intn_pts(j,2)==inf)    
    res = true;
    for s = [i,j]
        ang_line = lines(s,5);
        com_lines = vote_matrix{s}{2};
        if (res==true)
            for l = com_lines
                ang_diff = abs(ang_line - lines(l,5));
                if(ang_diff>a_thres)
                    res = false;
                    break;
                end
            end
        end
    end
elseif (intn_pts(i,2)==inf || intn_pts(j,2)==inf)
    if (intn_pts(i,2)==inf )
        x_inf = i; x_fin = j;
    else 
        x_inf = j; x_fin = i;
    end
    % Now let's estimate the angle and distance of each common line segment
    % from the vanishing line
    res = true;
    ang_line = lines(x_inf,5);
    m1 = tan(ang_line);
    com_lines = intersect(vote_matrix{i}{2},vote_matrix{j}{2});
    for l = com_lines
        ang_diff = abs(ang_line - lines(l,5));
        m2 = -1/tan(ang_line);
        p_mid = [(l(1)+l(2))/2 , (l(3)+l(4))/2]; %mid-point of line seg
        x = (p_mid(2)-intn_pts(x_fin,2)+m1*intn_pts(x_fin,1)-m2*p_mid(1)/(m1-m2));
        y = m1*(x-intn_pts(x_fin,1))+intn_pts(x_fin,2);        
        % here x,y is the foot of the perpendicular from p_mid
        d = sqrt((p_mid(1)-x)^2 + (p_mid(2)-y)^2);
        if(ang_diff>a_thres || d > d_thres)
            res = false;
            break;
        end
    end
else
    res = true;
    m1 = (intn_pts(i,2)-intn_pts(j,2))/(intn_pts(i,1)-intn_pts(j,1));
    com_lines = intersect(vote_matrix{i}{2},vote_matrix{j}{2});
    for l_t = 1:size(com_lines,1)
        l = lines(com_lines(l_t),:);
        ang_diff = abs(atan(m1) - lines(l,5));
        m2 = -1/m1;
        p_mid = [(l(1)+l(2))/2 , (l(3)+l(4))/2]; %mid-point of line seg
        x = (p_mid(2)-intn_pts(i,2)+m1*intn_pts(i,1)-m2*p_mid(1)/(m1-m2));
        y = m1*(x-intn_pts(i,1))+intn_pts(i,2);        
        % here x,y is the foot of the perpendicular from p_mid
        d = sqrt((p_mid(1)-x)^2 + (p_mid(2)-y)^2);
        if(ang_diff>a_thres || d > d_thres)
            res = false;
            break;
        end
    end
end
end
