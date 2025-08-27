---
title: Passkey 개발자 가이드
date: 2025-07-04
---

Passkey, WebAuthn, FIDO는 현대 웹 환경에서 비밀번호 없는(passwordless) 인증을 구현하기 위한 핵심 기술 스택입니다. 개발자 관점에서 이들의 기술적 세부 사항을 이해하는 것은 안전하고 사용자 친화적인 인증 시스템을 구축하는 데 필수적입니다.

## 1. Passkey (패스키) 개요

패스키는 사용자 계정과 웹사이트 또는 애플리케이션에 연결된 디지털 자격 증명입니다. 이는 기존의 비밀번호를 대체하며, 사용자 이름이나 비밀번호를 입력할 필요 없이, 또는 추가적인 인증 요소를 제공할 필요 없이 사용자가 인증할 수 있도록 합니다.

**주요 특징 및 장점:**

*   **비밀번호 없는 경험**: 사용자가 비밀번호를 기억하고 관리할 필요가 없어 사용자 경험이 향상됩니다.
*   **피싱 저항성**: 패스키는 웹사이트 또는 앱의 ID에 바인딩되어 있어 피싱 공격에 강합니다. 브라우저와 운영 체제는 패스키가 생성된 웹사이트 또는 앱에서만 사용될 수 있도록 보장합니다.
*   **공개 키 암호화 사용**: 패스키는 공개 키 암호화를 활용합니다. 사용자가 웹사이트나 애플리케이션에 패스키를 생성하면, 사용자 장치에 공개-개인 키 쌍이 생성됩니다. 서버에는 공개 키만 저장되며, 이 공개 키만으로는 공격자가 사용자의 개인 키를 유추할 수 없어 데이터 유출의 위협이 줄어듭니다.

**WebAuthn 및 FIDO와의 관계**: 패스키는 WebAuthn 표준을 사용하여 생성되는 자격 증명의 한 유형이며, WebAuthn은 FIDO2 프레임워크의 일부입니다. 즉, WebAuthn이 패스키를 가능하게 하는 기반 기술 사양이며, 패스키는 WebAuthn 기술의 사용자 친화적인 구현체라고 볼 수 있습니다.

## 2. FIDO (Fast Identity Online) Alliance 및 FIDO2

FIDO Alliance는 비밀번호 없는 인증 표준 및 프로토콜을 개발하고 홍보하는 산업 컨소시엄입니다. FIDO2는 FIDO Alliance의 최신 사양 세트로, 비밀번호 없는 인증을 가능하게 합니다.

**FIDO2의 주요 구성 요소:**

*   **WebAuthn (Web Authentication API)**: W3C(World Wide Web Consortium) 표준으로, 웹 애플리케이션이 공개 키 암호화를 사용하여 안전한 인증을 수행할 수 있도록 하는 JavaScript API입니다.
*   **CTAP (Client-to-Authenticator Protocol)**: 클라이언트(브라우저 또는 운영 체제)와 인증 장치(보안 키, 스마트폰, 생체 인식 장치 등) 간의 통신을 위한 프로토콜입니다.

## 3. WebAuthn 기술 세부 사항

WebAuthn은 웹 애플리케이션이 강력하고, 증명되며, 범위가 지정된 공개 키 기반 자격 증명을 생성하고 사용하여 사용자를 강력하게 인증할 수 있도록 하는 API를 정의합니다.

**핵심 원리**: WebAuthn은 공개 키 암호화를 사용합니다. 사용자의 개인 키는 장치에 안전하게 저장되며, 공개 키는 서버(Relying Party)에 저장됩니다.

**주요 참여자:**

*   **Relying Party (RP)**: 인증을 제공하는 웹사이트 또는 서비스입니다.
*   **User Agent (사용자 에이전트)**: 브라우저 또는 운영 체제로, RP와 인증 장치 간의 통신을 중재합니다.
*   **Authenticator (인증 장치)**: 암호화 작업을 수행하는 물리적 장치 또는 소프트웨어입니다 (예: 지문 인식기, 보안 키, 스마트폰).

### WebAuthn 인증 흐름

WebAuthn은 크게 두 가지 주요 흐름으로 구성됩니다: 등록(Registration) 흐름과 인증(Authentication) 흐름입니다.

#### 3.1. 등록 (Attestation) 흐름

사용자가 서비스에 처음으로 패스키를 등록하는 과정입니다.

