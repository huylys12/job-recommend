import json

from flask import Flask, request, jsonify
import job_recommender
from network_builder import *

app = Flask(__name__)

all_expertises = ['Software Developer', 'Mobile Developer', 'Java Developer', 'Testing', 'DevOps Engineer',
                  'Python Developer',
                  'Web Developer', 'Hadoop', 'Blockchain', 'ETL Developer',
                  'Operations Manager', 'Data Science', 'Mechanical Engineer',
                  'Database',
                  'Business Analyst', 'DotNet Developer', 'Automation Testing',
                  'Network Security Engineer', 'SAP Developer', 'Civil Engineer'
                  ]


def load_recommender():
    graphpath = '/Users/huylys12/Documents/2010289/job_recommender/data/network_data/graph.pkl'
    lsapath = '/Users/huylys12/Documents/2010289/job_recommender/data/network_data/lsa.pkl'
    with open(graphpath, 'rb') as f:
        G = pickle.load(f)

    with open(lsapath, 'rb') as f:
        lsa = pickle.load(f)

    recommender = job_recommender.JobRecommender(G, lsa)
    return recommender


recommender = load_recommender()
alpha = 0.8


@app.route("/")
def start():
    return "<h1>Api is running</h1>"


@app.route("/recommend", methods=['POST'])
def recommend():
    resume = request.form['resume']
    major = request.form['major'].strip()
    num_recommend = int(request.form['num_recommend'])
    user_data = {
        'expertise': major,
        'resume': resume
    }

    recommender.add_node_to_graph('candidate', user_data)

    personalized_results = recommender.rank_nodes(True, recommender.target_node, 'job', alpha)
    personalized_results = {key: item for i, (key, item) in enumerate(personalized_results.items()) if
                            i < num_recommend}

    job_list = []
    for key, value in personalized_results.items():
        job_node = recommender.G.nodes[key]
        job = {
            "company": job_node["company_id"],
            "job_name": job_node["job_name"],
            "tags": job_node["taglist"],
            "location": job_node["location"],
            "three_reasons": job_node["three_reasons"],
            "keywords": list(job_node["keywords"]),
            "description": job_node["description"]
        }
        job_list.append(job)

    return {
        "major": major,
        "num_recommend": len(job_list),
        "jobs": job_list
    }


if __name__ == '__main__':
    app.run(debug=True)
