import xml.etree.ElementTree as ET
import requests
import pandas as pd
import sys
import pymysql
from datetime import datetime

### 압축파일 안의 xml 파일 읽기
tree = ET.parse('CORPCODE.xml')
root = tree.getroot()

corp_name_lst = []
for country in root.iter("list"):
    corp_name_lst.append( country.findtext("corp_name") )

source = {
    'api_제공_회사명': corp_name_lst
}

df = pd.DataFrame(source)

df.to_excel('api_corp_name.xlsx')
print('추출 완료!')
