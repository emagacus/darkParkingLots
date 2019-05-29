
import json

response = "{'plate': 'JMU1303', 'confidence': 87.982277, 'matches_template': 1, 'plate_index': 0, 'region': 'wa', 'region_confidence': 0, 'processing_time_ms': 20.665997, 'requested_topn': 7, 'coordinates': [{'x': 299, 'y': 725}, {'x': 491, 'y': 735}, {'x': 489, 'y': 830}, {'x': 300, 'y': 821}], 'candidates': [{'plate': 'JMU13Q3', 'confidence': 88.643593, 'matches_template': 0}, {'plate': 'JMU1303', 'confidence': 87.982277, 'matches_template': 1}, {'plate': 'JMU13O3', 'confidence': 85.676521, 'matches_template': 0}, {'plate': 'JMU13D3', 'confidence': 85.527176, 'matches_template': 0}, {'plate': 'JMU13U3', 'confidence': 84.078094, 'matches_template': 0}, {'plate': 'JMU13B3', 'confidence': 83.754997, 'matches_template': 0}, {'plate': 'JMU13G3', 'confidence': 83.478088, 'matches_template': 0}]}"
response_dict = json.loads(response)

print(response_dict['plate'])