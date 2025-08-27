from flask import Flask, request, jsonify
import os
import glob
import re

app = Flask(__name__)

# Configuration - load from environment variables
OBSIDIAN_VAULT = "C:\\Users\\dashp\\.gemini\\obsidianVault"
if not OBSIDIAN_VAULT or not os.path.exists(OBSIDIAN_VAULT):
    print("⚠️ WARNING: OBSIDIAN_VAULT_PATH not set or invalid!")
    print("Set it with: export OBSIDIAN_VAULT_PATH=/path/to/your/vault")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/obsidian/query', methods=['POST', 'GET'])
def query_obsidian():
    """Handle Obsidian vault queries with better context extraction"""
    query = request.json.get('query', '').strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400
    
    results = []
    
    try:
        # Search all markdown files in vault
        for md_file in glob.glob(f"{OBSIDIAN_VAULT}/**/*.md", recursive=True):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Find all occurrences of the query
                    for match in re.finditer(re.escape(query), content, re.IGNORECASE):
                        start = max(0, match.start() - 150)
                        end = min(len(content), match.end() + 150)
                        
                        # Get context around the match
                        context = content[start:end].replace('\n', ' ').strip()
                        context = re.sub(r'\s+', ' ', context)
                        
                        # Highlight the query term
                        highlighted = context.replace(
                            query, 
                            f"**{query}**"
                        ) if query.lower() in context.lower() else context
                        
                        results.append({
                            "file": os.path.relpath(md_file, OBSIDIAN_VAULT),
                            "snippet": highlighted,
                            "relevance": len(query) / len(context)  # Simple relevance score
                        })
            except Exception as e:
                print(f"Error reading {md_file}: {str(e)}")
        
        # Sort by relevance (simple approach)
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return jsonify({
            "query": query,
            "results": results[:5],  # Return top 5 results
            "total": len(results)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keep your GitHub and Slack endpoints as before
# ... (rest of your mcp_server.py remains the same)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)