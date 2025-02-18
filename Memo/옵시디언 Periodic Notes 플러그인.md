- 일일, 주간 그리고 월간 노트를 자동으로 생성해주는 플러그인

## 🔹 **1. 일일 노트 템플릿 설정 (`Templates/daily.md`)**

📌 **어제 / 내일 링크 추가 (Templater 활용)**

예시 템플릿

```
# 📅 {{tp_date}}  
<< [[<% tp.date.now("YYYY-MM-DD", -1) %>]] | [[<% tp.date.now("YYYY-MM-DD", +1) %>]] >>  

## 🌅 오늘의 목표
- [ ] 주요 목표 1
- [ ] 주요 목표 2

## 📝 오늘의 기록
- 아침 운동:
- 업무 중 배운 것:
- 추가 메모:

## 📌 내일 할 일
- [ ] 미리 계획할 작업

```

💡 **이 기능의 효과**:

- 상단에 자동으로 어제와 내일 노트 링크 추가
- Obsidian에서 `Ctrl + Click`으로 빠르게 이동 가능

📌 **설정 적용**

- ⚙️(설정) → **Periodic Notes** → **Daily Note**
    - **"Folder"** → `Daily Notes/`
    - **"Template"** → `Templates/daily.md`
    - **"Date format"** → `YYYY-MM-DD`


다른 주간, 월간도 다음과 같이 설정 가능