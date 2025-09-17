# Quick Start

This guide will help you get started with Feluda quickly.

## Basic Usage

### 1. Import and Initialize

```python
from feluda import Feluda

# Initialize Feluda
feluda = Feluda()
```

### 2. Using Operators

Feluda uses operators to process different types of content. Here's a simple example:

```python
from feluda.factory import ImageFactory
from feluda.operators import ImageVecRep

# Initialize the operator
operator = ImageVecRep()

# Load an image
image_obj = ImageFactory.make_from_url("https://example.com/image.jpg")

# Extract features
features = operator.run(image_obj)
print(f"Feature vector shape: {features.shape}")  # (512,)
print(f"Feature vector dtype: {features.dtype}")  # float16

# Cleanup
operator.cleanup()
```

## Next Steps

- Explore the [API documentation](api/feluda) for detailed information
- Check out the [examples](examples/README) for more complex use cases
- Learn about [contributing](contributing/) to the project
