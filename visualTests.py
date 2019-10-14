import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from transforms import imageTransforms
from search import ImageSearch
from analyzer import img2vec, image_from_url

# maximizing plot windows: https://stackoverflow.com/a/22418354/3543635
plt.switch_backend('TkAgg')

def imageTesting():
    db_type = 'testing'
    images = [(1, 'https://picsum.photos/id/448/1024/768')]
    imageSearch = ImageSearch(db_type, images)
    imageSearch.thresh = 20  # to pass the following tests

    assert(len(imageSearch.vecs) > 0)

    transforms = ['crop', 'rotate', 'invert', 'mirror', 'BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SMOOTH', 'SMOOTH_MORE', 'SHARPEN', 'GaussianBlur', 'UnsharpMask', 'MedianFilter', 'MinFilter', 'MaxFilter', 'ModeFilter']

    for i, image in images:
        image = image_from_url(image)['image']

        for tf in transforms:
            imageTransformed = imageTransforms(image, type=tf)
            imageTransformedVec = img2vec(imageTransformed, type='image')

            ret = imageSearch.search(imageTransformedVec)            
            print(f'{i}=>{ret[0]}, {tf}: {ret[1]}')
            
            if ret[0] is not None:
                ret_image = image_from_url(images[ret[0]-1][1])['image']

            f, ax = plt.subplots(nrows=3, ncols=1)

            ax[0].imshow(image)
            ax[0].set_title('original image')
            ax[1].imshow(imageTransformed)
            ax[1].set_title(f'{tf} image')
            if ret[0] is not None:
                ax[2].imshow(ret_image)
                ax[2].set_title(f'similar image: {ret[1]:.2f}')
            
            mgr = plt.get_current_fig_manager()
            mgr.window.state('zoomed')
            plt.show()

if __name__ == "__main__":
    imageTesting()