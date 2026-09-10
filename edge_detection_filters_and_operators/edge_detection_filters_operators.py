import os
import numpy as np
from scipy import ndimage
from skimage import io, feature, filters, color, util
from skimage.color import rgb2gray
from skimage.util import random_noise
import matplotlib.pyplot as plt 

# this creates the directory structure of all figures and output files, 
# a symlink is made to be imported into latex for report creation
# without errors of directories not existing 
# it is not very important or relevant to the assignment,
# but it helps in automating the entire process for easier grading

def make_directory_structure(): 
    directory_structure = [
        "./figures/graphs/png",
        "./figures/graphs/svg",
        "./figures/output_files/png",
        "./figures/output_files/svg",
        "./figures/noisy_imgs",
    ]

    for directory in directory_structure: 
        os.makedirs(directory, exist_ok=True)

def calculate_rmse(control, current_img): 
    # matlab does this automatically, but python does not
    # logic is created to generate float arrays from the images
    gt = util.img_as_float(control)
    curr = util.img_as_float(current_img)

    mse = np.mean((gt - curr) ** 2)
    return np.sqrt(mse)

def filter_img(img, method):
    match method: 
        case 'Sobel':
            return filters.sobel(img)
        case 'Prewitt':
            return filters.prewitt(img)
        case 'Laplacian of Gaussian':
            return ndimage.gaussian_laplace(img, 1.0)
        case 'Canny Detection':
            # set matlab thresh to a scalar val of 0.1
            # in matlab, if a scalar value is given as thresh arg, it will automatically take 0.4 * thresh
            # this is to mimick that feature in matlab
            return feature.canny(img, sigma=1.0, low_threshold=(0.4 * 0.1), high_threshold=0.1)

    
def generate_edge_filter_imgs(img, canny_control, noise_level, methods):
    rows = 2
    columns = 3

    for m_idx, name in enumerate(methods): 
        figure, ax_arr = plt.subplots(rows, columns)
        plt.suptitle(f"Using {name} for Edge Detection", fontname='CMU Serif', fontsize=14)
        axes = ax_arr.flatten()

        for n_idx, n_var in enumerate(noise_level):
            #gassian noise is added to make a noisy image
            noisy_img = util.random_noise(img, mode='gaussian', var=n_var)
            if m_idx == 0: 
                plt.imsave(f"./figures/noisy_imgs/noisy_image_{n_var}.png", noisy_img, cmap='gray')

            #filter image in regards to what method is being used
            edge_img = filter_img(noisy_img, name)

            error = calculate_rmse(canny_control, edge_img)
            rmse_val[m_idx, n_idx] = error

            print(f"RMSE of {name} with noise level {n_var}:\t{error}")

            #plot the image on a 2 by 3 grid
            axes[n_idx].imshow(edge_img, cmap='gray')
            axes[n_idx].set_title(f"noise level: {n_var}", fontname='CMU Serif', fontsize=12)

        plt.tight_layout()

        plt.savefig(f"./figures/output_files/svg/figure_{name.replace(' ', '_')}.svg")
        plt.savefig(f"./figures/output_files/png/figure_{name.replace(' ', '_')}.png")

def plot_rmse_values(methods, noise_level, rmse_val):
    plt.figure()
    for i, name in enumerate(methods): 
        # remove reference datum, ow it will skew the graph
        # this is a terrible implementation yet I do not know a better way
        if name == 'Canny Detection':
            plt.plot(noise_level[1:], rmse_val[i, 1:], '-o', linewidth=2, label=methods[i])
        else:
            plt.plot(noise_level, rmse_val[i, :], '-o', linewidth=2, label=methods[i])

    plt.title("RMSE Performance of Various Edge Detection Techniques", fontname='CMU Serif', fontsize=14)
    plt.xlabel('Gaussian Noise Variance', fontname='CMU Serif', fontsize=12)
    plt.ylabel('RMSE', fontname='CMU Serif', fontsize=12)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig("./figures/graphs/svg/rmse_figure.svg")
    plt.savefig("./figures/graphs/png/rmse_figure.png")
 
def generate_thres_imgs(): 
    # finally, plotting canny images at different threshold values
    thresholds = [0.1, 0.5, 1, 1.5]

    thres_figures, thres_arr = plt.subplots(2, 2)
    plt.suptitle(f"Threshold Changes in Canny Filter", fontname='CMU Serif', fontsize=14)
    thres_axes = thres_arr.flatten()

    for k, thres_val, in enumerate(thresholds):
        thres_img = feature.canny(img, high_threshold=thres_val)
        thres_axes[k].imshow(thres_img, cmap='gray')
        thres_axes[k].set_title(f"Threshold = {thres_val}", fontname='CMU Serif', fontsize=12)

    plt.tight_layout()
    plt.savefig("./figures/graphs/svg/various_thresholds.svg")



if __name__ == "__main__":

    # grayscale the image
    # required in order to calculate intensities of edges 
    # certain edges may show up in a single channel but not the other
    # hence the importance to combine them into a single channel for proccessing
    img = color.rgb2gray(io.imread('lena.jpg'))
    
    # the canny feature with sigma = 1 and threshold = 0.1 is the control, rmse is compared to this
    canny_control = feature.canny(img, sigma=1.0, high_threshold=0.1)
    
    noise_level = [0, 0.01, 0.05, 0.1, 0.5, 1]
    methods = ['Sobel', 'Prewitt', 'Laplacian of Gaussian', 'Canny Detection']
    rmse_val = np.zeros((len(methods), len(noise_level)))

    make_directory_structure()
    generate_edge_filter_imgs(img, canny_control, noise_level, methods)
    plot_rmse_values(methods, noise_level, rmse_val)
    generate_thres_imgs()