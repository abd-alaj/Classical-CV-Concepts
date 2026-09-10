clear; close all; 

% TODO: rewrite this in python to be cohesive with all other projects in repo

% create the csv and figures folder
if ~exist('csv_files', 'dir')
    mkdir('csv_files');
end 

if ~exist('figures', 'dir')
    mkdir('figures');
end

% inputs 
cam = [0; 0; 0];
p1 = [-1; 0; 2]; 
p2 = [1; 0; 5]; 
p3 = [0; 1; 4]; 
p4 = [0; -1; 3];
f = 1;

%stack pts for easier plotting
pts_3d = [p1, p2, p3, p4]; 
pts_3d_frame = [pts_3d, pts_3d(:, 1)];

% labels for easier annotation later on
labels = {'$p_1$', '$p_2$', '$p_3$', '$p_4$'};
qlabels = {'$q_1$', '$q_2$', '$q_3$', '$q_4$'};

figure(1); 
hold on;

% create the wireframe for the points
plot3(pts_3d_frame(1,:), pts_3d_frame(2,:), pts_3d_frame(3,:));
set(gca, 'ColorOrderIndex', 1); % resets the color index so the wire frame and points are the same color
scatter3(pts_3d(1,:), pts_3d(2,:), pts_3d(3,:), 'filled', 'LineWidth', 3);

% label the points and accentuate them
text(pts_3d(1,:), pts_3d(2,:), pts_3d(3,:), labels, 'VerticalAlignment', 'bottom');
grid on;

% place camera
scatter3(cam(1), cam(2), cam(3), 'rx', 'LineWidth', 2);
text(cam(1), cam(2), cam(3), 'Camera', 'VerticalAlignment', 'bottom');

xlabel('$x$-axis');
ylabel('$y$-axis');
zlabel('$z$-axis');

view(3);

hold off;

saveas(gcf, './figures/01_3d_view_of_points.png');

%% Projection of 3D plot into a 2D plane
P_true = true_perspective(p1, p2, p3, p4, f);
P_weak = weak_perspective(p1, p2, p3, p4, f);
error_val = SSD_error(P_true, P_weak);

P_true_closed = [P_true, P_true(:, 1)];
P_weak_closed = [P_weak, P_weak(:, 1)];

figure(2);
hold on; 

% plot true perspective
set(gca, 'ColorOrderIndex', 1);
frame_true = plot(P_true_closed(1, :), P_true_closed(2, :));
set(gca, 'ColorOrderIndex', 1);
plot(P_true(1, :), P_true(2, :), 'o', 'LineWidth', 3);

% plot weak perspective
set(gca, 'ColorOrderIndex', 2);
frame_weak = plot(P_weak_closed(1, :), P_weak_closed(2, :));
set(gca, 'ColorOrderIndex', 2);
plot(P_weak(1, :), P_weak(2, :), 'x', 'LineWidth', 3);

text(P_true(1,:), P_true(2,:), labels, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
text(P_weak(1,:), P_weak(2,:), qlabels, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');

axis equal; 
xlabel('$x$-axis image plane');
ylabel('$y$-axis image plane');

set(gca, 'ColorOrderIndex', 1);
legend([frame_true, frame_weak], 'True perspective', 'Weak perspective', 'Location', 'northeastoutside');
grid on; 

hold off; 

saveas(gcf, './figures/02_true_and_weak_perspective.png');

%% Sum of square diffs of each pts 

% this portion creates a csv file of the SSD of each point. 
% i do this because it makes importing them into typst easier
csv_write(P_true, P_weak, './csv_files/normal_projection_errors.csv');

%% Rotation of Object O

R = rotation_cc(45); 

rotated_pts = R * pts_3d;
P_true_rot = true_perspective(rotated_pts(:,1), rotated_pts(:,2), rotated_pts(:,3), rotated_pts(:,4), f);
P_true_rot_frame = [P_true_rot, P_true_rot(:, 1)];

P_weak_rot = weak_perspective(rotated_pts(:,1), rotated_pts(:,2), rotated_pts(:,3), rotated_pts(:,4), f);
P_weak_rot_frame = [P_weak_rot, P_weak_rot(:, 1)];

figure(3);
hold on; 

% plot True perspective
set(gca, 'ColorOrderIndex', 1);
rot_true = plot(P_true_rot_frame(1, :), P_true_rot_frame(2, :));
set(gca, 'ColorOrderIndex', 1);
plot(P_true_rot(1, :), P_true_rot(2, :), 'o');

% plot weak perspective
set(gca, 'ColorOrderIndex', 2);
rot_weak = plot(P_weak_rot_frame(1, :), P_weak_rot_frame(2, :));
set(gca, 'ColorOrderIndex', 2);
plot(P_weak_rot(1, :), P_weak_rot(2, :), 'x', 'LineWidth', 3);

text(P_true_rot(1,:), P_true_rot(2,:), labels, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');
text(P_weak_rot(1,:), P_weak_rot(2,:), qlabels, 'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right');

axis equal; 

xlabel('$x$-axis image plane');
ylabel('$y$-axis image plane');
set(gca, 'ColorOrderIndex', 1);
legend([rot_true, rot_weak], 'True perspective', 'Weak perspective', 'Location', 'northeastoutside');

grid on; 
hold off;

saveas(gcf, './figures/03_true_and_weak_perspective_rotated.png');

% This calculates sumsqr diff but puts it in a .csv file instead.
csv_write(P_true_rot, P_weak_rot, './csv_files/rotated_projection_errors.csv');
