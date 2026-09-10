function proj = true_perspective(p1, p2, p3, p4, focal_point)

    % stack all pts into 1 mat
    pts_3d = [p1, p2, p3, p4];

    x_proj = focal_point * (pts_3d(1, :) ./ pts_3d(3, :)); 
    y_proj = focal_point * (pts_3d(2, :) ./ pts_3d(3, :));

    proj = [x_proj; y_proj];
end