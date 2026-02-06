#!/bin/bash

# Script to process the entire Korean IFEval dataset
# This script downloads the dataset and runs analysis

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Korean IFEval Dataset Processing${NC}"
echo -e "${BLUE}================================================${NC}"
echo

# Check if package is installed
if ! python -c "import ifeval_ko" 2>/dev/null; then
    echo -e "${YELLOW}Installing ifeval_ko package...${NC}"
    pip install -e .
    echo
fi

# Download or update dataset
echo -e "${BLUE}Step 1: Downloading/Updating Korean IFEval Dataset${NC}"
echo -e "${YELLOW}Running: ifeval-ko-update${NC}"
ifeval-ko-update
echo -e "${GREEN}✓ Dataset ready${NC}"
echo

# Run main analysis
echo -e "${BLUE}Step 2: Analyzing Dataset${NC}"
echo -e "${YELLOW}Running: python main.py${NC}"
python main.py
echo -e "${GREEN}✓ Analysis complete${NC}"
echo

# Check output files
echo -e "${BLUE}Step 3: Output Summary${NC}"
if [ -f "dataset_statistics.json" ]; then
    echo -e "${GREEN}✓ Statistics file created: dataset_statistics.json${NC}"
    echo
    echo "Dataset statistics:"
    python -m json.tool dataset_statistics.json | head -30
else
    echo -e "${RED}✗ Statistics file not found${NC}"
fi

echo
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}Processing complete!${NC}"
echo -e "${BLUE}================================================${NC}"
