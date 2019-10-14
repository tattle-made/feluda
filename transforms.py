from random import sample, uniform


def docTransforms(text, type=None, frac=0.3):
    # https://forums.fast.ai/t/nlp-any-libraries-dictionaries-out-there-for-fixing-common-spelling-errors/16411/8
    # TODO add 'synonym_replace', 'common_misspellings'
    # a good language model should be able to catch common transformations easily
    # what is that language model for each language?
    if type == 'drop_char':
        l = len(text)
        idx = sample(range(0, l), int(l*frac))

        text = list(text)
        for i, j in enumerate(idx):
            text[j] = ''
        text = ''.join(text)

        return text
    elif type == 'drop_word':
        text = text.split(' ')
        l = len(text)
        idx = sample(range(0, l), int(l*frac))

        for i, j in enumerate(idx):
            text[j] = ''
        text = ' '.join(text)

        return text
    elif type == 'synonym_replace':
        # from ntlk.corpus import wordnet
        # wordnet.synsets(word)
        pass
    elif type == 'common_mispellings':
        # char-rnns for catching misplellings
        # regex 
        pass
    else:
        return text


def imageTransforms(image, type=None, param=0.1):
    """get transformed image
    
    Arguments:
        image {PIL.Image|str} -- input image or url
    
    Keyword Arguments:
        type {str} -- whether image is a url or PIL.Image (default: {None})
        param {float} -- parameter for controlling different transforms (default: {0.1})
    
    Returns:
        [type] -- [description]
    """
    from PIL import Image, ImageFilter, ImageOps, ImageChops
    from torchvision.transforms import Grayscale, ColorJitter
    from random import uniform
    # PIL can convert across formats
    # PIL is a good library brent 11/10
    # https://pillow.readthedocs.io/en/3.3.x/reference/Image.html

    # All ImageFilters: ['BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SMOOTH', 'SMOOTH_MORE', 'SHARPEN', 'GaussianBlur', 'UnsharpMask', 'RankFilter', 'MedianFilter', 'MinFilter', 'MaxFilter', 'ModeFilter']
    imagefilters = ['BLUR', 'CONTOUR', 'DETAIL', 'EDGE_ENHANCE', 'EDGE_ENHANCE', 'EDGE_ENHANCE_MORE', 'EMBOSS', 'FIND_EDGES', 'SMOOTH', 'SMOOTH_MORE', 'SHARPEN', 'GaussianBlur', 'UnsharpMask', 'RankFilter', 'MedianFilter', 'MinFilter', 'MaxFilter', 'ModeFilter']

    # imageops as preprocessing: autocontrast, colorize, equalize
    imageops = ['invert', 'mirror', 'posterize', 'solarize']

    # ImageEnhance?

    # torchvision.transforms : https://pytorch.org/docs/stable/torchvision/transforms.html
    # TODO: try other torchvision transforms
    torchtransforms = ['ColorJitter', 'Grayscale']


    if type == 'crop':
        bounds = list(image.getbbox())
        # sides = sample(range(2, 4), 2)

        bounds[2] = int(bounds[2]*(1-(uniform(0, param))))
        bounds[3] = int(bounds[3]*(1-(uniform(0, param))))

        image = image.crop(tuple(bounds))
        
        return image
    elif type == 'rotate': 
        angle = sample(range(30, 330, 30), 1)[0]
        image = image.rotate(angle)
        
        return image
    elif type in imagefilters:
        image = image.filter(eval(f'ImageFilter.{type}'))
        return image
    elif type == 'invert':
        image = ImageOps.invert(image)
        return image
    elif type == 'grayscale':
        image = Grayscale(num_output_channels=3)(image)
        return image
    elif type == 'mirror':
        image = ImageOps.mirror(image)
        return image
    elif type == 'color_jitter':
        # TODO: convert return to PIL.image
        image = ColorJitter()(image)
        image = Image.fromarray(image)
    else:
        return image
