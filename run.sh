echo "make sure stanford coreNLP is running at localhost:9000."
echo "If not present download it and in the root folder run - java -mx4g -cp * edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000"

echo "starting server in debug mode"
python3 run_framework.py