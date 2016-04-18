function [res,o,f] = orthogonality_criteria(i,j,k,pts,size_im)
% This function, returns true for the set of points, such that their
% positon vectors are mutually perpendicular
res = true;
o = inf;
f = inf;
% first we check the number of vanishing points that are at infinity, and
% we indicate that with a 0 or 1, with 1 meaning that the point is at Inf
list = [[i,j,k]',zeros(3,1)];
n =0;
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
    [o,f] = find_ortho_focal_0(i,j,k,pts);
elseif(n==1)
    ind_finite = find(list(:,2) ~= 1);
    [o,f] = find_ortho_focal_1(ind_finite(1),ind_finite(2),pts,size_im);
else
    o = noninf_point;
end

% check if the determined values of o, f are feasible
res = check_ortho_focal(o,f,size_im,res);
end

function [o,f] = find_ortho_focal_0(i,j,k,pts)
% We first find the orthocentre of the triangle, and estimate the focal
% length of the camera from it.
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

% Now for the orthocentre
m1 = (pts(i,2)-pts(k,2))/(pts(i,1)-pts(k,1));%slope between i&k
m1 = -1/m1; %slope of perpendicular from j

x = (pts(k,2)-pts(j,2)+m1*pts(j,1)-m2*pts(k,1))/(m1-m2);
y = m1*(x-pts(j,1))+pts(j,2);
o = [x,y]; % o is the orthocentre of triangle ijk

% Now we use the property that f = sqrt(d1*d2), where d1, and d2 are the
% distances from the ends of the line segment to the point P,where the
% perperndicular from O(camera origin) falls on the segment.
% Note that this point P is the same as p, made by perpendicular from the
% orthocentre 'o', this is because O,o and P are in the same plane, which
% is perpendicular to the line segment.
d1 = sqrt((p(1)-pts(j,1))^2+(p(2)-pts(j,2))^2);
d2 = sqrt((p(1)-pts(i,1))^2+(p(2)-pts(i,2))^2);
f = sqrt((d1*d2));
end

function [o,f] = find_ortho_focal_1(i,j,pts,size_im)
% We first find the orthocentre of the triangle by estimating the point 
% closest to the centre of the image lying on the line segment and estimate
% the focal length of the camera from it, as done in find_ortho_focal_0.

end

function res = check_ortho_focal(o,f,size_im,res)
% This function returns the logical AND of initial value of res and the
% value computed in this function. The value computed is true if the values
% of 'o' and 'f' are within reasonable limits
end