# Mastodon Credential Generator

마스토돈 API를 활용하기 위한 키를 생성해주는 파이선 스크립트입니다.

A Python script that generates authentication key for using Mastodon API.

# 사용법 Usage

```
python credential.py [action]
```

## action

- `register`

새로운 키를 생성합니다.

Generates a new key

- `delete`

등록된 키를 삭제합니다. 삭제 과정 중에 키가 담긴 파일명을 요구할 것입니다.

Deletes previously registered key. May require filename containing credential.

- - -

파이선 스크립트 내에서 `import credential` 하여 `retrieve()` 함수를 사용할 수 있습니다. `사용자명`과 `인스턴스 주소`, `인증 내역이 저장된 파일명`을 요구할 수 있습니다.

You can use `retrieve()` function by `import credential` inside Python script. May require `username`, `instance address` and `filename containing auth credential`.

# Requirements

- Python3
- [Requests](https://github.com/psf/requests)
