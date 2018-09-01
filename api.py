from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from sage.all import matrix, latex 
import numpy as np
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)

@app.route('/echo')
@cross_origin()
def echo():
    A = matrix(np.random.randint(9, size=(3,3)))
    
    p = A.characteristic_polynomial()
        
    d = {
        'matrix': latex(A), 
        'charpoly': latex(p),
        'factoredcharpoly': latex(p.factor()),
        'eigenvalues': latex(A.eigenvalues()),
        'eigenvectors': latex(A.eigenvectors_right()),
        'rank': latex(A.rank()),
        'determinant': latex(A.det()),
        'rref': latex(A.echelon_form()),
        'rowspace': latex(A.row_space()),
        'colspace': latex(A.column_space()),
        'nullspace': latex(A.kernel()),
        'inverse': latex(A.inverse()) if A.rank() == 3 else "None"
    }
    return jsonify(d)

if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True)
