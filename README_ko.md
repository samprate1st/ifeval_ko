# IFEval-Ko (한국어 지시 따르기 평가)

[IFEval](https://arxiv.org/abs/2311.07911) (지시 따르기 평가)의 한국어 적응 버전입니다. [allganize/IFEval-Ko](https://huggingface.co/datasets/allganize/IFEval-Ko) 데이터셋과 [josejg/instruction_following_eval](https://github.com/josejg/instruction_following_eval) pip 설치 가능한 포크를 기반으로 합니다.

## 영어 IFEval에서의 변경사항

- **한국어 데이터셋**: GPT-4o를 사용해 한국어로 번역된 프롬프트 (allganize/IFEval-Ko에서 제공)
- **단위 변환**: 갤런 → 리터, 피트 → 미터, 달러 → 원
- **제목 형식**: `<<title>>` → `<<제목>>` 스타일로 업데이트
- **영어 WORD_LIST 폴백 제거**: 키워드, 금지된 단어, 끝 문구는 데이터셋 kwargs에서 제공되어야 함 (자동 영어 단어 생성 없음)
- **한국어 인식 텍스트 매칭**: 한국어는 영어처럼 단어 경계가 없으므로 키워드/금지된 단어 확인을 위해 부분 문자열 매칭 사용
- **패키지 이름 변경**: `instruction_following_eval` → `ifeval_ko`

## 설치

### 빠른 설치 (권장)

클론 없이 GitHub에서 직접 설치:

```shell
pip install git+https://github.com/samprate1st/ifeval_ko.git
```

또는 특정 브랜치 설치:

```shell
pip install git+https://github.com/samprate1st/ifeval_ko.git@branch_name
```

### requirements.txt를 이용한 설치

`requirements.txt` 파일에 패키지 추가:

```
git+https://github.com/samprate1st/ifeval_ko.git
```

또는 특정 브랜치 지정:

```
git+https://github.com/samprate1st/ifeval_ko.git@branch_name
```

설치:

```shell
pip install -r requirements.txt
```

### 수동 설치 (대안)

리포지토리를 클론 후 로컬에서 설치:

```shell
git clone https://github.com/samprate1st/ifeval_ko.git
cd ifeval_ko
pip install .
```

## 한국어 데이터셋 다운로드

설치 후 HuggingFace에서 한국어 데이터셋을 다운로드합니다:

```shell
ifeval-ko-download
```

또는 사용자 지정 출력 경로로:

```shell
ifeval-ko-download --output /path/to/output.jsonl
```

또는 프로그래밍 방식으로:

```python
from ifeval_ko.download_data import download_and_convert
download_and_convert()
```

## 한국어 데이터셋 업데이트

HuggingFace의 최신 버전으로 데이터셋을 업데이트 (자동 백업 포함):

```shell
ifeval-ko-update
```

또는 사용자 지정 출력 경로로:

```shell
ifeval-ko-update --output /path/to/output.jsonl
```

또는 프로그래밍 방식으로:

```python
from ifeval_ko.update_data import update_dataset
update_dataset()
```

## IFEval-Ko 실행

### 프로그래밍 방식 평가

```python
from ifeval_ko import get_examples, evaluate_instruction_following

# 한국어 예제 로드 (먼저 다운로드 필요)
examples = get_examples()

# 모델에서 응답 생성
for example in examples:
    example['response'] = model.generate(example['prompt'])

# 평가
metrics = evaluate_instruction_following(examples)
print(metrics)
```

예제 데이터 형식:

```python
{
    'key': 1001,
    'instruction_id_list': ['punctuation:no_comma'],
    'prompt': '일본 여행을 계획하고 있는데, 셰익스피어 스타일로 ...',
    'kwargs': [{}],
}
```

### 데이터셋 분석

제공된 스크립트를 사용하여 전체 한국어 데이터셋 분석:

```shell
# 완전한 분석 실행 및 통계 생성
python main.py

# 사용자 지정 데이터셋 파일 분석
python main.py --data-path /path/to/input_data.jsonl
```

다음을 포함하는 `dataset_statistics.json` 생성:
- 총 예제 수
- 지시사항 빈도 분포
- 일반적인 지시사항 조합
- 프롬프트 길이 통계 (최소, 최대, 평균)

### runme.sh를 사용한 빠른 시작

완전한 워크플로우 (데이터셋 다운로드/업데이트 및 분석):

```shell
bash runme.sh
```

이 스크립트는 다음을 수행합니다:
1. 필요하면 패키지 설치
2. 한국어 데이터셋 다운로드 또는 업데이트
3. 데이터셋 분석 실행
4. 통계 표시 및 결과를 `dataset_statistics.json`에 저장

## 테스트

```shell
python test/instructions_test.py
python test/instructions_util_test.py
```

## 크레딧

- 원본 IFEval: [Google Research](https://github.com/google-research/google-research/tree/master/instruction_following_eval)
- 한국어 데이셋: [allganize/IFEval-Ko](https://huggingface.co/datasets/allganize/IFEval-Ko)
- Pip 설치 가능한 포크: [josejg/instruction_following_eval](https://github.com/josejg/instruction_following_eval)
