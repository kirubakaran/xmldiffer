#!/bin/bash

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    pip install pre-commit
fi

# Install the hooks
pre-commit install 