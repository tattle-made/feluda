# Dimension Reduction Operator

## Description

The `Dimension Reduction` operator reduces the dimensionality of high-dimensional embeddings using t-SNE and UMAP algorithms. It supports reducing embeddings to 2D or 3D for visualization and analysis purposes while preserving the most important structural information.

## Model Information

- **t-SNE**: t-Distributed Stochastic Neighbor Embedding for non-linear dimensionality reduction
- **UMAP**: Uniform Manifold Approximation and Projection for scalable dimension reduction
- **Vector Size**: Configurable (typically 2-3 dimensions for visualization)
- **Usage**: Reduces high-dimensional embeddings to lower dimensions for visualization, clustering, and analysis

## Dependencies

- scikit-learn >= 1.6.1
- numpy >= 1.26,<2.2.0
- umap-learn >= 0.5.0

## How to Run the Tests

1. Ensure that you are in the root directory of the `feluda` project.
2. Install dependencies (in your virtual environment):

   ```bash
   uv pip install "./operators/dimension_reduction"
   uv pip install "feluda[dev]"
   ```

3. Run the tests:

   ```bash
   pytest operators/dimension_reduction/test.py
   ```

## Usage

```python
from operators.dimension_reduction.dimension_reduction import DimensionReduction

# Initialize with t-SNE
operator = DimensionReduction("tsne", {
    "n_components": 2,
    "perplexity": 2,
    "random_state": 42
})

# Prepare input data
input_data = [
    {"payload": "sample_1", "embedding": [1.0, 2.0, 3.0, 4.0, 5.0]},
    {"payload": "sample_2", "embedding": [2.0, 3.0, 4.0, 5.0, 6.0]},
    {"payload": "sample_3", "embedding": [3.0, 4.0, 5.0, 6.0, 7.0]}
]


# Run dimension reduction
result = operator.run(input_data)

# Access results
for item in result:
    print(f"Payload: {item['payload']}")
    print(f"Reduced embedding: {item['reduced_embedding']}")
```
