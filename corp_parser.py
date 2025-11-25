import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

class CorpDatabase:
    """회사 정보 데이터베이스 클래스"""
    
    def __init__(self, xml_path: str):
        self.corps: List[Dict[str, str]] = []
        self.load_xml(xml_path)
    
    def load_xml(self, xml_path: str):
        """XML 파일을 파싱하여 회사 정보를 메모리에 로드"""
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        for list_item in root.findall('list'):
            corp = {
                'corp_code': list_item.find('corp_code').text if list_item.find('corp_code') is not None else '',
                'corp_name': list_item.find('corp_name').text if list_item.find('corp_name') is not None else '',
                'corp_eng_name': list_item.find('corp_eng_name').text if list_item.find('corp_eng_name') is not None else '',
                'stock_code': list_item.find('stock_code').text if list_item.find('stock_code') is not None else '',
                'modify_date': list_item.find('modify_date').text if list_item.find('modify_date') is not None else ''
            }
            self.corps.append(corp)
    
    def search_by_name(self, query: str) -> List[Dict[str, str]]:
        """회사명으로 검색 (부분 일치)"""
        query = query.strip().lower()
        if not query:
            return []
        
        results = []
        for corp in self.corps:
            corp_name = corp['corp_name'].lower() if corp['corp_name'] else ''
            corp_eng_name = corp['corp_eng_name'].lower() if corp['corp_eng_name'] else ''
            
            if query in corp_name or query in corp_eng_name:
                results.append(corp)
        
        return results
    
    def get_by_corp_code(self, corp_code: str) -> Optional[Dict[str, str]]:
        """corp_code로 회사 정보 조회"""
        for corp in self.corps:
            if corp['corp_code'] == corp_code:
                return corp
        return None
    
    def get_total_count(self) -> int:
        """전체 회사 수 반환"""
        return len(self.corps)

