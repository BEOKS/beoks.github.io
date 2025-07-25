---
title: 디지털 서명 (Digital Signature)
date: 2025-07-04
---

디지털 서명은 디지털 문서나 메시지의 진위성, 무결성, 그리고 부인 방지를 보장하는 데 사용되는 암호화 기술입니다. 이는 손으로 쓰는 서명과 유사하지만, 훨씬 더 높은 수준의 보안을 제공합니다.

## 1. 작동 원리

디지털 서명은 주로 [[공개 키 암호화 (Public Key Cryptography)]], [[해시 함수]], 그리고 [[디지털 인증서]]의 세 가지 핵심 기술을 기반으로 작동합니다.

1.  **해싱 (Hashing)**: 서명하려는 원본 문서나 메시지는 먼저 해시 함수를 통해 고정된 길이의 고유한 값인 '해시값' (또는 메시지 다이제스트)으로 변환됩니다. 이 해시값은 원본 데이터의 '디지털 지문'과 같아서, 원본 내용이 조금이라도 변경되면 해시값도 완전히 달라집니다.
2.  **서명 생성**: 서명자는 자신의 [[개인 키]]를 사용하여 이 해시값을 암호화합니다. 이렇게 암호화된 해시값이 바로 '디지털 서명'이 됩니다. 서명은 원본 문서와 함께 수신자에게 전송됩니다.
3.  **서명 검증**: 수신자는 서명된 문서와 디지털 서명을 받으면 다음 단계를 거쳐 검증합니다.
    *   수신자는 받은 원본 문서에 동일한 해시 함수를 적용하여 새로운 해시값을 생성합니다.
    *   서명자가 제공한 [[공개 키]]를 사용하여 디지털 서명을 복호화합니다.
    *   수신자가 직접 계산한 해시값과 복호화된 해시값을 비교합니다. 두 해시값이 일치하면, 문서가 서명된 이후 변경되지 않았으며, 서명이 올바른 개인 키로 생성되었음을 의미합니다.

이 과정에서 [[인증 기관(CA)]]은 공개 키가 특정 개인이나 기관에 속함을 보증하는 디지털 인증서를 발급하여 신뢰성을 더합니다.

## 2. 장점

디지털 서명은 다음과 같은 여러 가지 중요한 장점을 제공합니다.

*   **무결성 (Integrity)**: 문서나 메시지가 서명된 이후 위변조되지 않았음을 보장합니다.
*   **인증 (Authentication)**: 메시지가 실제로 특정 개인이나 기관에 의해 생성되었음을 확인할 수 있습니다.
*   **부인 방지 (Non-repudiation)**: 서명자가 나중에 자신이 서명한 사실을 부인할 수 없도록 합니다.
*   **보안 강화**: 공개 키 기반 구조(PKI) 기술을 기반으로 하여 높은 수준의 보안을 제공하며, 사기 및 변조를 방지합니다.
*   **효율성 및 비용 절감**: 종이 문서 인쇄, 우편 발송, 보관 등의 필요성을 줄여 비용을 절감하고 업무 처리 속도를 높입니다.
*   **편의성 및 접근성**: 언제 어디서든 어떤 기기에서든 서명할 수 있어 원격 작업 환경에 적합하며 사용자 경험을 향상시킵니다.
*   **법적 유효성**: 많은 국가에서 법적 구속력을 가집니다.

## 3. 사용 사례

디지털 서명은 다양한 분야에서 활용되어 디지털 환경의 신뢰성과 효율성을 높이고 있습니다.

*   **전자 문서 서명**: 계약서, 법률 문서, 재무 보고서 등 다양한 디지털 문서에 서명하여 법적 유효성과 무결성을 보장합니다.
*   **소프트웨어 배포**: 소프트웨어의 원본 개발자를 확인하고, 다운로드된 소프트웨어가 변조되지 않았음을 검증하는 데 사용됩니다.
*   **금융 거래**: 온라인 뱅킹, 주식 거래, 암호화폐 거래 등에서 거래의 진위성과 무결성을 확인하고 사용자 신원을 인증합니다.
*   **이메일 보안**: 이메일 발신자의 신원을 확인하고, 이메일 내용이 전송 중에 변경되지 않았음을 보장합니다.
*   **정부 및 공공 서비스**: 정부 문서, 세금 신고, 민원 처리 등에서 본인 확인 및 문서의 신뢰성을 확보합니다.
*   **의료 분야**: 전자 처방전, 의료 기록 등에 적용되어 위변조를 방지하고 데이터 무결성을 유지합니다.
*   **블록체인 및 암호화폐**: 블록체인 네트워크에서 각 사용자가 자신의 거래를 증명하고 검증하는 핵심 수단으로 사용됩니다.
*   **DNS 서버 보안 (DNSSEC)**: DNS 서비스의 유효성을 보장하기 위해 DNS 메시지에 디지털 서명을 남겨 보안을 강화합니다.

## 결론

디지털 서명은 키 분배의 어려움을 해결하고, 디지털 서명을 통한 인증 및 부인 방지 기능을 제공하여 현대 정보 보안에 필수적인 역할을 합니다. 비록 대칭 키 암호화보다 속도가 느리다는 단점이 있지만, 이를 보완하는 하이브리드 암호화 방식과 PKI와 같은 추가적인 보안 메커니즘을 통해 광범위하게 활용되고 있습니다.

## 참고 자료

1.  Wikipedia: Public-key cryptography.
2.  MDN Web Docs: Transport Layer Security (TLS).
