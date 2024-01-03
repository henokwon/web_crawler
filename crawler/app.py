# app.py
from flask import Flask, request, jsonify
from crawler import WebCrawler
from .utils import CrawledData, save_to_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
crawler = WebCrawler()

@app.route('/crawl', methods=['GET'])
def crawl():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL parameter'}), 400

    # Initiate crawling for the provided URL
    content = crawler.crawl(url)

    # Save crawled data to the database
    save_to_database(url, content)

    return jsonify({'message': 'Crawling and saving initiated successfully'}), 200

@app.route('/get_crawled_data', methods=['GET'])
def get_crawled_data():
    database_uri = os.getenv('DATABASE_URI')
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    crawled_data = session.query(CrawledData).all()

    session.close()

    data = [{'url': item.url, 'content': item.content} for item in crawled_data]

    return jsonify({'crawled_data': data}), 200

@app.route('/save_crawled_data', methods=['POST'])
def save_crawled_data():
    try:
        database_uri = os.getenv('DATABASE_URI')
        engine = create_engine(database_uri)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch crawled data from the temporary storage (replace with your actual storage mechanism)
        crawled_data = session.query(CrawledData).all()

        # Save crawled data to the main database
        for data in crawled_data:
            save_to_database(data.url, data.content)

        # Optionally, you may clear the temporary storage if needed
        session.query(CrawledData).delete()
        session.commit()

        session.close()

        return jsonify({'message': 'Crawled data saved successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Error saving crawled data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
