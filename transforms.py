from random import sample


def docTransforms(text, type=None, frac=0.3):
    # TODO add 'synonym_replace', 'common_misspellings'
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
    else:
        return text


def imageTransforms(image, type=None, frac=0.1):
    from PIL import Image
    # PIL can convert across formats
    if type == 'crop':
        bounds = list(image.getbbox())
        sides = sample(range(0, 4), 2)
        bounds[sides[0]] = int(bounds[sides[0]]*frac)
        bounds[sides[1]] = int(bounds[sides[1]]*frac)

        image = image.crop(tuple(bounds))
        
        return image
    elif type == 'rotate': 
        angle = sample(range(30, 330, 30), 1)[0]
        image = image.rotate(angle)
        
        return image
    elif type == 'noise':
        # use Image.filter
        return image
    elif type == 'b/w':
        return image
    elif type == 'saturation':
        return image
    elif type == 'add_noise_to_embedding':
        return image
    else:
        return image
