from flask import Flask, render_template, request, jsonify
from corp_parser import CorpDatabase
from opendart_api import OpenDartAPI
from gemini_analyzer import GeminiAnalyzer
import os
from datetime import datetime

app = Flask(__name__)

# 모든 템플릿에 last_updated 주입
# 매 요청 시점의 시간을 찍어서, 새로고침하면 항상 갱신되도록 함
@app.context_processor
def inject_last_updated():
    return {'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# XML 파일 경로
XML_PATH = os.path.join(os.path.dirname(__file__), 'corp.xml')

# 데이터베이스 초기화
corp_db = CorpDatabase(XML_PATH)

# 오픈다트 API 초기화
OPENDART_API_KEY = os.getenv('OPENDART_API_KEY')
opendart_api = None
if OPENDART_API_KEY:
    opendart_api = OpenDartAPI(OPENDART_API_KEY)
    print(f"오픈다트 API 초기화 성공")
else:
    print("경고: OPENDART_API_KEY 환경 변수가 설정되지 않았습니다.")

# Gemini API 초기화
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini_analyzer = None
if GEMINI_API_KEY:
    try:
        gemini_analyzer = GeminiAnalyzer(GEMINI_API_KEY)
        print(f"Gemini API 초기화 성공")
    except Exception as e:
        print(f"Gemini API 초기화 실패: {e}")
        gemini_analyzer = None
else:
    print("경고: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

@app.route('/')
def index():
    """메인 검색 페이지"""
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    """회사명 검색 API"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'message': '검색어를 입력해주세요.',
            'results': []
        })
    
    results = corp_db.search_by_name(query)
    
    return jsonify({
        'success': True,
        'query': query,
        'count': len(results),
        'results': results[:100]  # 최대 100개까지만 반환
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """데이터베이스 통계 정보"""
    return jsonify({
        'total_count': corp_db.get_total_count()
    })

@app.route('/financial/<corp_code>')
def financial_view(corp_code):
    """재무 정보 시각화 페이지"""
    corp_info = corp_db.get_by_corp_code(corp_code)
    if not corp_info:
        return "회사 정보를 찾을 수 없습니다.", 404
    
    if not opendart_api:
        return "오픈다트 API가 설정되지 않았습니다.", 500
    
    current_year = opendart_api.get_current_year()
    return render_template('financial.html', corp_info=corp_info, current_year=current_year)

@app.route('/api/financial', methods=['GET'])
def get_financial_data():
    """재무 데이터 조회 API"""
    if not opendart_api:
        return jsonify({
            'success': False,
            'message': '오픈다트 API가 설정되지 않았습니다.'
        }), 500
    
    corp_code = request.args.get('corp_code', '').strip()
    bsns_year = request.args.get('bsns_year', '').strip()
    reprt_code = request.args.get('reprt_code', '11011').strip()
    
    if not corp_code:
        return jsonify({
            'success': False,
            'message': 'corp_code가 필요합니다.'
        }), 400
    
    if not bsns_year:
        bsns_year = opendart_api.get_current_year()
    
    # API 호출
    api_response = opendart_api.get_financial_data(corp_code, bsns_year, reprt_code)
    
    if not api_response:
        return jsonify({
            'success': False,
            'message': '재무 데이터를 가져올 수 없습니다.'
        }), 500
    
    if api_response.get('status') != '000':
        return jsonify({
            'success': False,
            'message': api_response.get('message', '알 수 없는 오류')
        }), 400
    
    # 데이터 파싱
    parsed_data = opendart_api.parse_financial_data(api_response)
    
    return jsonify({
        'success': True,
        'data': parsed_data,
        'raw': api_response
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_financial():
    """AI 재무 분석 API"""
    if not gemini_analyzer:
        return jsonify({
            'success': False,
            'message': 'Gemini API가 설정되지 않았습니다. 환경 변수 GEMINI_API_KEY를 확인해주세요.'
        }), 500
    
    data = request.get_json()
    
    corp_code = data.get('corp_code', '').strip()
    financial_data = data.get('financial_data')
    
    if not corp_code:
        return jsonify({
            'success': False,
            'message': 'corp_code가 필요합니다.'
        }), 400
    
    if not financial_data:
        return jsonify({
            'success': False,
            'message': 'financial_data가 필요합니다.'
        }), 400
    
    # 회사 정보 조회
    corp_info = corp_db.get_by_corp_code(corp_code)
    if not corp_info:
        return jsonify({
            'success': False,
            'message': '회사 정보를 찾을 수 없습니다.'
        }), 404
    
    # AI 분석 수행
    try:
        analysis = gemini_analyzer.analyze_financial_data(
            corp_info.get('corp_name', ''),
            financial_data
        )
        
        if not analysis:
            return jsonify({
                'success': False,
                'message': 'AI 분석 결과가 비어있습니다. 재무 데이터를 확인해주세요.'
            }), 500
    except Exception as e:
        error_msg = str(e)
        print(f"AI 분석 오류: {error_msg}")
        return jsonify({
            'success': False,
            'message': f'AI 분석 중 오류가 발생했습니다: {error_msg}'
        }), 500
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

if __name__ == '__main__':
    print(f"총 {corp_db.get_total_count()}개의 회사 정보가 로드되었습니다.")
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

