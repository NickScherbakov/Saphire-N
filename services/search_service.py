import requests
from typing import List, Dict, Any
from config.settings import (
    GOOGLE_SEARCH_API_KEY,
    GOOGLE_CUSTOM_SEARCH_ID,
    GOOGLE_API_URL,
    SEARCH_RESULTS_LIMIT,
    SEARCH_TIMEOUT
)
from utils.logger import logger

class SearchService:
    def __init__(self):
        self.api_key = GOOGLE_SEARCH_API_KEY
        self.search_engine_id = GOOGLE_CUSTOM_SEARCH_ID
        self.api_url = GOOGLE_API_URL
        self.results_limit = SEARCH_RESULTS_LIMIT
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Выполняет поиск в интернете по заданному запросу"""
        try:
            params = {
                'key': self.api_key,
                'cx': self.search_engine_id,
                'q': query,
                'num': self.results_limit
            }
            
            logger.debug(f"Выполняется поиск по запросу: {query}")
            response = requests.get(
                self.api_url,
                params=params,
                timeout=SEARCH_TIMEOUT
            )
            response.raise_for_status()
            
            results = response.json()
            search_results = []
            
            if 'items' in results:
                for item in results['items']:
                    search_results.append({
                        'title': item.get('title', ''),
                        'link': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'google'
                    })
            
            logger.info(f"Найдено {len(search_results)} результатов")
            return search_results
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при выполнении поискового запроса: {str(e)}")
            raise
    
    def analyze_search_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Анализирует результаты поиска и формирует сводку"""
        try:
            summary = {
                'total_results': len(results),
                'sources': set(),
                'main_topics': [],
                'relevant_links': []
            }
            
            for result in results:
                summary['sources'].add(result['source'])
                if result.get('link'):
                    summary['relevant_links'].append({
                        'title': result['title'],
                        'url': result['link']
                    })
            
            summary['sources'] = list(summary['sources'])
            logger.debug(f"Анализ результатов поиска завершен: {len(results)} результатов")
            return summary
            
        except Exception as e:
            logger.error(f"Ошибка при анализе результатов поиска: {str(e)}")
            raise
    
    def fetch_page_content(self, url: str) -> str:
        """Получает содержимое веб-страницы по URL"""
        try:
            logger.debug(f"Загрузка содержимого страницы: {url}")
            response = requests.get(url, timeout=SEARCH_TIMEOUT)
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при загрузке страницы {url}: {str(e)}")
            raise 