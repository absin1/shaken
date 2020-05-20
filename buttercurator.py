from flask import Flask, request, jsonify, Response, render_template, send_from_directory
import pickle 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('asr2.html')

@app.route('/asr_snips')
def asr_snips():
    page = 0
    page_size = 50
    if 'page' in request.args:
        page = int(request.args['page'])
    if 'page_size' in request.args:
        page_size = int(request.args['page_size'])
    resp = Response(jsonpickle.encode(snippets[page*page_size,page*(page_size+1)]), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route('/snip_asr')
def asr_snippets():
    rows = []
    if 'snippet_id' in request.args:
        snippet_id = int(request.args['snippet_id'])
        text = request.args['text']
        created_by = request.args['created_by']
        sql = "INSERT INTO public.snippet_asr (snippet_id, created_at, text_, created_by) VALUES(%s, now(), %s, %s);"
        rows, col_names = db.DBUtils.get_instance().execute_query(sql, (snippet_id, text, created_by),
                                                                  is_write=True, is_return=False)
    resp = Response(jsonpickle.encode(rows), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

snippets = []

if __name__ == '__main__':
    with open('/home/absin/Documents/shaken2/shaken.pickle', 'rb') as handle:
        snippets = pickle.load(handle)
        print('loaded {} utterances'.format(len(snippets)))
    app.run(host="0.0.0.0", port="9998", debug=True)