1.  **사용자 등록 시작**: 사용자가 RP 웹사이트에서 패스키 등록을 시작합니다.
2.  **RP 챌린지 생성**: RP 서버는 암호화된 챌린지(Challenge)를 생성하고 이를 브라우저로 전송합니다. 이 챌린지는 재생 공격(Replay Attack)을 방지하기 위한 일회성 무작위 문자열입니다.
3.  **브라우저 API 호출**: 브라우저는 `navigator.credentials.create()` JavaScript API를 호출하며, 이 때 RP ID, 사용자 정보, 챌린지 등의 옵션을 전달합니다.
4.  **인증 장치 사용자 확인**: 인증 장치는 사용자에게 생체 인식(지문, 얼굴 인식) 또는 PIN 입력과 같은 사용자 확인(User Verification)을 요청합니다.
5.  **키 쌍 생성**: 사용자 확인이 완료되면, 인증 장치는 새로운 공개-개인 키 쌍을 생성합니다. 개인 키는 장치 내부에 안전하게 저장되며 외부로 노출되지 않습니다.
6.  **자격 증명 데이터 전송**: 인증 장치는 생성된 공개 키, 자격 증명 ID(Credential ID), 그리고 증명 데이터(Attestation Data)를 브라우저로 다시 전송합니다.
7.  **브라우저 -> RP 서버**: 브라우저는 이 자격 증명 데이터를 RP 서버로 전달합니다.
8.  **RP 서버 검증 및 저장**: RP 서버는 수신된 데이터를 검증합니다. 이 검증에는 Origin 확인, 증명 데이터의 유효성, 챌린지 일치 여부 등이 포함됩니다. 검증이 성공하면, RP 서버는 해당 사용자와 공개 키 및 자격 증명 ID를 연결하여 저장합니다.

#### 3.2. 인증 (Assertion) 흐름

사용자가 이전에 등록된 패스키를 사용하여 서비스에 로그인하는 과정입니다.

1.  **사용자 로그인 시작**: 사용자가 RP 웹사이트에서 로그인을 시작합니다.
2.  **RP 챌린지 생성**: RP 서버는 새로운 챌린지를 생성하고 이를 브라우저로 전송합니다. 이 때, 이전에 등록된 자격 증명 ID 목록을 함께 보낼 수 있습니다.
3.  **브라우저 API 호출**: 브라우저는 `navigator.credentials.get()` JavaScript API를 호출하며, 이 때 RP ID, 챌린지, 허용된 자격 증명 ID 목록 등의 옵션을 전달합니다.
4.  **인증 장치 사용자 확인**: 인증 장치는 사용자에게 생체 인식 또는 PIN 입력과 같은 사용자 확인을 요청합니다.
5.  **챌린지 서명**: 사용자 확인이 완료되면, 인증 장치는 저장된 개인 키를 사용하여 RP가 보낸 챌린지에 서명합니다.
6.  **서명된 챌린지 전송**: 인증 장치는 서명된 챌린지(어설션)를 브라우저로 다시 전송합니다.
7.  **브라우저 -> RP 서버**: 브라우저는 이 서명된 챌린지를 RP 서버로 전달합니다.
8.  **RP 서버 검증**: RP 서버는 수신된 서명된 챌린지를 이전에 저장된 해당 사용자의 공개 키를 사용하여 검증합니다. 또한, Origin 확인, 챌린지 일치 여부, 서명 카운트(replay attack 방지) 등 다른 데이터도 검증합니다. 검증이 성공하면 사용자는 인증됩니다.

## 4. 개발자 구현 참고 사항

*   **클라이언트 측**: 웹 애플리케이션은 브라우저의 `navigator.credentials.create()` (등록) 및 `navigator.credentials.get()` (인증) JavaScript API를 사용하여 WebAuthn 흐름을 시작합니다.
*   **서버 측**: RP 서버는 챌린지를 생성하고, 인증 장치로부터 받은 응답을 검증하며, 사용자의 공개 키와 자격 증명 ID를 안전하게 저장해야 합니다.
*   **HTTPS 필수**: WebAuthn은 보안 컨텍스트(HTTPS)에서만 작동합니다.

패스키, WebAuthn, FIDO는 비밀번호 없는 미래를 위한 강력한 기반을 제공하며, 개발자는 이 기술들을 이해하고 구현함으로써 사용자에게 더 안전하고 편리한 인증 경험을 제공할 수 있습니다.

## 참고 자료

*   An Overview of WebAuthn | Curity.
*   A Short Introduction to WebAuthn Authentication. - Auth0.
*   WebAuthn Guide.
*   WebAuthn: How it Works & Example Flows - Descope.
*   FIDO2: Web Authentication (WebAuthn) - FIDO Alliance.
*   High Level WebAuthn Authentication flow - Yubico Developers.
*   FIDO2 Authentication Guide: Implementation for Developers - Deepak Gupta.
*   The Ultimate guide to WebAuthn registration and auth flows - Okta.
*   Passwordless Authentication with WebAuthn: A New Era of Security - Medium.
*   What Is FIDO2? | Microsoft Security.
*   How FIDO2 works technically - coding blog.
*   Authentication - How it Works | WebAuthn.wtf.
*   Web Authentication API - MDN Web Docs - Mozilla.
*   Specifications - passkeys.dev.
*   passkey - A developer guide. A quick technical introduction and… | by Shekhar Jha.
*   Developer Documents - Passkey Central.
*   What Is FIDO2 & How Does FIDO Authentication Work? - Descope.
*   Passkeys - Google for Developers.
*   WebAuthn Introduction - Yubico Developers.
*   Developer Guide: How to Implement Passkeys - Descope.
*   How Do They Work? - Passkeys.io.
*   Web Authentication: An API for accessing Public Key Credentials - Level 3 - W3C.
