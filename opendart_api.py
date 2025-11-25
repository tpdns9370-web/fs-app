import requests
from typing import Dict, List, Optional
from datetime import datetime

class OpenDartAPI:
    """오픈다트 API 클라이언트"""
    
    BASE_URL = "https://opendart.fss.or.kr/api"
    
    # 보고서 코드
    REPORT_CODES = {
        '사업보고서': '11011',
        '반기보고서': '11012',
        '1분기보고서': '11013',
        '3분기보고서': '11014'
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_financial_data(self, corp_code: str, bsns_year: str, reprt_code: str = '11011') -> Optional[Dict]:
        """
        단일회사 주요계정 조회
        
        Args:
            corp_code: 고유번호 (8자리)
            bsns_year: 사업연도 (4자리)
            reprt_code: 보고서 코드 (기본값: 11011 사업보고서)
        
        Returns:
            API 응답 데이터 또는 None
        """
        url = f"{self.BASE_URL}/fnlttSinglAcnt.json"
        
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'bsns_year': bsns_year,
            'reprt_code': reprt_code
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '000':  # 정상
                return data
            else:
                print(f"API 오류: {data.get('message', '알 수 없는 오류')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"API 요청 오류: {e}")
            return None
    
    def parse_financial_data(self, api_response: Dict) -> Dict:
        """
        API 응답 데이터를 시각화에 적합한 형태로 파싱
        
        Returns:
            파싱된 재무 데이터
        """
        if not api_response or api_response.get('status') != '000':
            return {}
        
        data_list = api_response.get('list', [])
        if not data_list:
            return {}
        
        # 연결재무제표(CFS) 데이터 우선 사용
        cfs_data = [item for item in data_list if item.get('fs_div') == 'CFS']
        ofs_data = [item for item in data_list if item.get('fs_div') == 'OFS']
        
        # 연결재무제표가 있으면 사용, 없으면 개별재무제표 사용
        target_data = cfs_data if cfs_data else ofs_data
        
        # 재무상태표(BS)와 손익계산서(IS) 분리
        bs_data = [item for item in target_data if item.get('sj_div') == 'BS']
        is_data = [item for item in target_data if item.get('sj_div') == 'IS']
        
        parsed = {
            'bsns_year': data_list[0].get('bsns_year', ''),
            'corp_code': data_list[0].get('corp_code', ''),
            'stock_code': data_list[0].get('stock_code', ''),
            'fs_div': data_list[0].get('fs_div', ''),
            'fs_nm': data_list[0].get('fs_nm', ''),
            'balance_sheet': {},
            'income_statement': {}
        }
        
        # 재무상태표 주요 계정 추출
        for item in bs_data:
            account_nm = item.get('account_nm', '')
            if account_nm in ['자산총계', '부채총계', '자본총계', '유동자산', '비유동자산', 
                             '유동부채', '비유동부채', '자본금', '이익잉여금']:
                parsed['balance_sheet'][account_nm] = {
                    'thstrm_amount': self._parse_amount(item.get('thstrm_amount', '0')),
                    'frmtrm_amount': self._parse_amount(item.get('frmtrm_amount', '0')),
                    'bfefrmtrm_amount': self._parse_amount(item.get('bfefrmtrm_amount', '0')),
                    'thstrm_dt': item.get('thstrm_dt', ''),
                    'frmtrm_dt': item.get('frmtrm_dt', ''),
                    'bfefrmtrm_dt': item.get('bfefrmtrm_dt', '')
                }
        
        # 손익계산서 주요 계정 추출
        for item in is_data:
            account_nm = item.get('account_nm', '')
            if account_nm in ['매출액', '영업이익', '법인세차감전 순이익', '당기순이익(손실)']:
                parsed['income_statement'][account_nm] = {
                    'thstrm_amount': self._parse_amount(item.get('thstrm_amount', '0')),
                    'frmtrm_amount': self._parse_amount(item.get('frmtrm_amount', '0')),
                    'bfefrmtrm_amount': self._parse_amount(item.get('bfefrmtrm_amount', '0')),
                    'thstrm_dt': item.get('thstrm_dt', ''),
                    'frmtrm_dt': item.get('frmtrm_dt', ''),
                    'bfefrmtrm_dt': item.get('bfefrmtrm_dt', '')
                }
        
        return parsed
    
    def _parse_amount(self, amount_str: str) -> int:
        """금액 문자열을 정수로 변환"""
        if not amount_str or amount_str == '-':
            return 0
        try:
            # 쉼표 제거 후 정수로 변환
            return int(amount_str.replace(',', ''))
        except (ValueError, AttributeError):
            return 0
    
    def get_current_year(self) -> str:
        """현재 연도 반환"""
        return str(datetime.now().year)

