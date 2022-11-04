import gspread
from oauth2client.service_account import ServiceAccountCredentials

def gsheet_upload(date, title, url, offer, message_author, classification="비고"):
    sheet_url = 'https://docs.google.com/spreadsheets/d/ID/edit?usp=sharing'
    scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
    ]
    json_file_name = 'sheetapi.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_url = sheet_url

    #문서 불러오기
    doc = gc.open_by_url(spreadsheet_url)
    #시트 불러오기
    worksheet = doc.worksheet('주제') #시트 페이지명
    
    # #마지막 행 찾기
    def next_available_row(sheet, cols_to_sample=2):
    # looks for empty row based on values appearing in 1st N columns
        cols = sheet.range(1, 1, sheet.row_count, cols_to_sample)
        return max([cell.row for cell in cols if cell.value]) + 1

    next_row = next_available_row(worksheet)


    title = title.replace('"','\'') #큰따옴표가 있으면 작은따옴표로 변환. (HYPERLINK 오류 방지)
    
    worksheet.append_row(['회차', '카테고리', '소분류', date,'타이틀', offer, classification , message_author])
    worksheet.update_acell("E{}".format(next_row),f'=HYPERLINK("{url}","{title}")')