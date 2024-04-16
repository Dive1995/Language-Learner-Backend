from flask import Flask
from flask_restful import Api, Resource, reqparse
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
from api_handler import reverso_translate
from scrape import get_context
from mongo import get_or_update_user, add_new_vocabulary

app = Flask(__name__)
CORS(app) 
api = Api(app)

class LangInput:
    def __init__(self, first, second):
        self.first = first
        self.second = second


class YotubeVideo(Resource):
    def post(self):
        video_post_args = reqparse.RequestParser()
        video_post_args.add_argument("video_id", type=str, help="Video id missing", required=True)
        video_post_args.add_argument("lang", type=dict, help="Language missing", required=True) 

        args = video_post_args.parse_args()
        transcript1 = None
        transcript2 = None
        print(args["video_id"])
        lang_input = args["lang"]

        first_langs = lang_input.get('first')
        print("First: ", first_langs)
        second_langs = lang_input.get('second')
        print("Secon: ", second_langs)


        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(args["video_id"])
            
            try:
                manual_transcript1 = transcript_list.find_transcript(first_langs)  
                print("manual1 ",manual_transcript1)
                transcript1 = manual_transcript1

            except Exception as e:
                print(f"Excepption thrown no transcripts for first: {e}")

            try:                
                manual_transcript2 = transcript_list.find_transcript(second_langs)  
                print("manual2 ",manual_transcript2)
                transcript2 = manual_transcript2

            except Exception as e:
                print(f"Excepption thrown no transcripts for second: {e}")

            if transcript1 or transcript2:
                if(transcript1 is None):
                    print("1 is none")
                    transcript1 = transcript2.translate(first_langs)

                if(transcript2 is None):
                    print("2 is none ")
                    print("2 is none ", transcript1.translate(second_langs[0]))
                    transcript2 = transcript1.translate(second_langs[0])
            
            # if transcript1 is None:
            #     try:
            #         generated_transcript1 = transcript_list.find_generated_transcript(first_langs)
            #         print("generated1 ",generated_transcript1)  
            #         transcript1 = generated_transcript1
            #     except Exception as e:
            #         print(f"Exception thrown no generated1 transcripts: {e}")

            # if transcript2 is None:
            #     try:
            #         generated_transcript2 = transcript_list.find_generated_transcript(second_langs)
            #         print("generated2 ",generated_transcript2)  
            #         transcript2 = generated_transcript2
            #     except Exception as e:
            #         print(f"Exception thrown no generated2 transcripts: {e}")

        except Exception as e:
            print(f"Programmatic exception thrown: {e}")

        print("first ", transcript1)
        print("second ", transcript2)
        
        return {"firstTranscript":None, "first_is_generated":None, "secondTranscript":None, "second_is_generated":None} if transcript1 and transcript2 is None else {"firstTranscript":transcript1.fetch(), "first_is_generated":transcript1.is_generated, "secondTranscript":transcript2.fetch(), "second_is_generated":transcript2.is_generated}
        
class Translation(Resource):
    def post(self):
        translte_post_args = reqparse.RequestParser()
        translte_post_args.add_argument("from", type=str, help="Translation from language missing", required=True)
        translte_post_args.add_argument("to", type=str, help="Translation to language missing", required=True)
        translte_post_args.add_argument("input", type=str, help="Translation input missing", required=True)

        args = translte_post_args.parse_args()
        response = reverso_translate(args)
        return response.json()
    
class Context(Resource):
    def post(self):
        context_post_args = reqparse.RequestParser()
        context_post_args.add_argument("word", type=str, help="Word is required", required=True)

        args = context_post_args.parse_args()
        response = get_context(args['word'])
        print("response ", response)
        return response
    
class User(Resource):
    def post(self):
        user_args = reqparse.RequestParser()
        user_args.add_argument("name", type=str, help="Name is required", required=True)
        user_args.add_argument("email", type=str, help="Email is required", required=True)
        user_args.add_argument("family_name", type=str, help="Family name is required", required=True)
        user_args.add_argument("given_name", type=str, help="Given name is required", required=True)

        args = user_args.parse_args()
        print("user args: ", args)
        response = get_or_update_user(args)
        print("user response ", response)
        return response

class Vocabulary(Resource):
    def post(self):
        vocabulary_args = reqparse.RequestParser()
        vocabulary_args.add_argument("id", type=str, required=True, help="userid is required")
        vocabulary_args.add_argument("videoId", type=str, required=True, help="videoId is required")
        vocabulary_args.add_argument("vocabulary", type=dict, required=True, help="vocabulary is required")

        args = vocabulary_args.parse_args()
        print("vocabulary args: ", args)
        response = add_new_vocabulary(args)
        print("vocabulary response ", response)
        return response

api.add_resource(YotubeVideo, "/video")
api.add_resource(Translation, "/vocabulary/translation")
api.add_resource(Context, "/vocabulary/context")
api.add_resource(User, "/user")
api.add_resource(Vocabulary, "/user/vocabulary")

if __name__ == "__main__":
    app.run(debug=True)