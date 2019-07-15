echo "Make sure you have python3 installed"

echo "Installing python dependencies"


pip3 install -r requirements.txt

python3 -m spacy download en

echo "run stanford coreNLP at localhost:9000."
echo "If not present download it and in the root folder run - java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000"

echo "starting server in debug mode"
python3 run_framework.py