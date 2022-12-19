# HealthStreaming

## Streaming Data

### 개념
- 스트리밍 데이터는 연속적으로 전송되는 작은 크기의 데이터 레코드
- 모바일이나 웹 애플리케이션을 사용하는 고객이 생성하는 로그 파일이나 소셜 네트워크 정보, 주식 거래소, 전자상거래 구매 등 다양한 데이터를 포함
- 데이터가 지속해서 생성되기 때문에 모든 데이터에 대해 접근하지 않고, 스트리밍 처리 기술을 이용하여 점진적으로 처리 
- 스트리밍 데이터에 대해 상관관계 도출, 카운팅, 필터링, 샘플링 등을 처리하는 다양한 스트리밍 알고리즘이 연구됨

### Object
- 트위터 스트리밍 데이터의 빈도수를 알고리즘을 통해 추정하여 오차율을 분석하고자 한다.
- Apache Kafka 플랫폼, Count-min Sketch Algorithm

## Method
### Kafka
- 분산 환경에서 스트리밍 데이터를 지원하는 플랫폼
- 기존 분산 환경에는 여러 DB, application 등이 hadoop, search engine, monitoring과 같이 다양한 기능에 end-to-end 방식으로 연결 
- 즉, 각기 다른 데이터 파이프라인으로 연결된 복잡한 구조이며, 데이터 연동과 확장을 어렵게 만듬
- kafka는 파이프라인을 하나로 통일시켜 손쉽게 확장. 특히, 스트리밍 데이터를 지원하는 만큼 통신 손실을 최소화시키고자 message queue (MQ) 시스템을 사용
- MQ는 producer와 consumer 사이에 통신을 담당 
- Producer는 통신 이벤트의 발행 주체로, 통신을 요청
- 이 요청은 consumer에 바로 가지 않고 MQ를 거치게 됨
- MQ는 이 이벤트를 가지고 있다가, consumer에게 보냄 
- 통신 손실이 발생할 상황에도 MQ에 저장하고 있기 때문에 나중에 처리할 수 있다는 장점이 있다.

### Count-min Sketch
<img width="1188" alt="image" src="https://user-images.githubusercontent.com/80090973/208362313-6729f939-07b4-4ef3-b2f0-6160ac823530.png">
- 스트리밍 데이터에서 빈도수 추정을 위한 확률적 자료구조
- 전체 데이터의 정확한 빈도수를 계산하기 위해서는 유일한 원소 개수에 비례하는 메모리 공간이 요구
- Count-min Sketch는 유일한 원소의 개수보다 적은 메모리 공간과 해시 함수(Hash function)를 통해 빈도수를 추정
- Count-min sketch는 확률적 자료 구조로써 이를 통해 얻어지는 빈도수는 실제 값이 아닌 근삿값이다.

## Dataset : COVID-19 Twitter Streaming Dataset
- 트위터에서 제공하는 COVID-19 스트리밍 데이터 셋을 사용 
- 월간마다 COVID-19 해시태그를 가지고 있는 트윗이라 불리는 데이터 아이디를 수집하여 제공
- 트위터처럼 대규모 분산 시스템에서는 작고 유니크한 아이디가 필요하기 때문에 snowflake라는 아이디 생성기를 사용
- snowflake는 시계열을 기반으로 유니크한 아이디를 생성
- snowflake는 분산 환경에서 유니크한 아이디를 가지기 위해, timestamp, instance (worker), sequence 번호를 조합
- timestamp는 unixtime도 같이 사용하기 때문에, unixtime만 알고 있다면 손쉽게 시계열 정보로 복원이 가능

## Experiment
### Setting
- 9000만 여개의 트위터 스트리밍 데이터를 Kafka-python 패키지로 처리
- COVID-19 데이터 셋의 요일 빈도수를 추정하기 위해 count-min sketch 알고리즘을 적용
- Count-min sketch의 depth를 데이터 셋의 라벨인 7개보다 작게 설정하여 적은 메모리를 사용하더라도 알고리즘이 정확성을 유지하는지 확인해 보고자 함 
- depth를 5개로 설정
- 데이터 셋이 가지고 있는 원래의 빈도수와 count-min sketch를 적용했을 때 빈도수의 오차를 비교하는 실험을 진행
- 7 X 5 사이즈의 hash table이 생성

### 과정
- Kafka-python을 이용하여 약 9천만 개의 row 데이터를 읽어드림
- Producer는 데이터를 topic을 지정하여 통신 메시지를 보냄
- Consumer는 받은 row 데이터를 한 줄씩 읽음 
- Snowflake 형식으로 구성된 트위터 아이디 데이터를 시계열 데이터로 복원
- 복원된 정보에서 요일을 추출하고, count-min sketch를 적용하여 요일별 빈도수를 카운트

## Result

<img width="801" alt="image" src="https://user-images.githubusercontent.com/80090973/208369118-f7402a65-ab27-4487-b113-9a8fe223b620.png">

<img width="748" alt="image" src="https://user-images.githubusercontent.com/80090973/208368592-db8f45bf-54f9-4c39-8e2c-938e5fb8448a.png">

- 원래 데이터셋의 빈도수와 알고리즘을 통해 추정한 빈도수 근사치
- 두 표의 빈도수를 비교했을 때, 월요일부터 토요일까지는 원래 데이터 셋의 빈도수와 동일
- 일요일은 기존 데이터 셋의 빈도수와 큰 차이가 나는 것을 확인
- 이번 프로젝트에서 기존 라벨 (7개)보다 작은 depth를 설정하였기 때문에 발생한 결과라고 추측
- 더 큰 depth를 설정하여 많은 hash function을 생성한다면 일요일도 정확한 빈도수를 추정할 수 있을 것이라 예상
