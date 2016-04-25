function res = check_threshold_vlines(i,j,lines,intn_pts,a_thres,d_thres,vp_membership)
% If either of the points are at Inf, then the criteria is satisied, if 
% both are at Inf, then the criteria doesn't apply thus we'll return the 
% min_angle possible.

if (intn_pts(i,2)==inf && intn_pts(j,2)==inf)    
    res = true;
    for s = [i,j]
        ang_line = lines(s,5);        
        com_lines = vp_membership{s};    
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
    set_1_com = vp_membership{i};
    set_2_com = vp_membership{j};
    com_lines = intersect(set_1_com,set_2_com);
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
    set_1_com = vp_membership{i};
    set_2_com = vp_membership{j};
    com_lines = intersect(set_1_com,set_2_com);
    for l_t = com_lines
        l = lines(l_t,:);
        ang_diff = abs(atan(m1) - l(5));
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
