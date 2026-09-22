# Project Management Agent PoC

프로젝트 진행 상황을 분석하고 필요한 Tool을 선택하여 정보를 조회하는  
**Project Management AI Agent**를 학습하기 위한 PoC 프로젝트입니다.

현재는 LangChain 기반 Tool Calling을 직접 구현하고 있으며,  
추후 LangGraph를 이용해 프로젝트 진행 중 발생하는 문제를 분석하고  
재계획(Replanning)을 제안하는 Agent로 확장할 예정입니다.

---

## Goal

최종적으로 다음과 같은 흐름을 구현하는 것이 목표입니다.

```text
사용자 요청
↓
AI Agent
↓
필요한 Tool 판단
↓
프로젝트 데이터 조회 / 계산
↓
문제 및 영향 분석
↓
재계획안 생성
↓
사용자 승인
↓
Spring Boot에서 실제 변경
