function bin = create_bin(intn_pts,size_im, ~,no_of_points,no_of_bins,vote)
% Let us use the following approach to creating bins, all the points at
% infinity should individually occupy separate bins.
% Points close to the centre or points inside the image should occupy bins
% of lesser size
% We will only consider the point having the maximum group membership.
% Ideally, bins should be formed out of points having the similar line
% membership. We will try to do this later
% here we are going to select 
%here bins are of the form a0R^2 (geometric progression)
    [~, sort_ind] = sort(sqrt((intn_pts(:,1)-(size_im(1)/2)).^2+ (intn_pts(:,2)-(size_im(2)/2)).^2));
    number_of_points = ceil(no_of_points/no_of_bins);
    for i = 1:no_of_bins
        index = number_of_points*(i-1)+1 : number_of_points*(i);
        sort_vote = vote((sort_ind(index)),1);
        [~, sort_ind_vote] = sort(sort_vote(end-number_of_points+1:end));
        bin((i-1)*number_of_points+1:(i)*number_of_points,1) = sort_ind(index(sort_ind_vote(end-number_of_points+1:end)));
    end
end
