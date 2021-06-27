from flask import Flask, request, jsonify
from model import show, episode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSON_SORT_KEYS'] = False

@app.before_first_request
def create_tables():
    alchemy.create_all()

@app.route('/',methods=['GET'])
def home():
    return "API funcionando", 200

@app.route('/show',methods=['POST'])
def create_show():
    request_data = request.get_json()
    new_show = show.ShowModel(request_data['name'])
    new_show.save_to_db()
    result = show.ShowModel.find_by_id(new_show.id)
    return jsonify(result.json())

@app.route('/show/<string:name>')
def get_show(name):
    result = show.ShowModel.find_by_name(name)
    if result:
        return result.json()
    return {'message': 'Série não encontrada'}, 404

@app.route('/show/<string:name>/episode',methods=['POST'])
def create_episode_in_show(name):
    request_data = request.get_json()
    parent = show.ShowModel.find_by_name((name))
    if parent:
        new_episode = episode.EpisodeModel(name=request_data['name'],
                                           season=request_data['season'],
                                           show_id=parent.id)
        new_episode.save_to_db()
        return new_episode.json()
    else:
        return {'message':'Série não encontrada'}, 404

@app.route('/show/<int:id>',methods=['DELETE'])
def delete_show(id):
    result = show.ShowModel.find_by_id(id)
    if result:
        result.delete_from_db()
        return {'message':'Excluído com sucesso!'}, 202
    else:
        return {'message': 'Série não encontrada!!'}, 404

@app.route('/episode/<int:id>',methods=['DELETE'])
def delete_episode(id):
    result = episode.EpisodeModel.find_by_id(id)
    if result:
        result.delete_from_db()
        return {'message':'Excluído com sucesso!'}, 202
    else:
        return {'message': 'Episódio não encontrado!'}, 404

@app.route('/shows')
def list():
    result = show.ShowModel.list_shows()
    return {'showlist': result}

@app.route('/show',methods=['PUT'])
def update_show():
    request_data = request.get_json()
    result = show.ShowModel.find_by_id(request_data['id'])
    if result:
        result.name = request_data['name']
        result.update()
        return {'message':'Série atualizada com sucesso'}, 200
    else:
        return {'message':'Série não encontrada'}, 404

if __name__ == '__main__':
    from data import alchemy
    alchemy.init_app(app)
    app.run(port=5000, debug=True)
