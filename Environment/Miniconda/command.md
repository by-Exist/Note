<!-- https://conda.io/projects/conda/en/latest/user-guide/tasks/index.html -->

# **[ 도움말 ]**

| 동작                     | 커맨드                               |
| ------------------------ | ------------------------------------ |
| conda에 대한 도움말      | conda -h                             |
| conda command_string + h | conda -h로 command들을 확인하여 활용 |

&nbsp;

&nbsp;

# **[ Conda 관리 ]**

| 동작      | 커맨드             |
| --------- | ------------------ |
| 버전 확인 | conda info         |
| 정보 확인 | conda -V           |
| 업데이트  | conda update conda |

&nbsp;

&nbsp;

# **[ 가상환경 관리 ]**

| 동작                                 | 커맨드                                                       |
| ------------------------------------ | ------------------------------------------------------------ |
| .                                    | .                                                            |
| 환경 생성                            | conda create -n my_env                                       |
| 파이썬 버전을 지정하며 환경 생성     | conda create -n my_env python=3.6                            |
| environment.yml의 구성으로 환경 생성 | conda create -f environment.yml                              |
| 환경 복사                            | conda env create -n new_env --clone my_env                   |
| 환경 제거                            | conda env remove -n my_env                                   |
| 환경 목록 보기                       | conda env list                                               |
| .                                    | .                                                            |
| 환경 활성화                          | conda activate my_env                                        |
| 환경 비활성화                        | conda deactivate                                             |
| .                                    | .                                                            |
| 변경 내역 확인                       | (activate) conda list --revisions                            |
| 환경 복구                            | (activate) conda install --rev rev_number                    |
| .                                    | .                                                            |
| 환경변수 등록                        | (activate) conda env config vars set my_var=value            |
| 환경변수 제거                        | (activate) conda env config vars unset my_var                |
| 환경변수 목록                        | (activate) conda env config vars list                        |
| .                                    | .                                                            |
| 호환성 있는 environment.yml 생성     | (activate) conda env export > environment.yml                |
| 종속적인 environment.yml 생성        | (activate) conda env export --from-history > environment.yml |

&nbsp;

&nbsp;

# **[ 패키지 관리 ]**

## conda로 설치할 수 없는 패키지가 pip로 설치 가능하다면

1. 가능한 많은 패키지를 conda를 써서 설치한 뒤 pip를 이용해 설치를 진행.
2. conda list pip (환경 내부 pip가 설치되어 있는지 확인)\
   1. conda install pip (없다면 설치)\
3. pip install package_name\
4. conda list (정상적으로 패키지가 설치되었는지 확인)

| 동작             | 커맨드                                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 패키지 검색      | conda search scipy                                                                                                            |
| .                | .                                                                                                                             |
| 패키지 설치      | (activate) conda install scipy=0.15.0 curl=7.26.0                                                                             |
| 업데이트         | (activate) conda update package_name                                                                                          |
| 패키지 제거      | (activate) conda remove package_name                                                                                          |
| .                | .                                                                                                                             |
| 패키지 목록      | (activate) conda list                                                                                                         |
| 패키지 목록 검색 | (activate) conda list package_name                                                                                            |
| .                | .                                                                                                                             |
| 업데이트 방지    | [Link](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html#preventing-packages-from-updating-pinning) |

&nbsp;

&nbsp;

# **[ 파이썬 관리 ]**

| 동작                                      | 커맨드                                                     |
| ----------------------------------------- | ---------------------------------------------------------- |
| 파이썬 버전 목록 확인                     | conda search python                                        |
| .                                         | .                                                          |
| 다른 버전의 파이썬 사용                   | 파이썬 버전을 지정해주는 방식으로 새로운 가상환경을 만들자 |
| .                                         | .                                                          |
| (부 버전 내에서) 업그레이드               | conda update python                                        |
| 타 버전의 Python 설치를 통하여 업그레이드 | conda install python=3.9                                   |
| .                                         | .                                                          |
| 버전 확인                                 | python -V                                                  |

&nbsp;

&nbsp;

# **[ Not Useful ]**

* Managing virtual packages
* Using conda with Travis CI
* 채널 관리
* 사용자 채널 만들기
