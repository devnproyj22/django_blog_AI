from datetime import datetime

def current_year(request):
    '''컨텍스트 프로세서: 현재 연도를 템플릿에서 사용'''
    return {
        'current_year': datetime.now().year
    }