# IFEval-Ko (Korean Instruction Following Eval)

Korean adaptation of [IFEval](https://arxiv.org/abs/2311.07911) (Instruction Following Evaluation), based on the [allganize/IFEval-Ko](https://huggingface.co/datasets/allganize/IFEval-Ko) dataset and the [josejg/instruction_following_eval](https://github.com/josejg/instruction_following_eval) pip-installable fork.

## Changes from English IFEval

- **Korean dataset**: Prompts translated to Korean using GPT-4o (from allganize/IFEval-Ko)
- **Unit conversions**: gallons to liters, feet to meters, dollars to won
- **Title format**: `<<title>>` updated to `<<제목>>` style
- **Removed English WORD_LIST fallbacks**: Keywords, forbidden words, and end phrases must be provided in the dataset kwargs (no automatic English word generation)
- **Korean-aware text matching**: Uses substring matching instead of word boundary matching for keyword/forbidden word checks (since Korean doesn't have word boundaries like English)
- **Package renamed**: from `instruction_following_eval` to `ifeval_ko`

## Install

### Quick Install (Recommended)

Install directly from GitHub without cloning:

```shell
pip install git+https://github.com/samprate1st/ifeval_ko.git
```

Or install a specific branch:

```shell
pip install git+https://github.com/samprate1st/ifeval_ko.git@branch_name
```

### Using requirements.txt

Add the package to your `requirements.txt`:

```
git+https://github.com/samprate1st/ifeval_ko.git
```

Or with a specific branch:

```
git+https://github.com/samprate1st/ifeval_ko.git@branch_name
```

Then install:

```shell
pip install -r requirements.txt
```

### Manual Installation (Alternative)

Clone the repository and install locally:

```shell
git clone https://github.com/samprate1st/ifeval_ko.git
cd ifeval_ko
pip install .
```

## Download Korean Dataset

After installing, download the Korean dataset from HuggingFace:

```shell
ifeval-ko-download
```

Or with a custom output path:

```shell
ifeval-ko-download --output /path/to/output.jsonl
```

Or programmatically:

```python
from ifeval_ko.download_data import download_and_convert
download_and_convert()
```

## Update Korean Dataset

To update the dataset to the latest version from HuggingFace (with automatic backup):

```shell
ifeval-ko-update
```

Or with a custom output path:

```shell
ifeval-ko-update --output /path/to/output.jsonl
```

Or programmatically:

```python
from ifeval_ko.update_data import update_dataset
update_dataset()
```

## Running IFEval-Ko

### Programmatic Evaluation

```python
from ifeval_ko import get_examples, evaluate_instruction_following

# Load Korean examples (must download first)
examples = get_examples()

# Generate responses from your model
for example in examples:
    example['response'] = model.generate(example['prompt'])

# Evaluate
metrics = evaluate_instruction_following(examples)
print(metrics)
```

Example data format:

```python
{
    'key': 1001,
    'instruction_id_list': ['punctuation:no_comma'],
    'prompt': '일본 여행을 계획하고 있는데, 셰익스피어 스타일로 ...',
    'kwargs': [{}],
}
```

### Dataset Analysis

Analyze the entire Korean dataset using the provided script:

```shell
# Run complete analysis and generate statistics
python main.py

# Analyze a custom dataset file
python main.py --data-path /path/to/input_data.jsonl
```

This generates `dataset_statistics.json` with:
- Total number of examples
- Instruction frequency distribution
- Common instruction combinations
- Prompt length statistics (min, max, average)

### Quick Start with runme.sh

For a complete workflow (download/update dataset and analyze):

```shell
bash runme.sh
```

This script will:
1. Install the package if needed
2. Download or update the Korean dataset
3. Run dataset analysis
4. Display statistics and save results to `dataset_statistics.json`

## Tests

```shell
python test/instructions_test.py
python test/instructions_util_test.py
```

## Credits

- Original IFEval: [Google Research](https://github.com/google-research/google-research/tree/master/instruction_following_eval)
- Korean Dataset: [allganize/IFEval-Ko](https://huggingface.co/datasets/allganize/IFEval-Ko)
- Pip-installable fork: [josejg/instruction_following_eval](https://github.com/josejg/instruction_following_eval)
