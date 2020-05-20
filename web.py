from flask import Flask, request, jsonify, Response, render_template, send_from_directory
import pickle
import jsonpickle
import random
from objects import Utterance, Speaker

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('asr2.html')


@app.route('/read')
def read_snippets():
    page = 0
    page_size = 25
    search = ''
    if 'q' in request.args:
        search = request.args['q']
    if 'page' in request.args:
        page = int(request.args['page'])
    if 'page_size' in request.args:
        page_size = int(request.args['page_size'])
    chosen_snippets = []
    if len(search) > 0:
        for index1, snippet in enumerate(snippets):
            if index1 > page * page_size:
                if search in snippet.sid:
                    chosen_snippets.append(snippet)
                if len(chosen_snippets) > page_size:
                    break
    else:
        from_index = int(page * page_size)
        to_index = int(page * page_size + page_size)
        print('Showing {} - {} snippets out of {}'.format(from_index, to_index, len(snippets)))
        chosen_snippets = snippets[from_index: to_index]
        # chosen_snippets = random.sample(snippets, page_size)
    res_body = jsonpickle.encode(chosen_snippets)
    resp = Response(res_body, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)


@app.route('/audio/<path:path>')
def send_audio(path):
    return send_from_directory('audio_files', path)


@app.route('/update')
def update_snippet():
    snippet_id = text = created_by = None
    if 'snippet_id' in request.args:
        snippet_id = request.args['snippet_id']
    if 'text' in request.args:
        text = request.args['text']
    if 'created_by' in request.args:
        created_by = request.args['created_by']
    snippet = None
    for s in snippets:
        if s.sid == snippet_id:
            snippet = s
    print('Changing text of snippet {} to {} by {}'.format(snippet_id, text, created_by))
    resp = Response('{"message":"Please supply a correct snippet id"}', mimetype='application/json', status=400)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/delete')
def delete_snippet():
    snippet_id = None
    if 'snippet_id' in request.args:
        snippet_id = request.args['snippet_id']
    snippet = None
    print('Deleting snippet {}'.format(snippet_id))
    for ind, s in enumerate(snippets):
        if s.sid == snippet_id:
            snippet = s
            break
    if snippet is None:
        print('While deleting snippet {} not found'.format(snippet_id))
        resp = Response('{"message":"Please supply a correct snippet id"}', mimetype='application/json', status=400)
    else:
        print('Before deleting snippet {} there are {} snippets'.format(snippet_id, len(snippets)))
        snippets.pop(ind)
        print('After deleting snippet {} there are {} snippets'.format(snippet_id, len(snippets)))
        snippet1=None
        for ind1, s1 in enumerate(snippets):
            if s1.sid == snippet_id:
                snippet1 = s1
                break
        if snippet1 is None:
            print('Confirm deleting snippet {} there are {} snippets'.format(snippet_id, len(snippets)))
        resp = Response(jsonpickle.encode(snippet), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

snippets = []

if __name__ == '__main__':
    with open('/home/absin/Documents/shaken2/shaken.utterances', 'rb') as handle:
        snippets = pickle.load(handle)
        print('loaded {} utterances'.format(len(snippets)))
        for s in snippets:
            s.set_sid(s.path.split('/')[2].split('.')[0])
    app.run(host="0.0.0.0", port="9998", debug=True)
