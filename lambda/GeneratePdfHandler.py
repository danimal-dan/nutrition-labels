import os
import json
from typing import List
from datetime import datetime
from Models import LabelQuantityPair
from AveryLabels import AveryLabel
from LabelDatabase import *
from PdfGenerator import generate_pdf


def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        template = int(data['template'])
        packetJson = data['labels']
    except (KeyError, TypeError, json.JSONDecodeError):
        return {'statusCode': 400, 'body': 'Invalid JSON structure'}

    # Validate the label
    if template not in [5160, 5161, 5163, 5167, 5371]:
        return {'statusCode': 400, 'body': 'Invalid template'}
    

    # Map and validate items to the domain model
    try:
        averyLabel = AveryLabel(template)
        packet = [LabelQuantityPair(**labelQuantityPair) for labelQuantityPair in packetJson]
        labelsToPrint = [label for pair in packet for label in [pair.label] * pair.quantity]; # flattens the packet into each label repeated the number of times specified by quantity
        generate_pdf(averyLabel, labelsToPrint)
    except KeyError:
        return {'statusCode': 400, 'body': 'Invalid items structure'}

    # Process the labels as needed...

    return {'statusCode': 200, 'body': 'Successfully processed'}
  

# Example event for testing
if __name__ == "__main__":
    # LAMBDA TEST
    # event = {
    #     'body': json.dumps({
    #         "template": 4224,
    #         "labels": [
    #             { "quantity": 1, "label": {"name": "Water", "ingredients": ["H2O"]}},
    #             { "quantity": 5, "label": {"name": "Soup", "ingredients": ["Naadfkjdafaklj", "Chloridad", "Pear", "Baking Soda", "Chicken Broth", { "name": "Formula", "ingredients": ["Aadfadf", "Badsfdafaf"]}]}}
    #         ]
    #     })
    # }
    # print(lambda_handler(event, None))

    # TEST RUN
    averyLabel = AveryLabel(4224)
    labelsToPrint = [
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler(),
        FullSampler()
    ]
    child_name = os.environ.get('NUTRITION_LABELS_CHILD_NAME')
    print('child', child_name)
    header = child_name + ' - ' + datetime.now().strftime("%-m/%-d/%Y") if child_name else ''
    generate_pdf(averyLabel, labelsToPrint, header)
