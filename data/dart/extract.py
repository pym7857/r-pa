from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

### 회사고유번호 데이터 불러오기
url = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=5f1d10ac04bc83ed14b340b5a39a0418bd0261c6'
with urlopen(url) as zipresp:
    with ZipFile(BytesIO(zipresp.read())) as zfile:
        zfile.extractall('corp_num') # XML파일로 추출

