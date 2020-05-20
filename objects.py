class Utterance(object):
    """Represents a snippet of the audio file post performing vad."""

    def __init__(self, sid, path, from_time, to_time, speaker, text, confidence, words, task_id, 
                 encoding=None, lemmas=None, language_code='en-IN'):
        self.sid = sid
        self.path = path
        self.from_time = from_time
        self.to_time = to_time
        self.speaker = speaker
        self.text = text
        self.confidence = confidence
        self.words = words
        self.encoding = encoding
        self.lemmas = lemmas
        self.negation_count = 0
        self.laser_encoding = None
        self.language_code = language_code
        self.task_id = task_id

    def set_sid(self, sid):
        self.sid = sid

    def set_use_encoding(self, encoding):
        self.encoding = encoding

    def set_lemmas(self, lemmas):
        self.lemmas = lemmas

    def set_negation_count(self, negation_count):
        self.negation_count = negation_count

    def set_laser_encoding(self, encoding):
        self.laser_encoding = encoding
        
    def set_speakero(self, speakero):
        self.speakero = speakero
        
        
class Speaker(object):
    
    def __init__(self, type_, user_id, scp_id, sid):
        self.type_ = type_
        self.user_id = user_id
        self.scp_id = scp_id
        self.sid = sid
