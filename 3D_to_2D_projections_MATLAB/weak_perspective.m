function proj = weak_perspective(q1, q2, q3, q4, focal_point)
    % stack all pts into 1 mat
    pts_3d = [q1, q2, q3, q4];

    % isotopic scaling factor f / Z_0
    s = focal_point / mean(pts_3d(3, :)); 

    x_proj = s .* pts_3d(1, :); 
    y_proj = s .* pts_3d(2, :);

    proj = [x_proj; y_proj];
end
