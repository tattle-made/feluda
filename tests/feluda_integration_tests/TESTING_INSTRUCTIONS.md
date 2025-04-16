# Feluda Testing Instructions

## Prerequisites
Python 3.8 or higher, pip, git

## Setup Instructions
### 1. Clone the Repository (if not already done)

```bash
git clone https://github.com/tattle-made/feluda.git
cd feluda
```
### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -e .
pip install pytest
```

Will install feluda in development mode along with its dependencies

## Running the Tests
### Running All Tests

To run all tests in the project:

```bash
python -m pytest
```

### Running Specific Integration Tests

To run only the integration tests:

```bash
python -m pytest tests/feluda_integration_tests/
```

### Running the Video Vector Representation Test Specifically

To run only the video vector representation integration test:

```bash
python -m pytest tests/feluda_integration_tests/test_02_feluda_and_vid_vec_rep_clip.py
## python -m pytest c:\Users\Lenovo\Downloads\feluda_C4GT\feluda\tests\feluda_integration_tests\test_02_feluda_and_vid_vec_rep_clip.py -v
```

## Test Structure

The test suite includes the following test methods:

- `test_video_vector_generation`: Tests the end to end process of creating a video object and generating vectors
- `test_invalid_video_url`: Tests error handling for invalid URLs
- `test_operator_configuration`: Verifies that the operator is properly configured
- `test_video_vector_consistency`: Ensures that generating vectors twice from the same video gives consistent results
