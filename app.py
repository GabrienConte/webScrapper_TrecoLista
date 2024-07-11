from flask import Flask, request, jsonify
from web_scraper import get_produto_info, get_produtos_info
import asyncio
import logging

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_product():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        produto_info = get_produto_info(url)
        return jsonify(produto_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/scrape-multiple', methods=['POST'])
def scrape_multiple_products():
    data = request.json
    produtos = data.get('produtos')
    app.logger.info(produtos)
    if not produtos:
        return jsonify({'error': 'Produtos are required'}), 400
    
    try:
        produto_info = asyncio.run(get_produtos_info(produtos, max_concurrent_requests=5, pause_interval=5, pause_duration=1))
        return jsonify(produto_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)