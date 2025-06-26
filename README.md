# Prompt2SQL
User Prompt → LLM-based SQL Generation → Database Execution → Structured Result Output

자연어 프롬프트를 SQL 쿼리로 변환하고 실행하여 결과를 출력하는 자동화 파이프라인입니다.  

LLM 기반의 자연어 처리 기능과 SQL 실행 모듈을 결합하여, 기술적 배경이 없는 사용자도 데이터베이스 질의를 쉽게 수행할 수 있도록 설계되었습니다.  

![image](https://github.com/user-attachments/assets/786d82c8-83c9-446e-a72c-4ef971b32253)

(현재 unittest와 unittest.mock을 이용한 테스트 코드를 개발 중입니다.)



## 주요 기능

- 자연어 → SQL 쿼리 변환 (OpenAI API 활용)
- PostgreSQL 및 SQLite 등의 데이터베이스에 쿼리 실행
- 결과를 표 또는 JSON 형태로 출력
- 입력 정제 및 예외 처리 포함 (비정상 쿼리 차단)



## 설치 방법

`bash
git clone https://github.com/jade-pond/Prompt2SQL.git
cd Prompt2SQL
pip install -r requirements.txt
`



## 실행 예시

`bash
python nl_to_sql.py --prompt "월간 매출 상위 제품을 보여줘"
`


### 테스트 케이스
- 빈 질의 입력 처리  
- 세미콜론, 마크다운 제거 등 쿼리 정제  
- SELECT 외 문법 차단 (INSERT/DELETE 제한)  
- 파일 누락 예외 처리  
- 데이터 전처리 유효성 검증  
- API 호출 모킹 및 오류 응답 테스트  

---

## 프로젝트 구조

```bash
Prompt2SQL/
├── nl_to_sql.py                # 메인 애플리케이션
├── requirements.txt            # 의존성 패키지 목록 
└── README.md                   # 프로젝트 설명 파일

```


## 설정 옵션

- `--prompt`: 사용자 입력 프롬프트  
- `--dataset`: 분석 대상 Excel/CSV 파일 경로  
- `--db`: 사용할 DB 종류 선택 (예: sqlite, postgres)



---
이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.
