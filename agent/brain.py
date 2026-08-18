import numpy as np
from sklearn.ensemble import IsolationForest

class ThreatBrain:
    def __init__(self):
        # Synthetic normal baseline data (200 samples)
        # entropy 2.5-5.5, io 1-30, churn 0-2
        np.random.seed(42)
        entropy = np.random.uniform(2.5, 5.5, 200)
        io_velocity = np.random.uniform(1, 30, 200)
        churn = np.random.uniform(0, 2, 200)
        
        self.X_train = np.column_stack((entropy, io_velocity, churn))
        
        self.model = IsolationForest(
            contamination=0.05,
            n_estimators=100,
            random_state=42
        )
        self.model.fit(self.X_train)

    def analyze(self, entropy, io_velocity, extension_churn):
        X_test = np.array([[entropy, io_velocity, extension_churn]])
        prediction = self.model.predict(X_test)[0]
        score = self.model.decision_function(X_test)[0]
        
        is_threat = prediction == -1
        
        # Threat levels based on anomaly score thresholds
        if score > 0:
            threat_level = 'NORMAL'
        elif score > -0.1:
            threat_level = 'ELEVATED'
        elif score > -0.3:
            threat_level = 'HIGH'
        else:
            threat_level = 'CRITICAL'
            
        confidence = abs(score) * 100 # arbitrary confidence scaling
        
        return {
            'is_threat': is_threat,
            'anomaly_score': float(score),
            'confidence': float(confidence),
            'threat_level': threat_level
        }

    def get_status(self):
        return {
            'status': 'active',
            'model': 'IsolationForest',
            'contamination': 0.05,
            'n_estimators': 100
        }
