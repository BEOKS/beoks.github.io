# 📆 <% tp.date.now("YYYY-MM") %>  
<< [[<% tp.date.now("YYYY-MM", -1) %>]] | [[<% tp.date.now("YYYY-MM", +1) %>]] >>  

## 🏆 이번 달 목표
```tasks 
due before next month
```

## 📝 월간 회고
- 이달의 주요 성과:
- 배운 점:
- 개선할 점:

## 📂 이번 달 주간 노트
<% tp.date.range("gggg-[W]ww", "gggg-[W]ww", tp.date.now("YYYY-MM-01", "startofmonth", 0, "week"), tp.date.now("YYYY-MM-01", "startofmonth", 4, "week")).map(date => `- [[${date}]]`).join("\n") %>
