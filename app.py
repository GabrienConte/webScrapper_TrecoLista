from flask import Flask, request, jsonify
from web_scraper import get_product_info

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape_product():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        product_info = get_product_info(url)
        return jsonify(product_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)