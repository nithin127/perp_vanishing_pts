function vote = vote_points(cross,lines)
% This function returns the vote value of all the intersection points
%vote = cell(size(cross,1),1);
vote = zeros(size(cross,1),1);
sigma = 0.1;
ind = find(cross(:,5)==1);
v_all = zeros(size(ind,1)*size(lines,1),1);
mean_v =[];
median_v =[];
mode_v =[];
for i_t = 1:size(ind,1)
    count = 0;
    i = ind(i_t);
    v_tot = 0;
    v_line = zeros(1,size(lines,1)); %pre-allocating for speed :P
    cnt =0;
    for j = 1:size(lines,1)
        if (cross(i,1)==inf)
            ang = cross(i,4);
        else
            ang = atan((cross(i,2)-0.5*(lines(j,3)+lines(j,4)))/...
            (cross(i,1)-0.5*(lines(j,1)+lines(j,2))));
        end
        ang = abs(ang - lines(j,5));
        len = sqrt((lines(j,1)-lines(j,2))^2+(lines(j,3)-lines(j,4))^2);
        v = len*exp(-ang/(2*sigma*sigma));  
        %if (v>threshold)
            %only counts the votes above a given threshold
            cnt = cnt +1;
            count = count+1;
            v_tot = v_tot + v;
            v_line(cnt) = v;
            v_all(count) = v;
        %end
    end
    vote(i) = v_tot;
    v_line = v_line(1:cnt);
    %vote{i} = {v_tot,v_line};    
    mean_v = [mean_v, mean(v_line)];
    median_v = [median_v ,median(v_line)];
    mode_v = [mode_v, mode(round(v_line))];
end
mean_t = mean(v_all);
median_t = median(v_all);
mode_t = round(mode(v_all));