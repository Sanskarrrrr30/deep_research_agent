"""Flask web application for Deep Research Agent"""
from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from modules.retriever import Retriever
from modules.reasoning import Reasoner

app = Flask(__name__)

# Initialize the retriever and reasoner
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
INDEX_DIR = os.path.join(os.path.dirname(__file__), "outputs", "index")
os.makedirs(INDEX_DIR, exist_ok=True)

# Global variables to store the initialized objects
retriever = None
reasoner = None

def initialize_system():
    """Initialize the retriever and reasoner if not already done"""
    global retriever, reasoner
    if retriever is None:
        retriever = Retriever(data_dir=DATA_DIR, index_dir=INDEX_DIR)
        retriever.build_or_load_index(force_rebuild=False)  # Don't force rebuild on web
        reasoner = Reasoner(retriever)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    try:
        initialize_system()
        
        data = request.get_json()
        query_text = data.get('query', '').strip()
        
        if not query_text:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Run multi-step reasoning
        combined, summary = reasoner.answer(query_text)
        
        # Export results to file
        export_path = os.path.join("outputs", "result.md")
        reasoner.answer_and_export(query_text, export_path=export_path)
        
        return jsonify({
            'query': query_text,
            'evidence': combined,
            'summary': summary,
            'export_path': export_path
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Check if the system is initialized"""
    try:
        initialize_system()
        return jsonify({'status': 'ready', 'data_files': len(os.listdir(DATA_DIR)) if os.path.exists(DATA_DIR) else 0})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/rebuild-index', methods=['POST'])
def rebuild_index():
    """Force rebuild the index"""
    try:
        global retriever, reasoner
        retriever = Retriever(data_dir=DATA_DIR, index_dir=INDEX_DIR)
        retriever.build_or_load_index(force_rebuild=True)
        reasoner = Reasoner(retriever)
        return jsonify({'status': 'success', 'message': 'Index rebuilt successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/download-result')
def download_result():
    """Download the latest result file"""
    result_path = os.path.join("outputs", "result.md")
    if os.path.exists(result_path):
        return send_file(result_path, as_attachment=True)
    else:
        return jsonify({'error': 'No result file found'}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)