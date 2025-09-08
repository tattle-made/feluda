# Feluda
[![DPG Badge](https://img.shields.io/badge/Verified-DPG%20(Since%20%202023)-3333AB?logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iMzEiIGhlaWdodD0iMzMiIHZpZXdCb3g9IjAgMCAzMSAzMyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE0LjIwMDggMjEuMzY3OEwxMC4xNzM2IDE4LjAxMjRMMTEuNTIxOSAxNi40MDAzTDEzLjk5MjggMTguNDU5TDE5LjYyNjkgMTIuMjExMUwyMS4xOTA5IDEzLjYxNkwxNC4yMDA4IDIxLjM2NzhaTTI0LjYyNDEgOS4zNTEyN0wyNC44MDcxIDMuMDcyOTdMMTguODgxIDUuMTg2NjJMMTUuMzMxNCAtMi4zMzA4MmUtMDVMMTEuNzgyMSA1LjE4NjYyTDUuODU2MDEgMy4wNzI5N0w2LjAzOTA2IDkuMzUxMjdMMCAxMS4xMTc3TDMuODQ1MjEgMTYuMDg5NUwwIDIxLjA2MTJMNi4wMzkwNiAyMi44Mjc3TDUuODU2MDEgMjkuMTA2TDExLjc4MjEgMjYuOTkyM0wxNS4zMzE0IDMyLjE3OUwxOC44ODEgMjYuOTkyM0wyNC44MDcxIDI5LjEwNkwyNC42MjQxIDIyLjgyNzdMMzAuNjYzMSAyMS4wNjEyTDI2LjgxNzYgMTYuMDg5NUwzMC42NjMxIDExLjExNzdMMjQuNjI0MSA5LjM1MTI3WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+Cg==)](https://digitalpublicgoods.net/r/feluda)

A configurable engine for analysing multi-lingual and multi-modal content.

While flexible, we built it to analyse data collected from social media - images, text, and video. This forms the core of our search, clustering, and analysis services. Since different use cases might require different search capabilities with different trade-offs, Feluda lets you specify which building blocks you want to use for the purpose and spins an engine with a corresponding configuration.

## Example Uses
- [Khoj](https://tattle.co.in/products/khoj/) : A Reverse Image search engine to find fact-check articles
- [Crowdsourcing Aid : A Case Study of the Information Chaos During India's Second Covid-19 Wave](https://tattle.co.in/articles/covid-whatsapp-public-groups/) : Analysis of whatsapp messages related to relief work collected from public WhatsApp groups during the second wave of Covid-19 in India.

## Understanding Operators in Feluda

When we built Feluda, we were focusing on the unique challenges of social media data in India. We needed to process data in various modalities (text, audio, video, images, hybrid) and various languages. There would often be very different technologies that needed to be evaluated for each. So we built Feluda around a concept of operators. You can think of operators as plugins that you can mix and match to perform different analyses on your data (see Features section below). When you start feluda, you [configure which operators](https://github.com/tattle-made/feluda/tree/main/operators) you want to use and then feluda loads it. While in its current iteration Feluda comes with certain operators in its source code, the operators are defined in a way that anyone can create their own operators and use it with Feluda. Operators are easy to swap in and out. Not only does this allow you to try out various analysis techniques, it also means you aren't tied to any one implementation for an operation. Some use cases for operators that we've tried out are following :

1. If someone wants to run image data aggregation on a budget, instead of using an operator that uses a heavy machine learning model, they can use an operator that uses hashing instead.
2. If someone wants to extract text from images and don't want to use a google product, they could use an operator that uses OpenCV instead of the Google Cloud Vision API.

## Features Enabled
- Support for Vector-based embeddings using ResNet models and Sentence Transformers.
- Support for hash-based search using pHash.
- Text extraction from images and indexing into the engine.
- Entity extraction from text and images and indexing into the engine.

## Basic Usage

Feluda can be used as a Python library to process and analyze data using its modular operators. Below is a quick overview of how to install Feluda, configure it, and use it in your Python projects.

### Prerequisites

Before you begin, ensure that the following system dependencies are installed:

- Python version 3.10 or higher
- optionally we recommend to use `uv` for python pacakges and project managment. Install `uv` by following its [official installation guide](https://docs.astral.sh/uv/).

### Installation

You can install `feluda` using
```bash
pip install feluda
```

Each operator also has to be installed seperately. Link to a list of [published](https://pypi.org/user/tattle/) feluda operators. For instance, you can install the `feluda-vid-vec-rep-clip` operator like
```sh
pip install feluda-vid-vec-rep-clip
```

### Configuration

Feluda uses a configuration file (`.yml`) to define the operators and their parameters. This allows you to customize your workflow without modifying the code. You will have to create this `.yml` file manually.

Here’s an example configuration file (`config.yml`):

```yaml
operators :
  label : "Operators"
  parameters :
    - name : "Video Vector Representation"
      type : "vid_vec_rep"
      parameters: {}
    - name : "Image Vector Representation"
      type : "image_vec_rep"
      parameters: {}
```

- **`operators`**: A list of operators to be used.
- **`name`**: The name of the operator.
- **`parameters`**: Any other Operator specific parameters.

### Code Example

Here’s a simple example to demonstrate how to use Feluda:

```python
from feluda import Feluda

config_path = "/path/to/config.yml"

# Initialize Feluda with the configuration file
feluda = Feluda(config_path)
# Set up Feluda and its operators
feluda.setup()

# Access an operator and run a task
operator = feluda.operators.get()["vid_vec_rep"]
result = operator.run("path/to/example.mp4")
print(result)
```

For more details, refer to the [Feluda Wiki](https://github.com/tattle-made/feluda/wiki).

## Contributing
You can find instructions on contributing on the [Wiki](https://github.com/tattle-made/feluda/wiki)

#### Documentation for Setting up Feluda for Local Development - [Link to the Wiki](https://github.com/tattle-made/feluda/wiki/Setup-Feluda-Locally-for-Development)
