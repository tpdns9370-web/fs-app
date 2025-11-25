import google.generativeai as genai
from typing import Dict, Optional
import json

class GeminiAnalyzer:
    """Gemini API를 사용한 재무 데이터 분석 클래스"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        # 사용 가능한 모델 순서대로 시도
        model_names = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.0-flash']
        self.model = None
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"Gemini 모델 초기화 성공: {model_name}")
                break
            except Exception as e:
                print(f"모델 {model_name} 초기화 실패: {e}")
                continue
        
        if not self.model:
            raise Exception("사용 가능한 Gemini 모델을 찾을 수 없습니다.")
    
    def analyze_financial_data(self, corp_name: str, financial_data: Dict) -> Optional[str]:
        """
        재무 데이터를 분석하여 인사이트 제공
        
        Args:
            corp_name: 회사명
            financial_data: 파싱된 재무 데이터
        
        Returns:
            AI 분석 결과 텍스트 또는 None
        """
        if not financial_data or not financial_data.get('balance_sheet'):
            return None
        
        bs = financial_data.get('balance_sheet', {})
        is_data = financial_data.get('income_statement', {})
        
        # 재무 데이터 요약 생성
        prompt = self._create_analysis_prompt(corp_name, bs, is_data)
        
        try:
            response = self.model.generate_content(prompt)
            
            # 응답 확인
            if not response:
                print("Gemini API: 응답이 없습니다.")
                return None
            
            # 텍스트 추출
            if hasattr(response, 'text'):
                text = response.text
                if text:
                    return text
                else:
                    print("Gemini API: 응답 텍스트가 비어있습니다.")
                    return None
            else:
                # 다른 형식의 응답 처리
                if hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        text = ''.join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                        if text:
                            return text
                
                print(f"Gemini API: 예상치 못한 응답 형식 - {type(response)}")
                return None
                
        except Exception as e:
            error_msg = str(e)
            print(f"Gemini API 오류: {error_msg}")
            print(f"오류 타입: {type(e).__name__}")
            # 오류 메시지를 반환하여 클라이언트에 전달할 수 있도록 함
            raise Exception(f"Gemini API 오류: {error_msg}")
    
    def _create_analysis_prompt(self, corp_name: str, balance_sheet: Dict, income_statement: Dict) -> str:
        """분석 프롬프트 생성"""
        
        # 재무상태표 데이터 정리
        bs_summary = []
        if balance_sheet.get('자산총계'):
            asset = balance_sheet['자산총계']
            bs_summary.append(f"자산총계: 당기 {self._format_korean(asset.get('thstrm_amount', 0))}원")
            if asset.get('frmtrm_amount'):
                bs_summary.append(f"전기 {self._format_korean(asset.get('frmtrm_amount', 0))}원")
        
        if balance_sheet.get('부채총계'):
            liability = balance_sheet['부채총계']
            bs_summary.append(f"부채총계: 당기 {self._format_korean(liability.get('thstrm_amount', 0))}원")
            if liability.get('frmtrm_amount'):
                bs_summary.append(f"전기 {self._format_korean(liability.get('frmtrm_amount', 0))}원")
        
        if balance_sheet.get('자본총계'):
            equity = balance_sheet['자본총계']
            bs_summary.append(f"자본총계: 당기 {self._format_korean(equity.get('thstrm_amount', 0))}원")
            if equity.get('frmtrm_amount'):
                bs_summary.append(f"전기 {self._format_korean(equity.get('frmtrm_amount', 0))}원")
        
        # 손익계산서 데이터 정리
        is_summary = []
        if income_statement.get('매출액'):
            revenue = income_statement['매출액']
            is_summary.append(f"매출액: 당기 {self._format_korean(revenue.get('thstrm_amount', 0))}원")
            if revenue.get('frmtrm_amount'):
                is_summary.append(f"전기 {self._format_korean(revenue.get('frmtrm_amount', 0))}원")
        
        if income_statement.get('영업이익'):
            op_income = income_statement['영업이익']
            is_summary.append(f"영업이익: 당기 {self._format_korean(op_income.get('thstrm_amount', 0))}원")
            if op_income.get('frmtrm_amount'):
                is_summary.append(f"전기 {self._format_korean(op_income.get('frmtrm_amount', 0))}원")
        
        if income_statement.get('당기순이익(손실)'):
            net_income = income_statement['당기순이익(손실)']
            is_summary.append(f"당기순이익: 당기 {self._format_korean(net_income.get('thstrm_amount', 0))}원")
            if net_income.get('frmtrm_amount'):
                is_summary.append(f"전기 {self._format_korean(net_income.get('frmtrm_amount', 0))}원")
        
        prompt = f"""당신은 재무 분석 전문가입니다. 다음 {corp_name}의 재무 데이터를 분석하여 인사이트를 제공해주세요.

**재무상태표 정보:**
{chr(10).join(bs_summary)}

**손익계산서 정보:**
{chr(10).join(is_summary)}

다음 항목들을 포함하여 분석해주세요:
1. 재무 건전성 평가 (자산, 부채, 자본 구조)
2. 수익성 분석 (매출, 영업이익, 순이익 추이)
3. 전년 대비 주요 변화점
4. 재무 리스크 요인
5. 종합 평가 및 투자 관점에서의 의견

한국어로 작성하고, 구체적인 수치와 비율을 활용하여 분석해주세요. 각 항목을 명확하게 구분하여 작성해주세요."""
        
        return prompt
    
    def _format_korean(self, amount: int) -> str:
        """금액을 한국어 형식으로 변환"""
        if amount >= 1000000000000:
            return f"{amount / 1000000000000:.2f}조"
        elif amount >= 100000000:
            return f"{amount / 100000000:.2f}억"
        elif amount >= 10000:
            return f"{amount / 10000:.2f}만"
        else:
            return f"{amount:,}"

