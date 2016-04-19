function [res,o,f] = orthogonality_criteria(i,j,k,pts,size_im,lines)
% This function, returns true for the set of points, such that their
% positon vectors are mutually perpendicular

o = inf;
f = inf;
% first we check the number of vanishing points that are at infinity, and
% we indicate that with a 0 or 1, with 1 meaning that the point is at Inf
list = [[i,j,k]',zeros(3,1)];
n = 0;
for t = 1:3
    if(pts(list(t,1),2)==inf)
        n = n+1;
        list(t,2) = 1;
    end
end    

% determining f and o, case-wise for each possible value of n
if(n==3)
    res=false;
elseif(n==0)
    [o,f,res] = find_ortho_focal_0(i,j,k,pts);
elseif(n==1)
    ind_finite = find(list(:,2) ~= 1);
    ind_inf = find(list(:,2) == 1);
    % inputs only the finite indices into the function
    [o,f,res] = find_ortho_focal_1(ind_finite(1),ind_finite(2),ind_inf...
        ,pts,size_im,lines);
else
    o = list((list(:,2) ~= 1),1);
    ind_inf = find(list(:,2) == 1);
    [res] = find_ortho_focal_2(ind_inf(1),ind_inf(2),pts,lines);
end

% check if the determined values of o, f are feasible
res = check_ortho_focal(o,f,size_im,res);
end

function [o,f,res] = find_ortho_focal_0(i,j,k,pts)
% We first find the orthocenter of the triangle, and estimate the focal
% length of the camera from it. The function returns true if the
% orthocenter iles inside the triangle

m1 = (pts(i,2)-pts(j,2))/(pts(i,1)-pts(j,1)); %slope between i&j
m2 = -1/m1; %slope of perpendicular from k

% To calculate the point of intersection
% y = m1(x-x1) + y1
% y = m2(x-x2) + y2
% =>x = (y2-y1+m1x1-m2x2)/(m1-m2)

x = (pts(k,2)-pts(j,2)+m1*pts(j,1)-m2*pts(k,1))/(m1-m2);
y = m1*(x-pts(j,1))+pts(j,2);
p = [x,y];
% p is the point of intersection of perpendicular from k to the line
% segment ij

% Now for the orthocenter
m1 = (pts(i,2)-pts(k,2))/(pts(i,1)-pts(k,1));%slope between i&k
m1 = -1/m1; %slope of perpendicular from j

x = (pts(k,2)-pts(j,2)+m1*pts(j,1)-m2*pts(k,1))/(m1-m2);
y = m1*(x-pts(j,1))+pts(j,2);
o = [x,y]; % o is the orthocenter of triangle ijk

% Now we use the property that f = sqrt(d1*d2), where d1, and d2 are the
% distances from the ends of the line segment to the point P,where the
% perperndicular from O(camera origin) falls on the segment.
% Note that this point P is the same as p, made by perpendicular from the
% orthocenter 'o', this is because O,o and P are in the same plane, which
% is perpendicular to the line segment.
d1 = sqrt((p(1)-pts(j,1))^2+(p(2)-pts(j,2))^2);
d2 = sqrt((p(1)-pts(i,1))^2+(p(2)-pts(i,2))^2);
f = sqrt((d1*d2));

% Now let's check if the point lies inside the orthocenter
vx = [pts(i,1);pts(j,1);pts(k,1)];
vy = [pts(i,2);pts(j,2);pts(k,2)];
res = inpolygon(o(1),o(2),vx,vy);
end

function [o,f,res] = find_ortho_focal_1(i,j,k,pts,size_im, lines)
% We first find the orthocenter of the triangle by estimating the point 
% closest to the centre of the image lying on the line segment and estimate
% the focal length of the camera from it, as done in find_ortho_focal_0.
% The function returns true if the vanishing line of v1,v2 is perpendicular
% to the infinite vanishing point direction

m1 = (pts(i,2)-pts(j,2))/(pts(i,1)-pts(j,1)); %slope between i&j
m2 = -1/m1; %slope of perpendicular from image centre
c = round(size_im/2);  % position of centre of image
x = (c(2)-pts(j,2)+m1*pts(j,1)-m2*c(1))/(m1-m2);
y = m1*(x-pts(j,1))+pts(j,2);
p = [x,y];
% p is the point of intersection of perpendicular from centre of the image
% to the line segment ij. Now, this is the orthocenter of the image.
d1 = sqrt((p(1)-pts(j,1))^2+(p(2)-pts(j,2))^2);
d2 = sqrt((p(1)-pts(i,1))^2+(p(2)-pts(i,2))^2);
f = sqrt((d1*d2));
o = p;
% Impose condition that the infinite vanishing point has a slope
% perpendicular to m1
mx = tan(lines(pts(k,3),5));
check = mx*m1+1;
% Impose tighter condition, if analysis fails
if (abs(check)>1e-2)
    res = false;
else
    res = true;
end
end

function [res] = find_ortho_focal_2(i,j,pts,lines)
mx = tan(lines(pts(i,3),5));
my = tan(lines(pts(j,3),5));
check = mx*my+1;
if (abs(check)>1e-2)
    res = false;
else
    res = true;
end
end

function res = check_ortho_focal(o,f,size_im,res)
% This function returns the logical AND of initial value of res and the
% value computed in this function. The value computed is true if the values
% of 'o' and 'f' are within reasonable limits

% define threshold values
f_thres_h = inf;
f_thres_l = 0;
o_limit = inf;

res_x = true;
if (f ~= inf)
    if ~(f>=f_thres_l && f<=f_thres_h)
        res_x = false;
    end
end
chck_o = o>= (round(size_im/2)-o_limit)& o<=(round(size_im/2)+o_limit);
% to make sure that it is within a o_limit distance from the centre
if ~(chck_o(1)&&chck_o(2))
    res_x = false;
end
res = res && res_x;
end