import os
import matplotlib.pyplot as plt
import numpy as np

from skimage import io, feature, color, util, draw
from skimage.color import rgb2gray
from numpy import linalg
from PIL import Image    

def matplot_to_rgbarray(fig):
    # logic to return a matplot fig to an rgb one 
    # this is John Matlab punishing me for insisting on the use of python
    fig.canvas.draw()
    
    rgba_buffer = fig.canvas.buffer_rgba()
    output = np.frombuffer(rgba_buffer, dtype=np.uint8)
    w, h = fig.canvas.get_width_height()
    output = output.reshape((h, w, 4))
    output = output[:, :, :3]
    
    plt.close(fig)
    return output

def line_detector(img): 

    # take image and use canny feature
    # matlab uses a default sigma of sqrt(2), this is much more accurate to an expected matlab output
    edge_img = feature.canny(color.rgb2gray(img), sigma=np.sqrt(2))

    # only the white lines on the edges of the road are preserved using this line instead, this is much faster for evaluation purposes
    # edge_img = feature.canny(color.rgb2gray(img), sigma=1, low_threshold=0.4, high_threshold=1.2)

    # sampling freq
    theta_sample_frequency = 0.01 
    rows, cols = (edge_img.shape)

    # this should stay an integer because stepping by 1 through rho
    rho_lim = int(np.ceil(np.linalg.norm([rows, cols])))

    # initialize ranges of rho and theta which will be stepped through
    rho = np.arange(-rho_lim, rho_lim, 1)
    theta = np.arange(0, np.pi, theta_sample_frequency)
    num_thetas = len(theta)
    num_rhos = len(rho)

    # creating an accumulator array with the length of rhos and thetas. 
    acc = np.zeros((num_rhos, num_thetas))

    ## Performing the hough transform
    # translating matlab code into python is thankfully very nice because I do not need to worry about row/column indexing
    for indrows in range(rows):
        for indcols in range(cols):
            if edge_img[indrows, indcols] == 1: 
                for theta_max in range(num_thetas):
                    
                    th = theta[theta_max]
                    r = indcols * np.cos(th) + indrows * np.sin(th)
                    
                    # this needs to stay an int bc it will go out of bounds otherwise. 
                    rho_max = int(round(r + rho_lim))     
                    if 0 <= rho_max < num_rhos:
                        acc[rho_max, theta_max] = acc[rho_max, theta_max] + 1


    I = np.argmax(acc) # grab linear index of max val
    M = acc.flat[I] # grab max val

    # we need to unravel the index to keep this code as close to matlab as possible
    rho_max_idx, theta_max_idx = np.unravel_index(I, acc.shape)
    
    # 2D Heatmap for accumulator
    fig_acc, ax_acc = plt.subplots()

    # 'extent' maps the indices to the actual theta and rho values for the axes
    im = ax_acc.imshow(acc, cmap='magma', extent=[theta[0], theta[-1], -rho_lim, rho_lim], aspect='auto', origin='lower')
    
    # Add the yellow circle marker at the peak of the LHT heatmap
    # We use the actual values from the theta and rho arrays based on the detected indices
    ax_acc.plot(theta[theta_max_idx], rho[rho_max_idx], 'o', fillstyle='none', color='yellow', markersize=10)
    
    ax_acc.set_title('Line Hough Space Heatmap')
    ax_acc.set_xlabel('Theta (radians)')
    ax_acc.set_ylabel('Rho (pixels)')
    plt.colorbar(im, ax=ax_acc, label='Votes')
    plt.savefig('hough_line_heatmap.png')

    m = - (np.cos(theta[theta_max_idx]) / np.sin(theta[theta_max_idx]))
    b = (rho[rho_max_idx]) / np.sin(theta[theta_max_idx])
    x_vals = np.arange(0, cols) 
    y_vals = m * x_vals + b

    fig, ax = plt.subplots()
    ax.imshow(img, cmap='gray')
    # Plotting x vs y (y vs x in image coordinates)
    ax.plot(x_vals, y_vals, 'g', linewidth=2)
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.axis('off')
    plt.tight_layout(pad=0)
    
    plt.savefig('output_line_detector.png')
    return matplot_to_rgbarray(fig)

def circle_detector(img, radii):
    gray = color.rgb2gray(img)
    
    edge_img = feature.canny(gray, sigma=np.sqrt(2), low_threshold=0.2, high_threshold=0.4)
    rows, cols = edge_img.shape
    
    theta = np.arange(0, 2 * np.pi, 0.01)
    results_img = np.copy(img)

    for r in radii:
        # Initialize Accumulator
        acc = np.zeros((rows, cols))
        
        # CHT Algorithm is implemented here
        edge_pixels = np.argwhere(edge_img > 0)
        for y, x in edge_pixels:
            for t in theta:
                a = int(x - r * np.cos(t))
                b = int(y - r * np.sin(t))
                if 0 <= a < cols and 0 <= b < rows:
                    acc[b, a] += 1
        
        max_idx = np.argmax(acc)

        # Convert flattened index back to (row, col)
        peak_b, peak_a = np.unravel_index(max_idx, acc.shape)
        
        # graphingg hs for this radis
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # 2D Heatmap for Circle Accumulator
        ax1.set_title(f"Hough Space Heatmap (Radius {r})")
        im = ax1.imshow(acc, cmap='hot')
        plt.colorbar(im, ax=ax1, label='Votes')

        # Mark the highest point in hs
        ax1.plot(peak_a, peak_b, 'cx', markersize=10) 

        # mark highest accumulator val on the image
        # Drawing yellow circle with thickness using multiple perimeters
        for thickness in range(4):
            rr, cc = draw.circle_perimeter(peak_b, peak_a, r + thickness, shape=results_img.shape)
            results_img[rr, cc] = [206, 16, 197] # experimenting with colors that contrast well with the image
        
        # Draw a larger solid disk for the center point
        rr_c, cc_c = draw.disk((peak_b, peak_a), 5, shape=results_img.shape)
        results_img[rr_c, cc_c] = [255, 0, 0] # Red center (larger radius)

        ax2.set_title(f"Detected Peak (Radius {r})")
        ax2.imshow(results_img)
        
        plt.savefig(f'output_circle_r{r}.png')
        plt.show()

    return results_img

if __name__ == "__main__": 

    dime_size = 25
    penny_size = 31

    road_img = io.imread("./test1.jpg")
    coins_img = io.imread("./test2.jpg")

    img_line = line_detector(road_img)
    result_circle = circle_detector(coins_img, [dime_size, penny_size])