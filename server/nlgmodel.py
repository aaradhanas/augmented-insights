class Phrase:
    type=""
    coordinates=[]

class Feature:
    tense=""

class Sentence:
    subject = Phrase()
    verb = ''
    object = Phrase()
    modifiers = []
    features = Feature()

# Sample JSON Payload
'''
            {  
            "sentence":
            {  
                "subject":{  
                "type":"coordinated_phrase",
                "coordinates":
                [  
                    "Beauty category"
                ]
                },
                "verb":"be",
                "object":
                {  
                "type":"coordinated_phrase",
                "coordinates":
                [  
                    "77%"
                ]
                },
                "modifiers":
                [  
                "higher"
                ],
                "indirect_object":"",
                "features":
                {  
                "tense":"present"
                }
            }
        }
    '''