import pandas as pd

df = pd.DataFrame()
print(df)

#반드시 열려있는 엑셀 파일을 닫고, 작업을 진행해야 합니다.
try:
    df.to_excel('C:/JSP/upload/good4.xlsx')
    print('추출 완료!')
except:
    print('추출 에러!')
    print('파일이 열려있다면, 반드시 닫아주세요.')