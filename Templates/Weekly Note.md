# 🗓️ Week <% tp.date.now("gggg-[W]ww") %>  
<< [[<% tp.date.now("gggg-[W]ww", -1) %>]] | [[<% tp.date.now("gggg-[W]ww", +1) %>]] >>  

## 📌 이번 주 목표
```tasks 
due before next week
```

## ✅ 이번 주 정리
- 주요 성과:
- 배운 점:
- 개선할 점:

## 🗂️ 이번 주 일일 노트
<% tp.date.range("YYYY-MM-DD", "YYYY-MM-DD", tp.date.now("YYYY-MM-DD", "startofweek"), tp.date.now("YYYY-MM-DD", "startofweek", 6)).map(date => `- [[${date}]]`).join("\n") %>
