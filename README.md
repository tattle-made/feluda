# Feluda
[![DPG Badge](https://img.shields.io/badge/Verified-DPG%20(Since%20%202023)-3333AB?logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iMzEiIGhlaWdodD0iMzMiIHZpZXdCb3g9IjAgMCAzMSAzMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE0LjIwMDggMjEuMzY3OEwxMC4xNzM2IDE4LjAxMjRMMTEuNTIxOSAxNi40MDAzTDEzLjk5MjggMTguNDU5TDE5LjYyNjkgMTIuMjExMUwyMS4xOTA5IDEzLjYxNkwxNC4yMDA4IDIxLjM2NzhaTTI0LjYyNDEgOS4zNTEyN0wyNC44MDcxIDMuMDcyOTdMMTguODgxIDUuMTg2NjJMMTUuMzMxNCAtMi4zMzA4MmUtMDVMMTEuNzgyMSA1LjE4NjYyTDUuODU2MDEgMy4wNzI5N0w2LjAzOTA2IDkuMzUxMjdMMCAxMS4xMTc3TDMuODQ1MjEgMTYuMDg5NUwwIDIxLjA2MTJMNi4wMzkwNiAyMi44Mjc3TDUuODU2MDEgMjkuMTA2TDExLjc4MjEgMjYuOTkyM0wxNS4zMzE0IDMyLjE3OUwxOC44ODEgMjYuOTkyM0wyNC44MDcxIDI5LjEwNkwyNC42MjQxIDIyLjgyNzdMMzAuNjYzMSAyMS4wNjEyTDI2LjgxNzYgMTYuMDg5NUwzMC42NjMxIDExLjExNzdMMjQuNjI0MSA5LjM1MTI3WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==)](https://digitalpublicgoods.net/r/feluda)

A configurable engine for analysing multi-lingual and multi-modal content.

While flexible, we built it to analyse data collected from social media - images, text, and video. This forms the core of our search, clustering, and analysis services. Since different use cases might require different search capabilities with different trade-offs, Feluda lets you specify which building blocks you want to use for the purpose and spins an engine with a corresponding configuration.

## Example Uses
- [Khoj](https://tattle.co.in/products/khoj/) : A Reverse Image search engine to find fact-check articles.
- [Crowdsourcing Aid: A Case Study of the Information Chaos During India's Second Covid-19 Wave](https://tattle.co.in/articles/covid-whatsapp-public-groups/) : Analysis of WhatsApp messages related to relief work collected from public WhatsApp groups during the second wave of Covid-19 in India.

## Understanding Operators in Feluda
When we built Feluda, we were focusing on the unique challenges of social media data that was found in India. We needed to process data in various modalities (text, audio, video, images, hybrid) and various languages. There would often be very different technologies that needed to be evaluated for each. So we built Feluda around a concept of operators. You can think of operators as plugins that you can mix and match to perform different analyses on your data (see Features section below). When you start Feluda, you [configure which operators](https://github.com/tattle-made/feluda/tree/master/src/api/core/operators) you want to use and then Feluda loads it. While in its current iteration Feluda comes with certain operators in its source code, the operators are defined in a way that anyone can create their own operators and use them with Feluda. Operators are easy to swap in and out. Not only does this allow you to try out various different analysis techniques, but it also means you aren't tied to any one implementation for an operation. Some use cases for operators that we've tried out are the following:
1. If someone wants to run image data aggregation on a budget, instead of using an operator that uses a heavy machine learning model, they can use an operator that uses hashing instead.
2. If someone wants to extract text from images and don't want to use a Google product, they could use an operator that uses OpenCV as opposed to Google Cloud Vision API.

## Features Enabled
- Support for Vector-based embeddings using ResNet models and Sentence Transformers.
- Support for hash-based search using pHash.
- Text extraction from images and indexing into the engine.
- Entity extraction from text and images and indexing into the engine.

---

## Basic Usage

Feluda can be used as a Python library to process and analyze data using its modular operators. This section provides a quick overview of how to install Feluda, configure it, and use it in your Python projects.

### Prerequisites

Before you begin, ensure that the following system dependencies are installed:

1. **Python**: Feluda requires Python 3.8 or higher. You can check your Python version using:
   ```bash
   python --version
   ```

2. **uv**: Feluda uses `uv` to manage and develop Python packages. Install `uv` by following its [official installation guide](https://docs.astral.sh/uv/).

3. **pip**: Ensure you have `pip` installed for managing Python packages. You can install or upgrade `pip` using:
   ```bash
   python -m ensurepip --upgrade
   ```

---

### Installation

1. Install the Feluda library:
   ```bash
   pip install feluda
   ```

2. Install operator packages from PyPI. For example:
   - To use the `vid_vec_rep_clip` operator:
     ```bash
     pip install feluda-vid-vec-clip
     ```
   - To use the `image_vec_rep_resnet` operator:
     ```bash
     pip install feluda-image-vec-resnet
     ```

---

### Configuration Overview

Feluda uses a configuration file to define the operators and their parameters. This allows you to customize your workflow without modifying the code.

Here’s an example configuration file (`config.yml`):

```yaml
operators:
  - name: vid_vec_rep_clip
    parameters: {}
      model_name: "ViT-B/32"
  - name: image_vec_rep_resnet
    parameters: {}
      model_name: "resnet50"
```

- **`operators`**: A list of operators to be used.
- **`name`**: The name of the operator.
- **`parameters`**: Operator-specific parameters.

---

### Python Code Example

Here’s a simple example to demonstrate how to use Feluda:

```python
from feluda import Feluda

# Path to the configuration file
config_path = "config.yml"

# Initialize Feluda with the configuration file
feluda = Feluda(config_path)

# Set up Feluda and its operators
feluda.setup()

# Access an operator and run a task
operator = feluda.operators.get()["vid_vec_rep_clip"]
result = operator.run("example.mp4")

print(result)
```

This example demonstrates how to initialize Feluda, set it up with a configuration file, and use an operator to process data.

---

For more details, refer to the [Feluda Wiki](https://github.com/tattle-made/feluda/wiki).

## Contributing
You can find instructions on contributing on the [Wiki](https://github.com/tattle-made/feluda/wiki)

#### Documentation for Setting up Feluda for Local Development - [Link to the Wiki](https://github.com/tattle-made/feluda/wiki/Setup-Feluda-Locally-for-Development)
