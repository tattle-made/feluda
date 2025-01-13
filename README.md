# Feluda

A configurable engine for analysing multi-lingual and multi-modal content.


While flexible, we built it to analyse data collected from social media - images,text and video. This forms the core of our search, clustering and analysis services. Since different use cases might require different search capabilities with different trade offs, Feluda lets you specify which building blocks you want to use for the purpose and spins an engine with a corresponding configuration.

## Example Uses
- [Khoj](https://tattle.co.in/products/khoj/) : An Reverse Image search engine to find fact check articles
- [Crowdsourcing Aid : A Case Study of the Information Chaos During India's Second Covid-19 Wave](https://tattle.co.in/articles/covid-whatsapp-public-groups/) : Analysis of whatsapp messages related to relief work collected from public whatsapp group during the second wave of Covid-19 in India.

## Understanding Operators in Feluda
When we built Feluda, we were focusing on the unique challenges of social media data that was found in India. We needed to process data in various modalities (text, audio, video, images, hybrid) and various languages. There would often be very different technologies that needed to be evaluated for each. So we built Feluda around a concept of operators. You can think of operators as plugins that you can mix and match to perform different analyses on your data (see Features section below). When you start feluda, you [configure which operators](https://github.com/tattle-made/feluda/tree/master/src/api/core/operators) you want to use and then feluda loads it. While in its current iteration Feluda comes with certain operators in its source code, the operators are defined in a way that anyone can create their own operators and use it with Feluda. Operators are easy to swap in and out. Not only does this allow you to try out various different analysis techniques, it also means you aren't tied to any one implementation for an operation. Some use cases for operators that we've tried out are following :
1. If someone wants to run image data aggregation on a budget, instead of using an operator that uses a heavy machine learning model, they can use an operator that uses hashing instead.
2. If someone wants to extract text from images and don't want to use a google product, they could use an operator that uses openCV as opposed to google cloud vision API.

## Features Enabled
- Support for Vector based embeddings using ResNet models and Sentence Transformers
- Support for hash based search using pHash
- Text extraction from images and indexing into the engine
- Entity extraction from text and images and indexing into the engine



## Contributing
You can find instructions on contributing on the [Wiki](https://github.com/tattle-made/feluda/wiki)

#### Documentation for Setting up Feluda for Local Development - [Link to the Wiki](https://github.com/tattle-made/feluda/wiki/Setup-Feluda-Locally-for-Development)
