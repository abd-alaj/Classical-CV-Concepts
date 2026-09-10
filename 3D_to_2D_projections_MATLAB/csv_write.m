function csv_write(P_true, P_weak, filename)

    num_pts = size(P_true, 2);
    point_errors = zeros(num_pts, 2);

    for i = 1:num_pts
        p_true_i = P_true(:, i);
        p_weak_i = P_weak(:, i);         
        e_i = SSD_error(p_true_i, p_weak_i);
        point_errors(i, :) = [i, e_i];
    end
    csvwrite(filename, point_errors);    
end