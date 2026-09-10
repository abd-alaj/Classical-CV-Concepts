function rotationMatrix = rotation_cc(ang)
    % converting to radians
    theta = deg2rad(ang); 
    
    r = [cos(theta), -sin(theta), 0;
         sin(theta),  cos(theta), 0;
         0,           0,          1];
         
    rotationMatrix = r;
end