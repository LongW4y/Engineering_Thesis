import numpy as np

def euclidian_distance(x1, x2, y1, y2, z1, z2):
    return np.sqrt(np.sum(x2-x1)**2)

class KNN:
    
    def __init__(self, k=3):
        self.k = k
        
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
    
    def predict(self, X):
        predicted_labels = [self._predict(x) for x in X]
        return np.array(predicted_labels)
        
    def _predict(self, x):
        # find the distance
        distances = [euclidian_distance(x, x_train) for x_train in self.X_train]
        # get k nearest neighbors
        sortedDistances = np.argsort(distances)
        k_nearest_labels = [self.y_train[i] for i in sortedDistances]
        
        # based on the conditions we choose
        most_common = Counter
    
    
    