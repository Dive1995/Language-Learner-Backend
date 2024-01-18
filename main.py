from flask import Flask
from flask_restful import Api, Resource, reqparse
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS
from api_handler import reverso_translate
from scrape import get_context

app = Flask(__name__)
CORS(app) 
api = Api(app)

video_post_args = reqparse.RequestParser()
video_post_args.add_argument("video_id", type=str, help="Video id missing", required=True)
video_post_args.add_argument("lang", type=str, help="Language missing", required=True)

class YotubeVideo(Resource):
    def post(self):
        args = video_post_args.parse_args()
        transcript = None
        print(args["video_id"])

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(args["video_id"])
            
            try:
                manual_transcript = transcript_list.find_manually_created_transcript([args["lang"]])  
                print("manual ",manual_transcript)
                transcript = manual_transcript

            except Exception as e:
                print(f"Excepption thrown no manual transcripts: {e}")
            
            if transcript is None:
                try:
                    generated_transcript = transcript_list.find_generated_transcript([args["lang"]])
                    print("generated ",generated_transcript)  
                    transcript = generated_transcript
                except Exception as e:
                    print(f"Exception thrown no generated transcripts: {e}")

        except Exception as e:
            print(f"Programmatic exception thrown: {e}")
        
        return {"transcript": None, "is_generated": None} if transcript is None else {"transcript":transcript.fetch(), "is_generated":transcript.is_generated}
        


translte_post_args = reqparse.RequestParser()
translte_post_args.add_argument("from", type=str, help="Translation from language missing", required=True)
translte_post_args.add_argument("to", type=str, help="Translation to language missing", required=True)
translte_post_args.add_argument("input", type=str, help="Translation input missing", required=True)

class Translation(Resource):
    def post(self):
        args = translte_post_args.parse_args()
        response = reverso_translate(args)
        return response.json()
    
context_post_args = reqparse.RequestParser()
context_post_args.add_argument("word", type=str, help="Word is required", required=True)
class Context(Resource):
    def post(self):
        args = context_post_args.parse_args()
        response = get_context(args['word'])
        print("response ", response)
        return response


api.add_resource(YotubeVideo, "/video")
api.add_resource(Translation, "/vocabulary/translation")
api.add_resource(Context, "/vocabulary/context")
# api.add_resource(YotubeVideo, "/video/<string:video_id>")

if __name__ == "__main__":
    app.run(debug=True)